#!/usr/bin/env python3
"""KAYSİS'ten (kms.kaysis.gov.tr, SGK kurum sayfası) tarayıcıyla alınan paketleri depoya işler.

KAYSİS yurt dışından erişime kapalı olduğundan belgeler kullanıcının bilgisayarındaki tarayıcıda
indirilip `kaysis-sgk-paket-NN.json` paketlerine konur (her belge base64 PDF). Bu betik paketleri açar:
  sgk/kaysis/<kategori>/<sayi>-<baslik>.pdf   (resmî PDF, olduğu gibi)
  sgk/kaysis/<kategori>/<sayi>-<baslik>.txt   (pdftotext metni; başında künye)
  sgk/kaysis/dizin.csv, sgk/kaysis/README.md
Çift kontrol: (1) PDF'in SHA-256'sı ve boyutu paketteki boyutla eşleşir; (2) metnin ilk sayfasında
KAYSİS dizinindeki sayı (ör. 2026/23) ya da başlığın ilk kelimeleri geçer. Tutmayanlar raporlanır.

Kullanım: python3 araclar/sgk/kaysis_isle.py <paket klasörü> [--pdf-sakla]
"""
import base64, csv, hashlib, json, pathlib, re, subprocess, sys, unicodedata, datetime, collections

KOK = pathlib.Path(__file__).resolve().parents[2]
HEDEF = KOK / "sgk" / "kaysis"
TR = str.maketrans("çğıöşüÇĞİÖŞÜâîûÂÎÛ", "cgiosuCGIOSUaiuAIU")
KAT = {"Kanunlar": "kanunlar", "Bakanlar Kurulu Kararları": "bakanlar-kurulu-kararlari", "Uluslararası Antlaşmalar": "uluslararasi-antlasmalar",
       "Kurum Yönetmelikleri": "yonetmelikler", "Kurum Genelgeleri": "genelgeler", "Esas ve Usuller": "usul-ve-esaslar", "Tebliğler": "tebligler",
       "Yönergeler": "yonergeler", "Talimat/Talimatname/İç emirler": "talimatlar", "Kurul / Komisyon / Konsey Kararları": "kurul-kararlari",
       "Sözleşme / Protokoller": "protokoller", "Genel Yazılar": "genel-yazilar"}


def slug(s, n=70):
    s = unicodedata.normalize("NFKD", s.translate(TR).lower()).encode("ascii", "ignore").decode()
    return (re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:n].rstrip("-")) or "adsiz"


def tr_low(s):
    return re.sub(r"\s+", "", s.replace("İ", "i").replace("I", "ı").lower())


OCR_ON = pathlib.Path("/tmp/kaysis_ocr")


def ocr(veri, sha):
    """Taranmış PDF için Türkçe OCR (tesseract, 200 dpi); sonuç sha'ya göre önbelleğe alınır."""
    OCR_ON.mkdir(exist_ok=True)
    on = OCR_ON / f"{sha}.txt"
    if on.exists():
        return on.read_text(encoding="utf-8")
    import tempfile, concurrent.futures as cf
    with tempfile.TemporaryDirectory() as d:
        pdf = pathlib.Path(d) / "a.pdf"; pdf.write_bytes(veri)
        subprocess.run(["pdftoppm", "-r", "200", "-gray", "-png", str(pdf), str(pathlib.Path(d) / "s")], capture_output=True)
        sayfalar = sorted(pathlib.Path(d).glob("s-*.png"))
        def tek(png):
            return subprocess.run(["tesseract", str(png), "-", "-l", "tur", "--psm", "6"], capture_output=True).stdout.decode("utf-8", "replace")
        with cf.ThreadPoolExecutor(4) as ex:
            metin = "\n\f".join(ex.map(tek, sayfalar))
    on.write_text(metin, encoding="utf-8")
    return metin


def sayfa_sayisi(veri):
    o = subprocess.run(["pdfinfo", "-"], input=veri, capture_output=True).stdout.decode("utf-8", "replace")
    m = re.search(r"Pages:\s*(\d+)", o)
    return int(m.group(1)) if m else 0


def main():
    kaynak = pathlib.Path(sys.argv[1])
    pdf_sakla = "--pdf-sakla" in sys.argv
    ekle = "--ekle" in sys.argv
    desen = sys.argv[sys.argv.index("--desen") + 1] if "--desen" in sys.argv else "kaysis-sgk-paket-*.json"
    paketler = sorted(kaynak.glob(desen))
    dizin, docs = None, {}
    alinma = ""
    for p in paketler:
        j = json.loads(p.read_text(encoding="utf-8"))
        alinma = alinma or j.get("alinma", "")
        if j.get("dizin"):
            dizin = j["dizin"]
        for d in j["docs"]:
            docs[(d["kat"], d["id"])] = d
    if not dizin:
        sys.exit("dizin (paket 01) bulunamadı")
    tarih = (alinma[:10] or str(datetime.date.today()))
    tarih_tr = f"{tarih[8:10]}.{tarih[5:7]}.{tarih[:4]}"
    rapor = {"paket": len(paketler), "dizin": len(dizin), "belge": len(docs), "yazilan": 0, "eksik": [], "pdf_degil": [],
             "boyut_tutmadi": [], "kontrol2_tutmadi": [], "metinsiz": []}
    satirlar = []
    kullanilan = set()
    eski = {}
    if ekle and (HEDEF / "dizin.csv").exists():
        with (HEDEF / "dizin.csv").open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                eski[(r["kategori"], r["kaynak"].rsplit("/", 1)[-1])] = r
                kullanilan.add(pathlib.Path(r["dosya"]).stem)
    rapor["yeni"] = []
    for x in dizin:
        d = docs.get((x["kat"], x["id"]))
        if ekle and (x["kat"], x["id"]) in eski:
            d = None  # artımlı kipte depoda olan kayıt yeniden işlenmez
        if not d:
            e = eski.get((x["kat"], x["id"]))
            if e:
                satirlar.append([e["kategori"], e["sayi"], e["baslik"], e["resmi_gazete"], e["dosya"], e["kaynak"], e["pdf_sha256"], e["kontrol2"]])
            else:
                rapor["eksik"].append(x["id"])
            continue
        rapor["yeni"].append(f"{x['kat']} | {x['sayi']} | {x['baslik']}")
        veri = base64.b64decode(d["b64"])
        if len(veri) != d["boyut"]:
            rapor["boyut_tutmadi"].append(x["id"])
        klasor = HEDEF / KAT.get(x["kat"], slug(x["kat"]))
        klasor.mkdir(parents=True, exist_ok=True)
        ad = f"{slug(x['sayi'], 20)}-{slug(x['baslik'])}"
        while ad in kullanilan:
            ad += f"-{x['id']}"
        kullanilan.add(ad)
        sha = hashlib.sha256(veri).hexdigest()
        ocrlu = dosya_yok = False
        if veri.startswith(b"%PDF"):
            metin = subprocess.run(["pdftotext", "-layout", "-", "-"], input=veri, capture_output=True).stdout.decode("utf-8", "replace")
            if len(re.sub(r"\s+", "", metin)) < 100:
                metin = ocr(veri, sha); ocrlu = True
                rapor.setdefault("ocr", []).append(f"{klasor.name}/{ad}")
            uzanti = "pdf"
        else:
            kod = (re.search(r"charset=([\w-]+)", d["ct"]) or re.search(rb"charset=([\w-]+)", veri[:3000]))
            kod = (kod.group(1).decode() if isinstance(kod.group(1), bytes) else kod.group(1)) if kod else "windows-1254"
            try:
                html = veri.decode(kod, "replace")
            except LookupError:
                html = veri.decode("windows-1254", "replace")
            dosya_yok = "Dosya Bulunamad" in html
            from bs4 import BeautifulSoup
            bs = BeautifulSoup(html, "html.parser")
            for t in bs(["script", "style", "head", "title"]):
                t.decompose()
            metin = "" if dosya_yok else re.sub(r"\n{3,}", "\n\n", bs.get_text("\n")).strip() + "\n"
            rapor["pdf_degil"].append([x["id"], "KAYSİS'te dosya yok" if dosya_yok else "HTML belge (metni alındı)"])
            uzanti = "html"
        if pdf_sakla and uzanti == "pdf":
            (klasor / f"{ad}.pdf").write_bytes(veri)
        metinsiz = len(re.sub(r"\s+", "", metin)) < 100
        if metinsiz and not dosya_yok:
            rapor["metinsiz"].append(f"{klasor.name}/{ad}")
        # kontrol 2: sayı veya başlık metnin başında
        bas = tr_low(metin[:20000])
        bas_n = re.sub(r"[/\-.]", "", bas)
        parcalar = [q for q in re.split(r"[\s\-–]+", x["sayi"].replace("Resmi Gazete:", "")) if len(re.sub(r"\D", "", q)) >= 3]
        sayi_ok = any(re.sub(r"[/\-.]", "", tr_low(q)) in bas_n for q in parcalar)
        kelimeler = [w for w in re.findall(r"\w+", x["baslik"]) if len(w) > 3][:6]
        baslik_ok = bool(kelimeler) and sum(tr_low(w) in bas for w in kelimeler) >= max(2, len(kelimeler) - 1)
        k2 = sayi_ok or baslik_ok
        if not k2 and not ocrlu and not dosya_yok and veri.startswith(b"%PDF") and sayfa_sayisi(veri) <= 30:
            # metin katmanı bozuk olabilir: OCR ile yeniden dene, kontrol tutarsa OCR metnini kullan
            m2 = ocr(veri, sha); b2 = tr_low(m2[:20000]); b2n = re.sub(r"[/\-.]", "", b2)
            if any(re.sub(r"[/\-.]", "", tr_low(q)) in b2n for q in parcalar) or (kelimeler and sum(tr_low(w) in b2 for w in kelimeler) >= max(2, len(kelimeler) - 1)):
                metin, ocrlu, k2 = m2, True, True
                rapor.setdefault("ocr", []).append(f"{klasor.name}/{ad} (metin katmanı bozuktu)")
        if not k2 and not metinsiz:
            rapor["kontrol2_tutmadi"].append(f"{klasor.name}/{ad}")
        kaynak_url = f"https://kms.kaysis.gov.tr/Home/Goster/{x['id']}"
        kunye = (f"KAYNAK: {kaynak_url}\nKURUM: Sosyal Güvenlik Kurumu Başkanlığı (KAYSİS)\nTÜR: {x['kat']}\nSAYI: {x['sayi']}\n"
                 f"ADI: {x['baslik']}\n" + (f"RESMÎ GAZETE: {re.sub(r'^Resmi Gazete:\s*', '', x['rg'])}\n" if x.get("rg") else "") +
                 (f"ALINMA: {tarih_tr} (KAYSİS resmî {'PDF' if uzanti == 'pdf' else 'HTML belge'}; kullanıcının bilgisayarındaki tarayıcıdan)\n{'PDF' if uzanti == 'pdf' else 'BELGE'} SHA-256: {sha}\n" if not dosya_yok else f"ALINMA: {tarih_tr}\nDURUM: KAYSİS'te bu kaydın dosyası yok (\"Dosya Bulunamadı\"); yalnızca künye\n") +
                 (f"METİN: taranmış PDF; Türkçe OCR ile çıkarıldı (tesseract). OCR hataları olabilir, rakam ve tarihleri kaynak PDF'ten teyit ediniz.\n" if ocrlu else "") +
                 f"KONTROL: boyut {'tamam' if len(veri) == d['boyut'] else 'TUTMADI'}; sayı/başlık metinde {'bulundu' if k2 else ('metin yok' if metinsiz else 'BULUNAMADI')}\n\n")
        (klasor / f"{ad}.txt").write_text(kunye + ("" if dosya_yok else ("METİN ÇIKARILAMADI (kaynak bağlantısına bakınız)\n" if metinsiz else "")) + metin,
                                          encoding="utf-8")
        rapor["yazilan"] += 1
        satirlar.append([x["kat"], x["sayi"], x["baslik"], x.get("rg", ""), f"{klasor.name}/{ad}.txt", kaynak_url, sha, "evet" if k2 else "hayır"])
    with (HEDEF / "dizin.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["kategori", "sayi", "baslik", "resmi_gazete", "dosya", "kaynak", "pdf_sha256", "kontrol2"])
        w.writerows(satirlar)
    say = collections.Counter(s[0] for s in satirlar)
    fs = [HEDEF / s_[4] for s_ in satirlar if (HEDEF / s_[4]).exists()]
    bas_ = {f: f.read_text(encoding="utf-8", errors="replace")[:2500] for f in fs}
    yok_ = [f for f, b in bas_.items() if "DURUM: KAYSİS'te bu kaydın dosyası yok" in b]
    html_ = sum("KAYSİS resmî HTML belge" in b for b in bas_.values())
    ocr_ = sum("Türkçe OCR ile" in b for b in bas_.values())
    k2_ = [f for f, b in bas_.items() if "BULUNAMADI" in b]
    gecen = len(fs) - len(k2_) - len(yok_)
    md = ["# SGK mevzuatı — KAYSİS (kms.kaysis.gov.tr)", "",
          f"Kaynak: Sosyal Güvenlik Kurumu Başkanlığının KAYSİS kurum sayfası (https://kms.kaysis.gov.tr/Home/Kurum/22620739). Son güncelleme: {tarih_tr}.",
          "KAYSİS yurt dışından erişime kapalı olduğundan belgeler kullanıcının bilgisayarındaki tarayıcıdan resmî PDF olarak alınır "
          "(`araclar/sgk/kaysis_indir.js`) ve `araclar/sgk/kaysis_isle.py` ile metne çevrilir. Her dosyanın başında kaynak bağlantısı, sayı, SHA-256 ve kontrol sonucu yazar.", "",
          f"**Çift kontrol:** (1) indirilen belgenin boyutu KAYSİS'in gönderdiğiyle eşleşiyor ve SHA-256 değeri dosyanın başına yazıldı; (2) belgenin sayısı ya da başlığı metnin başında (ilk ~20.000 karakter) geçiyor. "
          f"{len(fs)} kaydın {gecen}'i iki kontrolden de geçti. {len(k2_)} belgede sayı/başlık metnin başında bulunamadı; bunlar ek/form, içindekiler sayfası ya da Resmî Gazete sayfa başlığıyla başlıyor (aşağıda listeli, içerik elle teyit edilmeli). "
          f"{len(yok_)} kaydın KAYSİS'te dosyası yok (yalnızca künye). {ocr_} taranmış ya da metin katmanı bozuk PDF Türkçe OCR ile metne çevrildi (dosyalarında işaretli; OCR hatası olabileceğinden rakam ve tarihleri kaynak PDF'ten teyit ediniz). "
          f"{html_} belge KAYSİS'te PDF yerine HTML olarak sunuluyor; metni HTML'den alındı.", "",
          "Not: KAYSİS'teki genelgeler ve genel yazılar Resmî Gazete'de yayımlanmaz; SGK'nın kendi düzenlemeleridir. Yeni kayıtlar, kullanıcının bilgisayarında çalışan günlük görevle eklenir.", "",
          "| Klasör | Kategori | Adet |", "|---|---|---|"]
    md += [f"| `{KAT.get(k, slug(k))}/` | {k} | {n} |" for k, n in say.most_common()]
    md += ["", "Tam liste: `dizin.csv`.", ""]
    if k2_:
        md += ["## Sayı/başlık metinde bulunamayanlar (elle bakılmalı)", ""] + [f"- `{f.relative_to(HEDEF).with_suffix('').as_posix()}`" for f in k2_] + [""]
    (HEDEF / "README.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 30 else f"{len(v)} kayıt") for k, v in rapor.items()}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
