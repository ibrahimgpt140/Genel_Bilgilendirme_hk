#!/usr/bin/env python3
"""GİB mevzuat taraması (gib.gov.tr portalı).

Kaynak: https://gib.gov.tr/api/gibportal/mevzuat/<tur>/list  (portalın kendi API'si)
Her kayıt gib/<klasor>/<id>-<baslik>.md olarak yazılır (künye + tam metin).

Kullanım:
  python3 araclar/gib/gib_tara.py tam [--ozelge-baslangic 2025-09-01]
      Tüm türleri baştan çeker. Özelgeler yalnızca verilen tarihten itibaren.
  python3 araclar/gib/gib_tara.py guncelle
      Tümünü yeniden tarar (API güncellenme tarihine göre sıralamaya izin
      vermiyor), yalnızca yeni/değişen dosyaları yazar ve gib/GUNLUK.md'ye ekler.
      Daha eski özelgeler için: guncelle --ozelge-baslangic 2024-01-01
"""
import argparse, json, os, re, sys, time, urllib.request, html as htmlmod
from datetime import datetime, timezone

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("pip install beautifulsoup4")

API = "https://gib.gov.tr/api/gibportal/mevzuat/{}/list"
KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gib")

# tur (API) -> (klasör, Türkçe ad, tarih alanı, sayı alanı)
TURLER = {
    "teblig":        ("tebligler",      "Tebliğ",               "resmiGazeteTarih", "resmiGazeteSayi"),
    "sirkuler":      ("sirkuler",       "Sirküler",             "sirkulerTarih",    "sirkulerNo"),
    "ozelge":        ("ozelgeler",      "Özelge",               "ozelgeTarih",      "ozelgeNo"),
    "icGenelge":     ("ic-genelgeler",  "İç Genelge",           "tarih",            "sayi"),
    "genelYazilar":  ("genel-yazilar",  "Genel Yazı",           "tarih",            "sayi"),
    "yonetmelikler": ("yonetmelikler",  "Yönetmelik",           "resmiGazeteTarih", "resmiGazeteSayi"),
    "bkk":           ("bkk",            "Bakanlar Kurulu Kararı","resmiGazeteTarih", "no"),
    "cbk":           ("cbk",            "Cumhurbaşkanı Kararı", "resmiGazeteTarih", "no"),
    "gerekce":       ("gerekceler",     "Kanun Gerekçesi",      None,               None),
    "kkdf":          ("kkdf",           "KKDF",                 "timeCreatedAt",    None),
    "taslak":        ("taslaklar",      "Taslak",               "timePublishedAt",  None),
    "uluslararasi-anlasma": ("uluslararasi", "Uluslararası Anlaşma", "creationDate", None),
}
TR = str.maketrans("çğıöşüÇĞİÖŞÜâîû", "cgiosuCGIOSUaiu")


def istek(tur, sayfa, boyut, sirala, yon="DESC"):
    url = f"{API.format(tur)}?page={sayfa}&size={boyut}&sortFieldName={sirala}&sortType={yon}"
    govde = json.dumps({"status": 2, "deleted": False}).encode()
    for deneme in range(5):
        try:
            r = urllib.request.Request(url, data=govde, method="POST",
                                       headers={"Content-Type": "application/json",
                                                "User-Agent": "Mozilla/5.0 ymm-mevzuat-bankasi"})
            with urllib.request.urlopen(r, timeout=120) as y:
                return json.load(y)["resultContainer"]
        except Exception as e:
            print(f"  ! {tur} s{sayfa}: {e}; tekrar", file=sys.stderr)
            time.sleep(3 * (deneme + 1))
    raise RuntimeError(f"{tur} sayfa {sayfa} alınamadı")


def slug(s, n=70):
    s = re.sub(r"<[^>]+>", " ", s or "").translate(TR).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:n].rstrip("-") or "kayit"


def metne(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    for im in soup.find_all("img", src=True):  # taranmış belge/tablo görselleri kaybolmasın
        im.replace_with(f"\n[Görsel: <{im['src']}>]\n")
    for a in soup.find_all("a", href=True):
        a.replace_with(f"{a.get_text(' ', strip=True)} <{a['href']}>")
    for tr in soup.find_all("tr"):
        hucre = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"], recursive=False)]
        tr.replace_with(" | ".join(h for h in hucre if h) + "\n")
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for p in soup.find_all(["p", "div", "li", "h1", "h2", "h3", "h4"]):
        p.append("\n")
    t = htmlmod.unescape(soup.get_text())
    t = re.sub(r"[ \t\xa0]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def tarih(k, alan):
    v = k.get(alan) if alan else None
    return (v or "")[:10]


def yaz(tur, k):
    klasor, ad, ta, sa = TURLER[tur]
    d = os.path.join(KOK, klasor)
    os.makedirs(d, exist_ok=True)
    yol = os.path.join(d, f"{k['id']}-{slug(k.get('title'))}.md")
    for eski in os.listdir(d):  # başlık değiştiyse eski dosyayı kaldır
        if eski.startswith(f"{k['id']}-") and os.path.join(d, eski) != yol:
            os.remove(os.path.join(d, eski))
    baslik = re.sub(r"<[^>]+>", " ", k.get("title") or "").strip()
    maddeler = [re.sub(r"<[^>]+>", " ", m.get("title") or "").strip() for m in (k.get("maddeList") or [])]
    dosyalar = k.get("fileNames") or []
    satir = [
        "---",
        f"tur: {ad}",
        f"gib_id: {k['id']}",
        f"baslik: {json.dumps(baslik, ensure_ascii=False)}",
        f"tarih: {tarih(k, ta)}",
        f"sayi: {json.dumps(str(k.get(sa) or '') if sa else '', ensure_ascii=False)}",
        f"kanun: {json.dumps(((k.get('kanunNo') or '') + ' ' + (k.get('kanunTitle') or '')).strip(), ensure_ascii=False)}",
        f"kaynak: {k.get('siteLink') or k.get('link') or ''}",
        f"gib_guncelleme: {(k.get('updated_at') or '')[:19]}",
        f"alindi: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "---", "", f"# {baslik}", "",
    ]
    if maddeler:
        satir += ["**İlgili maddeler:** " + "; ".join(maddeler), ""]
    if dosyalar:
        satir += ["**Ekler:** " + ", ".join(
            f"<https://cdn.gib.gov.tr/api/gibportal-file/file/getFile?objectKey={f}>" for f in dosyalar), ""]
    satir += [metne(k.get("description")) or "_(Metin GİB portalında yok; kaynak bağlantısına veya eklere bakınız.)_", ""]
    yeni = "\n".join(satir)
    if os.path.exists(yol):
        eski = open(yol, encoding="utf-8").read()
        if re.sub(r"\nalindi: .*", "", eski) == re.sub(r"\nalindi: .*", "", yeni):
            return yol, False
    open(yol, "w", encoding="utf-8").write(yeni)
    return yol, True


def dizin_yaz():
    toplam = []
    for tur, (klasor, ad, *_ ) in TURLER.items():
        d = os.path.join(KOK, klasor)
        if not os.path.isdir(d):
            continue
        kayit = []
        for f in os.listdir(d):
            if not f.endswith(".md") or f == "README.md":
                continue
            bas = open(os.path.join(d, f), encoding="utf-8").read(3000)
            g = lambda a: (re.search(rf"\n{a}: (.*)", bas) or [None, ""])[1].strip().strip('"')
            kayit.append((g("tarih"), g("sayi"), g("kanun"), g("baslik"), f))
        kayit.sort(key=lambda x: x[0], reverse=True)
        with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as o:
            o.write(f"# GİB {ad} dizini ({len(kayit)} kayıt)\n\nKaynak: gib.gov.tr mevzuat. En yeni üstte.\n\n"
                    "| Tarih | Sayı | Kanun | Başlık |\n|---|---|---|---|\n")
            for t, s, kn, b, f in kayit:
                b = b.replace("|", "/")
                o.write(f"| {t} | {s.replace('|','/')} | {kn} | [{b}]({f}) |\n")
        toplam.append((ad, klasor, len(kayit)))
    return toplam


def durum_oku():
    p = os.path.join(KOK, "_durum.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def durum_yaz(d):
    os.makedirs(KOK, exist_ok=True)
    json.dump(d, open(os.path.join(KOK, "_durum.json"), "w"), ensure_ascii=False, indent=1)


def tara(ozelge_bas):
    """Tüm türleri çeker; yalnızca yeni/değişen dosyaları yazar ve listesini döndürür."""
    degisen = []
    for tur, (_, ad, ta, _) in TURLER.items():
        sirala = ta if tur == "ozelge" else "id"
        sayfa, n = 0, 0
        while True:
            rc = istek(tur, sayfa, 500, sirala)
            dur = False
            for k in rc.get("content") or []:
                if tur == "ozelge" and tarih(k, ta) and tarih(k, ta) < ozelge_bas:
                    dur = True
                    break
                yol, d = yaz(tur, k)
                n += 1
                if d:
                    degisen.append((ad, tarih(k, ta), re.sub(r"<[^>]+>", " ", k.get("title") or "").strip(),
                                    os.path.relpath(yol, KOK)))
            print(f"{ad}: sayfa {sayfa+1}/{rc.get('totalPages')} -> {n}", flush=True)
            sayfa += 1
            if dur or sayfa >= (rc.get("totalPages") or 0):
                break
    return degisen


def calistir(ozelge_bas, gunluk):
    durum = durum_oku()
    ozelge_bas = ozelge_bas or durum.get("ozelge_baslangic", "2025-09-01")
    degisen = tara(ozelge_bas)
    simdi = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    durum.update(son_tarama=simdi, ozelge_baslangic=min(ozelge_bas, durum.get("ozelge_baslangic", ozelge_bas)))
    durum_yaz(durum)
    dizin_yaz()
    if gunluk and degisen:
        g = os.path.join(KOK, "GUNLUK.md")
        eski = open(g, encoding="utf-8").read() if os.path.exists(g) else "# GİB mevzuat değişiklik günlüğü\n"
        bas, _, govde = eski.partition("\n")
        blok = f"\n## {simdi[:10]} taraması ({len(degisen)} yeni/güncellenen)\n\n" + "".join(
            f"- **{a}** {t} — [{b}]({y})\n" for a, t, b, y in degisen)
        open(g, "w", encoding="utf-8").write(bas + "\n" + blok + govde)
    print(json.dumps({"degisen": len(degisen), "liste": degisen[:50]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("kip", choices=["tam", "guncelle", "dizin"])
    ap.add_argument("--ozelge-baslangic", default=None)
    a = ap.parse_args()
    if a.kip in ("tam", "guncelle"):
        calistir(a.ozelge_baslangic, gunluk=(a.kip == "guncelle"))
    else:
        print(dizin_yaz())
