#!/usr/bin/env python3
"""mevzuat.gov.tr kaynaklı depo içeriğini güncel tutar (yalnızca www.mevzuat.gov.tr).

Kapsam
  - Depodaki mevzuat.gov.tr kaynaklı her metin yeniden okunur ve boşluklar yok sayılarak
    karşılaştırılır; yalnızca gerçekten değişen metin yeniden yazılır:
      * PDF kaynaklı kanun klasörleri (kanunlar/<kanun>/, kanunlar/tum/<kanun>/): PDF indirilir,
        pdftotext -layout ile tam-metin.txt karşılaştırılır; değiştiyse PDF, tam metin, madde
        dosyaları (araclar/bol.py), ANALIZ.md (araclar/analiz.py) ve KAYNAK.md yenilenir.
      * İlk satırı "KAYNAK: https://www.mevzuat.gov.tr/mevzuat?..." olan metin dosyaları
        (tüzükler, genel tebliğler, yönetmelikler, KDVGUT, diğer tebliğler, CB kararnameleri).
  - Listeye yeni giren kayıtlar eklenir: kanunlar, tüzükler, başlığında "GENEL TEBLİĞ" geçen
    tebliğler, Cumhurbaşkanlığı kararnameleri, Cumhurbaşkanı kararları ve Cumhurbaşkanlığı genelgeleri.
  - Listeden çıkan (mülga olabilecek) kayıtlar silinmez, raporlanır.

Kullanım
  python3 araclar/mevzuat/mevzuat_tara.py guncelle [--kuru] [--sinir N]
  python3 araclar/mevzuat/mevzuat_tara.py haftalik   # guncelle + CB kararlarının değişiklik kontrolü
Çıktı: son satırda JSON özet; değişiklikler GUNLUK-mevzuat.md dosyasına eklenir.
"""
import argparse, concurrent.futures as cf, datetime, hashlib, json, os, pathlib, re, subprocess, sys, threading, time, unicodedata

import requests
from bs4 import BeautifulSoup

KOK = pathlib.Path(__file__).resolve().parents[2]
SITE = "https://www.mevzuat.gov.tr"
BUGUN = datetime.date.today()
BUGUN_TR = BUGUN.strftime("%d.%m.%Y")
TR = str.maketrans("çğıöşüÇĞİÖŞÜâîûÂÎÛ", "cgiosuCGIOSUaiuAIU")
KILIT = threading.Lock()
_yerel = threading.local()

# toplu_isle.py ile aynı konu aileleri (genel tebliğ klasörleri)
AILE = [("vergi-usul-kanunu", r"VERG[İI] USUL"), ("gelir-vergisi", r"GEL[İI]R VERG[İI]S[İI]"),
        ("kurumlar-vergisi", r"KURUMLAR VERG|KURUMLAR VERGİSİ|ASGARİ TAMAMLAYICI"), ("harclar", r"HARÇLAR|HARCI"),
        ("damga-vergisi", r"DAMGA VERG"), ("emlak-vergisi", r"EMLAK VERG"), ("belediye-gelirleri", r"BELED[İI]YE GEL[İI]RLER"),
        ("motorlu-tasitlar-vergisi", r"MOTORLU TAŞITLAR"), ("ozel-iletisim-vergisi", r"ÖZEL İLETİŞİM"),
        ("veraset-intikal", r"VERASET"), ("tahsilat", r"TAHS[İI]LAT GENEL"), ("gider-vergileri", r"G[İI]DER VERG"),
        ("ozel-tuketim-vergisi", r"ÖZEL TÜKETİM"), ("kdv", r"KATMA DEĞER"), ("3568-smmm-ymm", r"MUHASEBEC[İI]|MAL[İI] MÜŞAV[İI]R"),
        ("yapilandirma-varlik", r"YAPILANDIR|VARLIKLARIN|UZLAŞMA USULÜ|EKONOMİYE KAZANDIR"), ("gumruk", r"GÜMRÜK"),
        ("milli-emlak", r"M[İI]LL[İÎ] EML"), ("muhasebat", r"MUHASEBAT|MUHASEBE SİSTEMİ|HARCAMA YETK"),
        ("tesvik-arge", r"TEŞVİK|ARAŞTIRMA|GELİŞTİRME|SERBEST BÖLGE"), ("masak", r"MALİ SUÇLARI"),
        ("kamu-personeli", r"MEMURLAR|PERSONEL|HARCIRAH"), ("diger-vergiler", r"VERG[İI]|KONAKLAMA|DİJİTAL|DEĞERLİ")]

# Liste servisindeki tür adları
TUR = {"kanun": ("Kanun", 1), "tuzuk": ("Tuzuk", 2), "teblig": ("Teblig", 9),
       "cbk": ("CumhurbaskaniKararnameleri", 19), "cbkarar": ("CumhurbaskaniKararlari", 20),
       "genelge": ("CumhurbaskanligiGenelgeleri", 22)}
ETIKET = {"Kanun": "Kanun", "Tuzuk": "Tüzük", "Teblig": "Tebliğ", "CumhurbaskaniKararnameleri": "Cumhurbaşkanlığı Kararnamesi",
          "CumhurbaskaniKararlari": "Cumhurbaşkanı Kararı", "CumhurbaskanligiGenelgeleri": "Cumhurbaşkanlığı Genelgesi"}
MADDE_DOSYA = re.compile(r"^(madde-|ek-madde-|gecici-madde-|00-baslik\.txt$|zz-islenemeyen)")


def slug(s, n=60):
    s = s.translate(TR).lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:n].rstrip("-") or "adsiz"


def norm(s):
    return re.sub(r"\s+", "", s or "")


def aile(ad):
    u = ad.upper()
    for k, p in AILE:
        if re.search(p, u):
            return k
    return "diger"


def oturum():
    s = getattr(_yerel, "s", None)
    if s is None:
        s = requests.Session()
        s.headers["User-Agent"] = "Mozilla/5.0 (mevzuat arsivi guncelleme)"
        _yerel.s = s
    return s


def getir(url, ikili=False, deneme=3):
    son = None
    for i in range(deneme):
        try:
            r = oturum().get(url, timeout=90)
            if r.status_code == 200:
                return r.content if ikili else r.content.decode("utf-8", "replace")
            son = f"HTTP {r.status_code}"
            if r.status_code == 404:
                break
        except Exception as e:  # ağ hatası
            son = str(e)[:200]
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"{url}: {son}")


def liste(tur_ad):
    """Liste servisinden bir türün tüm kayıtları (100'lük sayfalar)."""
    out, bas, toplam = [], 0, None
    while True:
        p = {"MevzuatTur": tur_ad, "YonetmelikMevzuatTur": "OsmanliKanunu", "AranacakIfade": "", "AranacakYer": "2",
             "TamCumle": "true", "MevzuatNo": "", "BaslangicTarihi": ""}
        b = {"draw": 1, "columns": [], "order": [], "start": bas, "length": 100,
             "search": {"value": "", "regex": False}, "parameters": p}
        j, son = None, ""
        for i in range(6):
            try:
                s = requests.Session()
                s.headers["User-Agent"] = "Mozilla/5.0 (mevzuat arsivi guncelleme)"
                s.get(SITE + "/", timeout=60)
                r = s.post(SITE + "/Anasayfa/MevzuatDatatable", json=b, timeout=120)
                if r.status_code == 200:
                    j = r.json()
                    break
                son = f"HTTP {r.status_code} {r.text[:60]}"
            except Exception as e:
                son = str(e)[:120]
            time.sleep(5 * (i + 1))
        if j is None:
            raise RuntimeError(f"liste {tur_ad} başlangıç {bas}: {son}")
        veri = j.get("data") or []
        toplam = j.get("recordsTotal", 0)
        out += veri
        bas += len(veri)
        if not veri or bas >= toplam:
            if len(out) < toplam:
                raise RuntimeError(f"liste {tur_ad} eksik: {len(out)}/{toplam}")
            return out


def html_metin(html):
    """MevzuatFihristDetayIframe sayfasının metni (depodaki metinlerle boşluk hariç aynı yöntem)."""
    s = BeautifulSoup(html, "html.parser")
    for x in s(["script", "style", "head", "noscript", "title"]):
        x.decompose()
    t = s.get_text("")
    return re.sub(r"\n{3,}", "\n\n", t.replace("\r", "")).strip() + "\n"


def iframe_url(tur, no, tertip):
    return f"{SITE}/anasayfa/MevzuatFihristDetayIframe?MevzuatTur={tur}&MevzuatNo={no}&MevzuatTertip={tertip}"


def kaynak_url(tur, no, tertip):
    return f"{SITE}/mevzuat?MevzuatNo={no}&MevzuatTur={tur}&MevzuatTertip={tertip}"


def pdf_metin(veri):
    if not veri.startswith(b"%PDF"):
        raise RuntimeError("PDF değil")
    r = subprocess.run(["pdftotext", "-layout", "-", "-"], input=veri, capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def pdf_tarih(veri):
    r = subprocess.run(["pdfinfo", "-"], input=veri, capture_output=True)
    m = re.search(r"CreationDate:\s*(.+)", r.stdout.decode("utf-8", "replace"))
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------- envanter
def envanter():
    """Depodaki mevzuat.gov.tr kaynaklı kayıtlar."""
    htmls, pdfler = [], []
    kokler = ["kanunlar", "tuzukler", "tebligler", "yonetmelikler", "cumhurbaskanligi"]
    bas = re.compile(r"^KAYNAK: https://www\.mevzuat\.gov\.tr/mevzuat\?MevzuatNo=([^&\s]+)&MevzuatTur=(\d+)&MevzuatTertip=(\d+)")
    for k in kokler:
        for kok, dirs, files in os.walk(KOK / k):
            dirs[:] = [d for d in dirs if d not in ("ekler", "bolumler", "eski-gib-2026-04")]
            for f in files:
                p = pathlib.Path(kok) / f
                if f == "KAYNAK.md" and k == "kanunlar":
                    t = p.read_text(encoding="utf-8")
                    m1 = re.search(r"\| Kaynak \| https://www\.mevzuat\.gov\.tr/MevzuatMetin/1\.(\d+)\.(\d+)\.pdf", t)
                    m2 = re.search(r"\| Kaynak \| https://www\.mevzuat\.gov\.tr/mevzuat\?MevzuatNo=(\d+)&MevzuatTur=([01])&MevzuatTertip=(\d+)", t)
                    mp = re.search(r"\| PDF(?: dosyası)? \| `([^`]+\.pdf)`", t)
                    if (m1 or m2) and mp:
                        tur, tertip, no = ("1", m1.group(1), m1.group(2)) if m1 else (m2.group(2), m2.group(3), m2.group(1))
                        pdfler.append({"dir": p.parent, "no": no, "tur": tur, "tertip": tertip, "pdf": KOK / mp.group(1)})
                elif f.endswith(".txt") and not MADDE_DOSYA.match(f):
                    with p.open(encoding="utf-8", errors="replace") as fh:
                        m = bas.match(fh.readline())
                    if m:
                        htmls.append({"yol": p, "no": m.group(1), "tur": int(m.group(2)), "tertip": m.group(3)})
    return htmls, pdfler


# ---------------------------------------------------------------- güncelleme
def ayir(metin):
    """Başlık satırları ve gövde (ilk boş satıra kadar başlık)."""
    if "\n\n" in metin:
        b, g = metin.split("\n\n", 1)
    else:
        b, g = metin, ""
    return b.split("\n"), g


def html_kontrol(k, kuru):
    eski = k["yol"].read_text(encoding="utf-8", errors="replace")
    bas, govde = ayir(eski)
    yeni = html_metin(getir(iframe_url(k["tur"], k["no"], k["tertip"])))
    if norm(yeni) == norm(govde):
        return None
    if len(norm(yeni)) < 100:
        raise RuntimeError("sayfadan metin alınamadı")
    oran = len(norm(yeni)) / max(1, len(norm(govde)))
    if oran < 0.5:
        raise RuntimeError(f"yeni metin eskisinin %{oran*100:.0f}'i kadar; şüpheli, yazılmadı")
    if not kuru:
        bas = [l for l in bas if not l.startswith("ALINMA:")]
        bas.append(f"ALINMA: {BUGUN_TR} (mevzuat.gov.tr güncel metni)")
        k["yol"].write_text("\n".join(bas) + "\n\n" + yeni, encoding="utf-8")
    return {"yol": k["yol"].relative_to(KOK).as_posix(), "fark": len(norm(yeni)) - len(norm(govde))}


def kanun_bol(d):
    for f in d.iterdir():
        if f.is_file() and MADDE_DOSYA.match(f.name):
            f.unlink()
    r = subprocess.run([sys.executable, str(KOK / "araclar" / "bol.py"), str(d / "tam-metin.txt"), str(d)],
                       capture_output=True, text=True)
    tamam = r.returncode == 0 and '"butunluk": true' in r.stdout
    if not tamam:
        for f in d.iterdir():
            if f.is_file() and MADDE_DOSYA.match(f.name):
                f.unlink()
    a = d / "ANALIZ.md"
    if tamam and a.exists():
        m = re.match(r"# (.+?) — yapısal analiz", a.read_text(encoding="utf-8"))
        if m:
            subprocess.run([sys.executable, str(KOK / "araclar" / "analiz.py"), str(d), m.group(1)], capture_output=True)
    return tamam, r.stdout.strip()[:3000]


def pdf_kontrol(k, kuru):
    d = k["dir"]
    tm = d / "tam-metin.txt"
    eski = tm.read_text(encoding="utf-8", errors="replace") if tm.exists() else ""
    veri = getir(f"{SITE}/MevzuatMetin/{k['tur']}.{k['tertip']}.{k['no']}.pdf", ikili=True)
    yeni = pdf_metin(veri)
    if len(norm(yeni)) < 200:
        raise RuntimeError("PDF'ten metin alınamadı")
    if norm(yeni) == norm(eski):
        return None
    oran = len(norm(yeni)) / max(1, len(norm(eski)))
    if oran < 0.5:
        raise RuntimeError(f"yeni metin eskisinin %{oran*100:.0f}'i kadar; şüpheli, yazılmadı")
    bilgi = {"yol": d.relative_to(KOK).as_posix(), "fark": len(norm(yeni)) - len(norm(eski))}
    if kuru:
        return bilgi
    k["pdf"].parent.mkdir(parents=True, exist_ok=True)
    k["pdf"].write_bytes(veri)
    tm.write_text(yeni, encoding="utf-8")
    kaynak = d / "KAYNAK.md"
    t = kaynak.read_text(encoding="utf-8")
    sha = hashlib.sha256(veri).hexdigest()
    t = re.sub(r"(\| SHA-256 \| `)[0-9a-f]+(`)", rf"\g<1>{sha}\g<2>", t)
    t = re.sub(r"(\| İndirme tarihi \| )[^|]+", rf"\g<1>{BUGUN_TR} ", t)
    t = re.sub(r"(\| Alınma \| )[^|]+", rf"\g<1>{BUGUN_TR} (mevzuat.gov.tr güncel metni) ", t)
    t = re.sub(r"(\| PDF'in mevzuat\.gov\.tr'deki oluşturulma tarihi \| )[^|]+", rf"\g<1>{pdf_tarih(veri)} ", t)
    if (d / "00-baslik.txt").exists() or any(MADDE_DOSYA.match(f.name) for f in d.iterdir()):
        tamam, cikti = kanun_bol(d)
        bilgi["bolme"] = "bölündü" if tamam else "BÖLÜNEMEDİ (yalnızca tam metin)"
        t = re.sub(r"(\| Madde bölme \| )[^|]+", rf"\g<1>{'bölündü' if tamam else 'yalnızca tam metin'} ", t)
    kaynak.write_text(t, encoding="utf-8")
    return bilgi


# ---------------------------------------------------------------- yeni kayıtlar
def baslik_satirlari(kayit, tur_ad, kaynak):
    return (f"KAYNAK: {kaynak}\nADI: {kayit.get('mevAdi','').strip()}\nTÜR: {tur_ad}\n"
            f"RESMÎ GAZETE: {kayit.get('resmiGazeteTarihi') or ''} / {kayit.get('resmiGazeteSayisi') or ''}\n"
            f"ALINMA: {BUGUN_TR} (mevzuat.gov.tr güncel metni)\n\n")


def yeni_html(kayit, hedef, tur_ad):
    no, tur, tertip = kayit["mevzuatNo"], kayit["mevzuatTur"], kayit["mevzuatTertip"]
    metin = html_metin(getir(iframe_url(tur, no, tertip)))
    if len(norm(metin)) < 100:
        raise RuntimeError("sayfadan metin alınamadı")
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(baslik_satirlari(kayit, tur_ad, kaynak_url(tur, no, tertip)) + metin, encoding="utf-8")
    return hedef.relative_to(KOK).as_posix()


def yeni_pdf_metin(kayit, hedef, tur_ad):
    url = kayit.get("url") or ""
    if not url.startswith("http"):
        url = f"{SITE}/MevzuatMetin/{kayit['mevzuatTur']}.{kayit['mevzuatTertip']}.{kayit['mevzuatNo']}.pdf"
    veri = getir(url, ikili=True)
    metin = pdf_metin(veri)
    not_ = "" if len(norm(metin)) >= 100 else "METİN ÇIKARILAMADI (PDF taranmış görüntü olabilir; kaynak PDF'e bakınız)\n"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(baslik_satirlari(kayit, tur_ad, url) + f"PDF SHA-256: {hashlib.sha256(veri).hexdigest()}\n\n" + not_ + metin,
                     encoding="utf-8")
    return hedef.relative_to(KOK).as_posix(), bool(not_)


def yeni_kanun(kayit):
    no, tertip, ad = kayit["mevzuatNo"], kayit["mevzuatTertip"], kayit["mevAdi"].strip()
    tur = kayit.get("mevzuatTur", 1)
    d = KOK / "kanunlar" / "tum" / f"{slug(no, 10)}-{slug(ad, 60)}"
    d.mkdir(parents=True, exist_ok=True)
    try:
        veri = getir(f"{SITE}/MevzuatMetin/{tur}.{tertip}.{no}.pdf", ikili=True)
        metin = pdf_metin(veri)
    except Exception:
        veri, metin = None, ""
    if veri and len(norm(metin)) >= 200:
        pdf = KOK / "kaynak-dosyalar" / "kanun-pdf" / f"{tur}.{tertip}.{no}.pdf"
        pdf.parent.mkdir(parents=True, exist_ok=True)
        pdf.write_bytes(veri)
        (d / "tam-metin.txt").write_text(metin, encoding="utf-8")
        tamam, cikti = kanun_bol(d)
        info = (f"| PDF | `{pdf.relative_to(KOK).as_posix()}` |\n| SHA-256 | `{hashlib.sha256(veri).hexdigest()}` |\n"
                f"| Madde bölme | {'bölündü' if tamam else 'yalnızca tam metin'} |\n")
        if cikti:
            info += "\nBölme betiği çıktısı:\n\n```\n" + cikti + "\n```\n"
    else:
        yeni_html(kayit, d / "tam-metin.txt", "Kanunlar")
        info = "| PDF | mevzuat.gov.tr'de PDF yok; HTML metin alındı |\n"
    (d / "KAYNAK.md").write_text(
        f"# {ad}\n\n| | |\n|---|---|\n| Kanun No | {no} |\n| Kaynak | {kaynak_url(tur, no, tertip)} |\n"
        f"| Resmî Gazete | {kayit.get('resmiGazeteTarihi','')} / {kayit.get('resmiGazeteSayisi','')} |\n"
        f"| Kabul | {kayit.get('kabulTarih') or ''} |\n| Alınma | {BUGUN_TR} (mevzuat.gov.tr güncel metni) |\n{info}\n"
        "Metin otomatik çıkarıldı; insan gözüyle resmî metinle karşılaştırılmadı. Kullanmadan önce mevzuat.gov.tr ile teyit ediniz.\n",
        encoding="utf-8")
    return d.relative_to(KOK).as_posix()


def yil(kayit):
    t = (kayit.get("resmiGazeteTarihi") or "").strip()
    m = re.match(r"\d{1,2}[./]\d{1,2}[./]((?:19|20)\d\d)$", t)
    return m.group(1) if m else "tarihsiz"


def hedef_yol(anahtar, kayit):
    no, ad = str(kayit["mevzuatNo"]), kayit["mevAdi"].strip()
    if anahtar == "tuzuk":
        return KOK / "tuzukler" / f"{slug(no, 20)}-{slug(ad)}" / "tam-metin.txt"
    if anahtar == "teblig":
        return KOK / "tebligler" / "genel-tebligler" / aile(ad) / f"{slug(no, 20)}-{slug(ad, 70)}.txt"
    if anahtar == "cbk":
        return KOK / "cumhurbaskanligi" / "kararnameler" / f"{slug(no, 10)}-{slug(ad, 70)}.txt"
    if anahtar == "cbkarar":
        return KOK / "cumhurbaskanligi" / "kararlar" / yil(kayit) / f"{slug(no, 12)}-{slug(ad, 70)}.txt"
    if anahtar == "genelge":
        return KOK / "cumhurbaskanligi" / "genelgeler" / yil(kayit) / f"{slug(no, 12)}-{slug(ad, 70)}.txt"
    raise ValueError(anahtar)


def pdf_kayit_envanteri(klasor):
    """PDF'ten metne çevrilen CB kararı/genelgesi dosyalarının KAYNAK adresleri."""
    out = {}
    for p in (KOK / "cumhurbaskanligi" / klasor).rglob("*.txt"):
        with p.open(encoding="utf-8", errors="replace") as fh:
            ilk = fh.readline()
        if ilk.startswith("KAYNAK: "):
            out[ilk[8:].strip()] = p
    return out


# ---------------------------------------------------------------- dizinler
def cb_readme(listeler):
    d = KOK / "cumhurbaskanligi"
    d.mkdir(exist_ok=True)
    say = {k: len(list((d / k).rglob("*.txt"))) if (d / k).exists() else 0 for k in ("kararnameler", "kararlar", "genelgeler")}
    satir = ["# Cumhurbaşkanlığı mevzuatı (mevzuat.gov.tr)", "",
             "Kaynak: mevzuat.gov.tr. Dosyalar `araclar/mevzuat/mevzuat_tara.py` ile otomatik alınır ve güncellenir.",
             "Her dosyanın başında kaynak adresi, Resmî Gazete bilgisi ve alınma tarihi yazar. Metinler otomatik çıkarılmıştır;",
             "kullanmadan önce resmî metinle teyit ediniz.", "",
             "| Klasör | İçerik | Dosya |", "|---|---|---|",
             f"| `kararnameler/` | Cumhurbaşkanlığı Kararnameleri, işlenmiş güncel metin (her gün değişiklik kontrolü) | {say['kararnameler']} |",
             f"| `kararlar/<yıl>/` | Cumhurbaşkanı Kararları, PDF'ten çıkarılan metin (yeni kararlar her gün, değişiklik kontrolü haftalık) | {say['kararlar']} |",
             f"| `genelgeler/<yıl>/` | Cumhurbaşkanlığı Genelgeleri, PDF'ten çıkarılan metin | {say['genelgeler']} |", ""]
    if "cbkarar" in listeler:
        satir += ["## Cumhurbaşkanı Kararları dizini (en yeni önce)", "", "| RG tarihi | Sayı | Karar | Dosya |", "|---|---|---|---|"]
        env = pdf_kayit_envanteri("kararlar")
        for k in listeler["cbkarar"]:
            url = k.get("url") or ""
            p = env.get(url)
            if p:
                satir.append(f"| {k.get('resmiGazeteTarihi','')} | {k['mevzuatNo']} | {k['mevAdi'].strip().replace('|','/')[:160]} | "
                             f"`{p.relative_to(d).as_posix()}` |")
    (d / "README.md").write_text("\n".join(satir) + "\n", encoding="utf-8")


def teblig_readme():
    d = KOK / "tebligler" / "genel-tebligler"
    r = d / "README.md"
    if not r.exists():
        return
    say = sorted(((p.name, len(list(p.glob("*.txt")))) for p in d.iterdir() if p.is_dir()), key=lambda x: -x[1])
    t = r.read_text(encoding="utf-8")
    tablo = "| Klasör | Adet |\n|---|---|\n" + "".join(f"| `{a}/` | {n} |\n" for a, n in say if n)
    t = re.sub(r"\| Klasör \| Adet \|\n\|---\|---\|\n(?:\|.*\|\n)+", tablo, t)
    t = re.sub(r"tebliğler \((\d+)\)", f"tebliğler ({sum(n for _, n in say)})", t, count=1)
    r.write_text(t, encoding="utf-8")


def readme_ekle(dosya, satir):
    if dosya.exists():
        with dosya.open("a", encoding="utf-8") as fh:
            fh.write(satir + "\n")


# ---------------------------------------------------------------- ana akış
def paralel(fonk, isler, n=6):
    sonuc, hata = [], []

    def sar(x):
        try:
            return ("ok", x, fonk(x))
        except Exception as e:
            return ("hata", x, str(e)[:300])
    with cf.ThreadPoolExecutor(n) as ex:
        for i, (durum, x, r) in enumerate(ex.map(sar, isler), 1):
            (sonuc if durum == "ok" else hata).append((x, r))
            if i % 200 == 0:
                print(f"  {i}/{len(isler)}", file=sys.stderr, flush=True)
    return sonuc, hata


def calistir(kip, kuru, sinir):
    rapor = {"tarih": BUGUN_TR, "kip": kip, "kuru": kuru, "degisen": [], "yeni": [], "hata": [], "listede_yok": [],
             "metinsiz": []}
    htmls, pdfler = envanter()
    print(f"envanter: {len(htmls)} metin dosyası, {len(pdfler)} PDF kaynaklı kanun", file=sys.stderr, flush=True)

    # 1) değişiklik kontrolü
    ok, hata = paralel(lambda k: pdf_kontrol(k, kuru), pdfler)
    rapor["degisen"] += [dict(r, tur="Kanun") for _, r in ok if r]
    rapor["hata"] += [{"yol": k["dir"].relative_to(KOK).as_posix(), "hata": e} for k, e in hata]
    ok, hata = paralel(lambda k: html_kontrol(k, kuru), htmls)
    rapor["degisen"] += [dict(r, tur="Metin") for _, r in ok if r]
    rapor["hata"] += [{"yol": k["yol"].relative_to(KOK).as_posix(), "hata": e} for k, e in hata]

    # 2) yeni kayıtlar
    var_html = {(k["tur"], str(k["no"]), str(k["tertip"])) for k in htmls}
    var_kanun = {(k["no"], k["tertip"]) for k in pdfler} | {(n, t) for (tu, n, t) in var_html if tu == 1}
    listeler = {}
    for anahtar, (tur_ad, tur_no) in TUR.items():
        try:
            listeler[anahtar] = liste(tur_ad)
        except Exception as e:
            rapor["hata"].append({"yol": f"liste:{tur_ad}", "hata": str(e)[:300]})
            continue
        lst = listeler[anahtar]
        if anahtar == "teblig":
            lst = [k for k in lst if "GENEL TEBLİĞ" in k["mevAdi"].upper()]
        if anahtar == "kanun":
            yeniler = [k for k in lst if (str(k["mevzuatNo"]), str(k["mevzuatTertip"])) not in var_kanun]
        elif anahtar in ("cbkarar", "genelge"):
            env = pdf_kayit_envanteri("kararlar" if anahtar == "cbkarar" else "genelgeler")
            yeniler = [k for k in lst if (k.get("url") or "") not in env]
        else:
            yeniler = [k for k in lst if (int(k["mevzuatTur"]), str(k["mevzuatNo"]), str(k["mevzuatTertip"])) not in var_html]
        # listeden çıkanlar
        if anahtar in ("kanun", "tuzuk", "teblig", "cbk"):
            listede = {(str(k["mevzuatNo"]), str(k["mevzuatTertip"])) for k in lst}
            if anahtar == "kanun":
                eksik = [k for k in pdfler if (k["no"], k["tertip"]) not in listede]
                rapor["listede_yok"] += [k["dir"].relative_to(KOK).as_posix() for k in eksik]
            else:
                turler = {int(k["mevzuatTur"]) for k in lst} | {tur_no}
                eksik = [k for k in htmls if k["tur"] in turler and (str(k["no"]), str(k["tertip"])) not in listede]
                if anahtar == "teblig":  # yalnızca genel tebliğ klasöründekiler takip edilir
                    eksik = [k for k in eksik if "genel-tebligler" in k["yol"].parts]
                rapor["listede_yok"] += [k["yol"].relative_to(KOK).as_posix() for k in eksik]
        if sinir:
            yeniler = yeniler[:sinir]
        print(f"{tur_ad}: listede {len(lst)}, yeni {len(yeniler)}", file=sys.stderr, flush=True)
        if kuru or not yeniler:
            rapor["yeni"] += [{"tur": ETIKET[tur_ad], "no": k["mevzuatNo"], "ad": k["mevAdi"].strip(), "rg": k.get("resmiGazeteTarihi"),
                               "yol": "(kuru çalıştırma)"} for k in yeniler] if kuru else []
            continue

        def ekle(k, anahtar=anahtar, tur_ad=ETIKET[tur_ad]):
            if anahtar == "kanun":
                return yeni_kanun(k), False
            if anahtar in ("tuzuk", "teblig", "cbk"):
                return yeni_html(k, hedef_yol(anahtar, k), tur_ad), False
            return yeni_pdf_metin(k, hedef_yol(anahtar, k), tur_ad)
        ok, hata = paralel(ekle, yeniler, n=8 if anahtar == "cbkarar" else 6)
        for k, (yol, metinsiz) in ok:
            rapor["yeni"].append({"tur": ETIKET[tur_ad], "no": k["mevzuatNo"], "ad": k["mevAdi"].strip(), "rg": k.get("resmiGazeteTarihi"), "yol": yol})
            if metinsiz:
                rapor["metinsiz"].append(yol)
            if anahtar == "tuzuk":
                readme_ekle(KOK / "tuzukler" / "README.md",
                            f"| `{pathlib.Path(yol).parent.name}/` | {k['mevAdi'].strip()} | {k.get('resmiGazeteTarihi','')} |  |")
            if anahtar == "kanun":
                readme_ekle(KOK / "kanunlar" / "tum" / "README.md",
                            f"| `{pathlib.Path(yol).name}/` | {k['mevAdi'].strip()} | {k.get('resmiGazeteTarihi','')} | yeni ({BUGUN_TR}) |")
        rapor["hata"] += [{"yol": f"yeni:{tur_ad}:{k['mevzuatNo']}", "hata": e} for k, e in hata]

    # 3) haftalık: CB kararlarının değişiklik kontrolü (PDF metni)
    if kip == "haftalik" and "cbkarar" in listeler:
        env = pdf_kayit_envanteri("kararlar")

        def cb_kontrol(k):
            p = env.get(k.get("url") or "")
            if not p:
                return None
            veri = getir(k["url"], ikili=True)
            yeni = pdf_metin(veri)
            bas, govde = ayir(p.read_text(encoding="utf-8", errors="replace"))
            govde = govde.split("\n\n", 1)[1] if govde.startswith("PDF SHA-256:") and "\n\n" in govde else govde
            if len(norm(yeni)) < 100 or norm(yeni) == norm(govde.replace("METİN ÇIKARILAMADI", "")):
                return None
            if not kuru:
                yeni_pdf_metin(k, p, "Cumhurbaşkanı Kararı")
            return {"yol": p.relative_to(KOK).as_posix(), "fark": len(norm(yeni)) - len(norm(govde))}
        ok, hata = paralel(cb_kontrol, listeler["cbkarar"], n=4)
        rapor["degisen"] += [dict(r, tur="CB Kararı") for _, r in ok if r]
        rapor["hata"] += [{"yol": f"cbkarar:{k['mevzuatNo']}", "hata": e} for k, e in hata]

    if not kuru:
        if any(x["tur"].startswith("Cumhurbaşkan") for x in rapor["yeni"]) or not (KOK / "cumhurbaskanligi" / "README.md").exists():
            cb_readme(listeler)
        if any(x["tur"] == "Tebliğ" for x in rapor["yeni"]):
            teblig_readme()
        gunluk(rapor)
        durum = KOK / "araclar" / "mevzuat" / "_durum.json"
        durum.write_text(json.dumps({"son_tarama": datetime.datetime.now().isoformat(timespec="seconds"), "kip": kip,
                                     "degisen": len(rapor["degisen"]), "yeni": len(rapor["yeni"]), "hata": len(rapor["hata"])},
                                    ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return rapor


def gunluk(rapor):
    if not (rapor["degisen"] or rapor["yeni"]):  # yalnızca "listede_yok" varsa her gün tekrar yazılmaz
        return
    g = KOK / "GUNLUK-mevzuat.md"
    eski = g.read_text(encoding="utf-8") if g.exists() else (
        "# mevzuat.gov.tr güncelleme günlüğü\n\n`araclar/mevzuat/mevzuat_tara.py` her çalıştığında değişen ve yeni eklenen kayıtları buraya yazar (en yeni üstte).\n\n")
    ust, alt = (eski.split("\n## ", 1) + [""])[:2]
    s = [f"## {rapor['tarih']} ({rapor['kip']})", ""]
    if rapor["degisen"]:
        s += [f"**Değişen ({len(rapor['degisen'])})**", ""] + [f"- `{x['yol']}` ({x['tur']}, {x['fark']:+d} karakter{', ' + x['bolme'] if x.get('bolme') else ''})" for x in rapor["degisen"]] + [""]
    if rapor["yeni"]:
        yeni = rapor["yeni"]
        s += [f"**Yeni ({len(yeni)})**", ""]
        if len(yeni) > 60:
            from collections import Counter
            s += [f"- {t}: {n}" for t, n in Counter(x["tur"] for x in yeni).items()] + [""]
        else:
            s += [f"- {x['tur']} {x['no']} — {x['ad']} (RG {x['rg']}) → `{x['yol']}`" for x in yeni] + [""]
    if rapor["listede_yok"]:
        s += [f"**mevzuat.gov.tr listesinde artık görünmeyenler ({len(rapor['listede_yok'])}, silinmedi; mülga olabilir)**", ""] + \
             [f"- `{y}`" for y in rapor["listede_yok"][:100]] + [""]
    g.write_text(ust.rstrip() + "\n\n" + "\n".join(s) + ("\n## " + alt if alt else ""), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kip", choices=["guncelle", "haftalik"])
    ap.add_argument("--kuru", action="store_true", help="hiçbir dosyaya yazma, yalnızca raporla")
    ap.add_argument("--sinir", type=int, default=0, help="tür başına en çok N yeni kayıt (deneme için)")
    a = ap.parse_args()
    r = calistir(a.kip, a.kuru, a.sinir)
    ozet = dict(r)
    ozet["yeni_sayi"] = len(r["yeni"])
    if len(r["yeni"]) > 80:
        from collections import Counter
        ozet["yeni"] = [x for x in r["yeni"] if x["tur"] != "Cumhurbaşkanı Kararı"][:80]
        ozet["yeni_cb_kararlari"] = [f"{x['no']} — {x['ad'][:150]} (RG {x['rg']})" for x in r["yeni"] if x["tur"] == "Cumhurbaşkanı Kararı"][:300]
        ozet["yeni_turlere_gore"] = dict(Counter(x["tur"] for x in r["yeni"]))
    print(json.dumps(ozet, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
