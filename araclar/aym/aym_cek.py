#!/usr/bin/env python3
"""Anayasa Mahkemesi vergiyle ilgili kararlarını çeker (yalnızca anayasa.gov.tr).

Kaynak: Anayasa Mahkemesi Kararlar Bilgi Bankası
  Norm denetimi : https://normkararlarbilgibankasi.anayasa.gov.tr  (iptal / itiraz)
  Bireysel başvuru: https://kararlarbilgibankasi.anayasa.gov.tr
Her iki sitenin kendi arama API'si (POST /api/core/public/search) kullanılır.

Kapsam ("vergiyle ilgili" karar):
  Norm denetimi  : (a) incelenen norm vergi/harç/amme alacağı/YMM vb. bir kanun, KHK, tebliğ veya
                   yönetmelik olan kararlar; (b) başvuranı vergi mahkemesi / vergi dava dairesi
                   olan itiraz kararları; (c) metninde "vergi" geçen ve karar konusu vergi,
                   harç, resim, amme alacağı vb. olan kararlar.
  Bireysel başvuru: (a) ilgili mevzuatı vergi kanunlarından biri olan kararlar; (b) metninde
                   "vergi" geçen ve karar konusu vergi, harç, amme alacağı vb. olan kararlar.

Çıktı: kararlar/anayasa-mahkemesi/{norm-denetimi,bireysel-basvuru}/<yıl>/<no>.md,
       kararlar/anayasa-mahkemesi/README.md ve konular.md (konu başlıklarına göre dizin).

Kullanım: python3 araclar/aym/aym_cek.py <depo kökü>
"""
import concurrent.futures as cf, html as htmlmod, json, os, re, sys, time, urllib.request
from bs4 import BeautifulSoup

NORM = "https://normkararlarbilgibankasi.anayasa.gov.tr"
BB = "https://kararlarbilgibankasi.anayasa.gov.tr"
VERGI_TANIM = re.compile(r"(Vergi|Amme Alacak|Harçlar|Harç|Belediye Gelirleri|Gümrük Kanunu|Yeminli Mali)", re.I)
VERGI_KONU = re.compile(r"(vergi|harç|harc|resmi\b|resim|amme alaca|tahsil|gümrük|fon pay|katkı pay|ödeme emri|"
                        r"kdv|katma değer|tarh|matrah|stopaj|tevkifat|vergi ziya|usulsüzlük|mükellef)", re.I)

# konu başlıkları: (başlık, desen) — karar konusu + metin üzerinde aranır
KONULAR = [
    ("KDV iadesi", r"(kdv|katma değer vergisi)[^.]{0,120}iade|iade[^.]{0,60}(kdv|katma değer vergisi)"),
    ("Katma değer vergisi", r"katma değer vergisi|\bkdv\b"),
    ("Sahte / muhteviyatı itibarıyla yanıltıcı belge", r"sahte (fatura|belge)|muhteviyatı itibarıyla yanıltıcı|naylon fatura"),
    ("Vergi ziyaı ve vergi cezaları", r"vergi ziya|usulsüzlük cezası|özel usulsüzlük|vergi cezas|kaçakçılık"),
    ("Tahsilat, ödeme emri ve haciz (6183)", r"6183|ödeme emri|amme alaca|haciz|teminat|ihtiyati"),
    ("Gecikme faizi ve gecikme zammı", r"gecikme faizi|gecikme zammı|pişmanlık zammı"),
    ("Kanuni temsilci / ortak sorumluluğu", r"kanuni temsilci|ortakların sorumluluğu|mükerrer 35"),
    ("Vergi incelemesi ve tarhiyat", r"vergi incelemesi|re'sen tarh|resen tarh|ikmalen|tarhiyat|takdir komisyonu"),
    ("Uzlaşma ve yapılandırma", r"uzlaşma|yapılandırma|vergi barışı|matrah artırımı"),
    ("Zamanaşımı", r"zamanaşımı"),
    ("Gelir vergisi", r"gelir vergisi"),
    ("Kurumlar vergisi", r"kurumlar vergisi"),
    ("Özel tüketim vergisi", r"özel tüketim vergisi|\bötv\b"),
    ("Damga vergisi", r"damga vergisi"),
    ("Harçlar", r"harçlar kanunu|harç"),
    ("Emlak vergisi", r"emlak vergisi|bina vergisi|arazi vergisi"),
    ("Motorlu taşıtlar vergisi", r"motorlu taşıtlar vergisi"),
    ("Veraset ve intikal vergisi", r"veraset ve intikal"),
    ("Belediye gelirleri", r"belediye gelirleri"),
    ("Gümrük vergileri", r"gümrük vergi|gümrük kanunu"),
    ("SMMM / YMM", r"yeminli mali müşavir|serbest muhasebeci|3568"),
    ("Mülkiyet hakkı (vergi)", r"mülkiyet hakk"),
    ("Kanunilik ilkesi (Anayasa md. 73)", r"73\. madde|anayasa'nın 73|vergi ödevi|kanunilik ilkesi|yasallık ilkesi"),
]
KONULAR = [(a, re.compile(b, re.I)) for a, b in KONULAR]
KDV_IADE = re.compile(r"kdv iade|katma değer vergisi iade|iade edilecek katma değer|kdv alacağı|katma değer vergisi alaca", re.I)


def etiketle(konu, metin=""):
    """Başlıklar önce karar konusuna (itiraz/iptal konusu, başvuru konusu) göre atanır. Konudan hiçbir
    başlık çıkmazsa, karar metninde en az 5 kez geçen başlıklar atanır."""
    e = [a for a, p in KONULAR if p.search(konu or "")]
    # KDV iadesi ayrıca: metinde en az 2 kez KDV iadesi / KDV alacağı geçiyorsa
    if "KDV iadesi" not in e and len(KDV_IADE.findall(metin or "")) >= 2:
        e.insert(0, "KDV iadesi")
    if e or not metin:
        return e
    return [a for a, p in KONULAR if len(p.findall(metin)) >= 5]


def post(host, govde):
    for d in range(5):
        try:
            r = urllib.request.Request(f"{host}/api/core/public/search", data=json.dumps(govde).encode(),
                                       headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 ymm-mevzuat-bankasi"},
                                       method="POST")
            with urllib.request.urlopen(r, timeout=180) as y:
                return json.load(y)
        except Exception as e:
            print(f"  ! {e}; tekrar", file=sys.stderr, flush=True)
            time.sleep(4 * (d + 1))
    raise RuntimeError(f"alınamadı: {govde}")


def tumu(host, govde, boyut=500):
    """Sayfa numarası 1'den başlar (0 ile 1 aynı sonucu verir)."""
    out, s = [], 1
    while True:
        r = post(host, dict(govde, page=str(s), size=str(boyut)))
        out += r.get("data") or []
        if len(r.get("data") or []) < boyut or len(out) >= r.get("total", 0):
            return out, r.get("total", 0)
        s += 1


def onar(s):
    """Kaynaktaki çift kodlanmış UTF-8'i (Ä°, ÅŸ, Ã§ ...) düzeltir."""
    if s and re.search(r"Ã.|Ä.|Å.", s):
        try:
            t = s.encode("cp1252", "strict").decode("utf-8", "strict")
            return t
        except Exception:
            try:
                return s.encode("latin-1", "strict").decode("utf-8", "strict")
            except Exception:
                return s
    return s


def metne(h):
    if not h:
        return ""
    soup = BeautifulSoup(h, "html.parser")
    for x in soup(["script", "style"]):
        x.decompose()
    for tr in soup.find_all("tr"):
        tr.replace_with(" | ".join(td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])) + "\n")
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for p in soup.find_all(["p", "div", "li", "h1", "h2", "h3", "h4"]):
        p.append("\n")
    t = htmlmod.unescape(soup.get_text())
    t = re.sub(r"[ \t\xa0]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return onar(re.sub(r"\n{3,}", "\n\n", t).strip())


def tanimlar():
    with urllib.request.urlopen(f"{NORM}/api/core/public/tanim/lookup", timeout=180) as y:
        return json.load(y)["data"]


def aday_listesi():
    t = tanimlar()
    secilen = lambda pids: [x for x in t if x.get("isim") and VERGI_TANIM.search(x["isim"]) and x["paramId"][:8] in pids]
    norm, neden = {}, {}

    def ekle(d, kayitlar, gerekce):
        for k in kayitlar:
            d.setdefault(k["id"], k)
            neden.setdefault(k["id"], set()).add(gerekce)

    for alan, pids, ger in [("normNumaraAdParamId", {"53ab265d", "a5d73691", "852d9609", "c64f0e7b"}, "incelenen norm vergi mevzuatı"),
                            ("basvuranOzel", {"fd7cb719"}, "başvuran vergi mahkemesi/dairesi"),
                            ("basvuranGenel", {"83de86e5"}, "başvuran vergi mahkemesi/dairesi")]:
        for x in secilen(pids):
            k, _ = tumu(NORM, {"kararTipi": "NormDenetimi", alan: x["id"]})
            ekle(norm, k, ger)
    k, _ = tumu(NORM, {"kararTipi": "NormDenetimi", "query": "vergi"})
    ekle(norm, [x for x in k if VERGI_KONU.search(onar(metne(x.get("kararKonusu"))))], "karar konusu vergi")
    bb = {}
    for x in secilen({"77dceefd"}):
        k, _ = tumu(BB, {"kararTipi": "BireyselBasvuru", "ilgiliHukukMevzuatTarihiNoIsimParamId": x["id"]})
        ekle(bb, k, "ilgili mevzuat vergi kanunu")
    k, _ = tumu(BB, {"kararTipi": "BireyselBasvuru", "query": "vergi"})
    ekle(bb, [x for x in k if VERGI_KONU.search(onar(metne(x.get("kararKonusu"))))], "karar konusu vergi")
    return norm, bb, neden


def dosya_adi(k):
    if k["kararTipi"] == "NormDenetimi":
        e = (k.get("esasNo") or "x").replace("/", "-")
        n = (k.get("kararNo") or "x").replace("/", "-")
        yil = (k.get("kararNo") or k.get("kararTarihi") or "0000")[:4]
        return os.path.join("norm-denetimi", yil, f"E{e}_K{n}.md")
    no = (k.get("basvuruNo") or k["id"]).replace("/", "-")
    yil = (k.get("kararTarihi") or "0000")[:4]
    return os.path.join("bireysel-basvuru", yil, f"{no}_{k['id'][:8]}.md")


def detay(k):
    host = NORM if k["kararTipi"] == "NormDenetimi" else BB
    r = post(host, {"kararTipi": k["kararTipi"], "id": k["id"]})
    x = (r.get("data") or [{}])[0]
    return x


def yaz(kok, k, x, neden):
    yol = os.path.join(kok, dosya_adi(k))
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    konu = metne(x.get("kararKonusu") or k.get("kararKonusu"))
    metin = metne(x.get("icerik"))
    norm = k["kararTipi"] == "NormDenetimi"
    host = NORM if norm else BB
    etiket = etiketle(konu, metin)
    if norm:
        kunye = [f"esas_no: {k.get('esasNo','')}", f"karar_no: {k.get('kararNo','')}",
                 f"resmi_gazete: {k.get('resmiGazeteTarihi') or ''} / {k.get('resmiGazeteSayisi') or ''}"]
        baslik = f"AYM E.{k.get('esasNo','')}, K.{k.get('kararNo','')}"
    else:
        kunye = [f"basvuru_no: {k.get('basvuruNo','')}", f"basvuru_adi: {json.dumps(k.get('basvuruAdi') or '', ensure_ascii=False)}",
                 f"karar_veren: {k.get('kararVerenBirimLabel') or ''}"]
        baslik = f"AYM B. No: {k.get('basvuruNo','')} — {k.get('basvuruAdi') or ''}"
    sonuc = k.get("kararTuruDosyaSonucuLabel") or k.get("kararTuruBasvuruSonucuLabel") or ""
    icerik = "\n".join(["---", f"tur: {'Norm denetimi' if norm else 'Bireysel başvuru'}", *kunye,
                        f"karar_tarihi: {k.get('kararTarihi') or ''}", f"sonuc: {sonuc}",
                        f"konular: {json.dumps(etiket, ensure_ascii=False)}",
                        f"secim_gerekcesi: {json.dumps(sorted(neden), ensure_ascii=False)}",
                        f"aym_id: {k['id']}", f"kaynak: {host}/kbb/",
                        f"alindi: {time.strftime('%Y-%m-%d')}", "---", "", f"# {baslik}", "",
                        f"**Sonuç:** {sonuc}  ", f"**Karar tarihi:** {k.get('kararTarihi') or ''}", "",
                        "## Karar konusu", "", konu or "_(yok)_", "", "## Karar metni", "",
                        metin or "_(Metin karar bankasında yok.)_", ""])
    open(yol, "w", encoding="utf-8").write(icerik)
    return {"yol": os.path.relpath(yol, kok), "tur": "Norm" if norm else "Bireysel", "tarih": k.get("kararTarihi") or "",
            "no": (f"E.{k.get('esasNo','')} K.{k.get('kararNo','')}" if norm else k.get("basvuruNo") or ""),
            "ad": (konu[:140].replace("\n", " ") if norm else (k.get("basvuruAdi") or "")), "sonuc": sonuc,
            "konular": etiket, "metin": len(metin)}


def main():
    depo = sys.argv[1]
    kok = os.path.join(depo, "kararlar", "anayasa-mahkemesi")
    os.makedirs(kok, exist_ok=True)
    norm, bb, neden = aday_listesi()
    print(f"aday: norm {len(norm)}, bireysel {len(bb)}", flush=True)
    hepsi = list(norm.values()) + list(bb.values())
    kayit, hata = [], []

    def isle(k):
        try:
            return yaz(kok, k, detay(k), neden[k["id"]])
        except Exception as e:
            hata.append((k["id"], str(e)))
            return None

    with cf.ThreadPoolExecutor(4) as ex:
        for i, r in enumerate(ex.map(isle, hepsi), 1):
            if r:
                kayit.append(r)
            if i % 100 == 0:
                print(f"{i}/{len(hepsi)}", flush=True)
    kayit.sort(key=lambda x: x["tarih"], reverse=True)
    json.dump({"kayit": kayit, "hata": hata}, open(os.path.join(kok, "_dizin.json"), "w"), ensure_ascii=False, indent=0)
    # konu dizini
    with open(os.path.join(kok, "konular.md"), "w", encoding="utf-8") as o:
        o.write("# Anayasa Mahkemesi vergi kararları — konu başlıklarına göre\n\n"
                "Bir karar birden çok başlıkta yer alabilir. Başlıklar karar konusu ve metindeki ifadelere göre "
                "otomatik atanmıştır; kesin değerlendirme için karar metnine bakınız.\n\n")
        for a, _ in KONULAR:
            liste = [x for x in kayit if a in x["konular"]]
            if not liste:
                continue
            o.write(f"## {a} ({len(liste)})\n\n| Tarih | Tür | Karar | Sonuç | Konu / Başvurucu |\n|---|---|---|---|---|\n")
            for x in liste:
                o.write(f"| {x['tarih']} | {x['tur']} | [{x['no']}]({x['yol']}) | {x['sonuc']} | {x['ad'].replace('|','/')} |\n")
            o.write("\n")
    for tur, klasor in (("Norm", "norm-denetimi"), ("Bireysel", "bireysel-basvuru")):
        liste = [x for x in kayit if x["tur"] == tur]
        with open(os.path.join(kok, klasor, "README.md"), "w", encoding="utf-8") as o:
            o.write(f"# Anayasa Mahkemesi — {'norm denetimi' if tur=='Norm' else 'bireysel başvuru'} (vergi) — {len(liste)} karar\n\n"
                    "| Tarih | Karar | Sonuç | Konu / Başvurucu |\n|---|---|---|---|\n")
            for x in liste:
                o.write(f"| {x['tarih']} | [{x['no']}]({os.path.relpath(x['yol'], klasor)}) | {x['sonuc']} | {x['ad'].replace('|','/')} |\n")
    print(json.dumps({"norm": sum(1 for x in kayit if x["tur"] == "Norm"), "bireysel": sum(1 for x in kayit if x["tur"] == "Bireysel"),
                      "hata": len(hata), "metinsiz": sum(1 for x in kayit if x["metin"] < 500)}, ensure_ascii=False))


def yeniden_dizin(depo):
    kok = os.path.join(depo, "kararlar", "anayasa-mahkemesi")
    d = json.load(open(os.path.join(kok, "_dizin.json")))
    for x in d["kayit"]:
        yol = os.path.join(kok, x["yol"])
        t = open(yol, encoding="utf-8").read()
        konu = (re.search(r"## Karar konusu\n\n(.*?)\n\n## Karar metni", t, re.S) or [None, ""])[1]
        metin = t.split("## Karar metni", 1)[-1]
        x["konular"] = etiketle(konu, metin)
        t = re.sub(r"\nkonular: .*", "\nkonular: " + json.dumps(x["konular"], ensure_ascii=False).replace("\\", "\\\\"), t, count=1)
        open(yol, "w", encoding="utf-8").write(t)
    json.dump(d, open(os.path.join(kok, "_dizin.json"), "w"), ensure_ascii=False, indent=0)
    return d["kayit"]


def konu_dizini(kok, kayit):
    with open(os.path.join(kok, "konular.md"), "w", encoding="utf-8") as o:
        o.write("# Anayasa Mahkemesi vergi kararları — konu başlıklarına göre\n\n"
                "Bir karar birden çok başlıkta yer alabilir. Başlıklar karar konusundaki (itiraz/iptal konusu, "
                "başvuru konusu) ifadelere, konudan çıkmadığında karar metninde en az 5 kez geçen ifadelere göre otomatik atanmıştır; kesin değerlendirme için karar metnine bakınız.\n\n")
        for a, _ in KONULAR:
            liste = [x for x in kayit if a in x["konular"]]
            if not liste:
                continue
            o.write(f"## {a} ({len(liste)})\n\n| Tarih | Tür | Karar | Sonuç | Konu / Başvurucu |\n|---|---|---|---|---|\n")
            for x in liste:
                o.write(f"| {x['tarih']} | {x['tur']} | [{x['no']}]({x['yol']}) | {x['sonuc']} | {x['ad'].replace('|','/')} |\n")
            o.write("\n")
        diger = [x for x in kayit if not x["konular"]]
        o.write(f"## Başlık atanamayanlar ({len(diger)})\n\n| Tarih | Tür | Karar | Sonuç | Konu / Başvurucu |\n|---|---|---|---|---|\n")
        for x in diger:
            o.write(f"| {x['tarih']} | {x['tur']} | [{x['no']}]({x['yol']}) | {x['sonuc']} | {x['ad'].replace('|','/')} |\n")


if __name__ == "__main__":
    if sys.argv[2:] == ["dizin"]:
        k = yeniden_dizin(sys.argv[1])
        konu_dizini(os.path.join(sys.argv[1], "kararlar", "anayasa-mahkemesi"), k)
    else:
        main()
