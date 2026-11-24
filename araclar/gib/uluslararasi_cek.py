#!/usr/bin/env python3
"""GİB uluslararası mevzuat (ÇVÖA, bilgi değişimi, AB, diğer anlaşmalar) dosyalarını indirir.

Başlangıç: gib/uluslararasi/*.md içindeki cdn.gib.gov.tr bağlantıları (GİB portalının
uluslararası mevzuat sayfaları). HTML alt sayfalar (ör. ÇVÖA Türkçe metinleri, özelge
listesi) izlenir ve içlerindeki cdn.gib.gov.tr dosyaları da alınır (en fazla 3 seviye).
Yalnızca cdn.gib.gov.tr / gib.gov.tr adresleri indirilir; diğer siteler (OECD vb.)
yalnızca bağlantı olarak listelenir.

Çıktı: gib/uluslararasi/dosyalar/<objectKey yolu>  (özgün dosya)
       gib/uluslararasi/dosyalar/<objectKey yolu>.md (metin; PDF için pdftotext)
       gib/uluslararasi/cvoa/README.md, ozelgeler.md, tebligler.md (dizinler)

Kullanım: python3 araclar/gib/uluslararasi_cek.py
"""
import hashlib, html as htmlmod, json, os, re, subprocess, sys, time, urllib.parse, urllib.request
from bs4 import BeautifulSoup

KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gib", "uluslararasi")
HEDEF = os.path.join(KOK, "dosyalar")
UZANTI = (".pdf", ".htm", ".html", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar")


def resmi(u):
    h = urllib.parse.urlparse(u).hostname or ""
    return h == "gib.gov.tr" or h.endswith(".gib.gov.tr")


def anahtar(u):
    q = urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
    k = (q.get("objectKey") or [None])[0]
    return k or urllib.parse.urlparse(u).path.lstrip("/")


def getir(u):
    for d in range(4):
        try:
            r = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 ymm-mevzuat-bankasi"})
            with urllib.request.urlopen(r, timeout=120) as y:
                return y.read(), y.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return None, f"HTTP {e.code}"
            time.sleep(3 * (d + 1))
        except Exception:
            time.sleep(3 * (d + 1))
    return None, "erişilemedi"


def coz(b):
    for enc in ("utf-8-sig", "windows-1254", "iso-8859-9"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            pass
    return b.decode("utf-8", "replace")


def html_metin(s, taban):
    soup = BeautifulSoup(s, "html.parser")
    for x in soup(["script", "style"]):
        x.decompose()
    for a in soup.find_all("a", href=True):
        a.replace_with(f"{a.get_text(' ', strip=True)} <{urllib.parse.urljoin(taban, a['href'])}>")
    for tr in soup.find_all("tr"):
        tr.replace_with(" | ".join(td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])) + "\n")
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for p in soup.find_all(["p", "div", "li", "h1", "h2", "h3", "h4"]):
        p.append("\n")
    t = htmlmod.unescape(soup.get_text())
    t = re.sub(r"[ \t\xa0]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def baglantilar(s, taban):
    soup = BeautifulSoup(s, "html.parser")
    out = []
    for a in soup.find_all("a", href=True):
        u = urllib.parse.urljoin(taban, a["href"].strip())
        out.append((u, a.get_text(" ", strip=True)))
    return out


def pdf_metin(yol):
    try:
        return subprocess.run(["pdftotext", "-layout", yol, "-"], capture_output=True, timeout=300).stdout.decode("utf-8", "replace")
    except Exception:
        return ""


def main():
    os.makedirs(HEDEF, exist_ok=True)
    kuyruk = []
    for f in sorted(os.listdir(KOK)):
        if f[0].isdigit() and f.endswith(".md"):
            for u in re.findall(r"<(https?://[^>\s]+)>", open(os.path.join(KOK, f), encoding="utf-8").read()):
                kuyruk.append((u, 0, f))
    gorulen, kayit, dis, hata = set(), [], set(), []
    while kuyruk:
        u, seviye, kaynak = kuyruk.pop(0)
        u = u.replace("http://", "https://", 1) if resmi(u) else u
        if u in gorulen:
            continue
        gorulen.add(u)
        if not resmi(u):
            dis.add(u)
            continue
        k = anahtar(u)
        if not k.lower().endswith(UZANTI) and "getFile" not in u:
            continue  # duyuru sayfası vb.
        yol = os.path.join(HEDEF, k)
        os.makedirs(os.path.dirname(yol), exist_ok=True)
        b, ct = getir(u)
        if b is None:
            hata.append((u, ct, kaynak))
            continue
        if not os.path.exists(yol) or open(yol, "rb").read() != b:
            open(yol, "wb").write(b)
        metin = ""
        if k.lower().endswith((".htm", ".html")) or "html" in ct:
            s = coz(b)
            metin = html_metin(s, u)
            if seviye < 3:
                for v, _ in baglantilar(s, u):
                    if v not in gorulen:
                        kuyruk.append((v, seviye + 1, k))
        elif k.lower().endswith(".pdf"):
            metin = pdf_metin(yol)
        if metin is not None and k.lower().endswith((".pdf", ".htm", ".html")):
            ust = (f"---\nkaynak: {u}\ndosya: {os.path.basename(k)}\nbaglanti_sayfasi: {kaynak}\n---\n\n")
            govde = metin.strip() or "_(Metin çıkarılamadı: taranmış görüntü olabilir; özgün dosyaya bakınız.)_"
            open(yol + ".md", "w", encoding="utf-8").write(ust + govde + "\n")
        kayit.append({"url": u, "dosya": os.path.relpath(yol, KOK), "bayt": len(b),
                      "metin_karakter": len(metin.strip()), "kaynak": kaynak})
        print(f"{len(kayit):4} {k} ({len(b)//1024} KB)", flush=True)
    json.dump({"dosyalar": kayit, "hatalar": hata, "dis_baglantilar": sorted(dis)},
              open(os.path.join(KOK, "_indirme.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({"indirilen": len(kayit), "hata": len(hata), "dis": len(dis),
                      "metinsiz_pdf": sum(1 for x in kayit if x["dosya"].endswith(".pdf") and x["metin_karakter"] < 200)},
                     ensure_ascii=False))




def cvoa_dizin():
    """ÇVÖA sayfalarından ülke / özelge / tebliğ / sirküler dizinlerini yazar (gib/uluslararasi/cvoa/)."""
    cv = os.path.join(KOK, "cvoa")
    os.makedirs(cv, exist_ok=True)
    taban = os.path.join(HEDEF, "arsiv/mevzuat/uluslararasi_mevzuat/Cifte_Vergilendirme")
    yerel = lambda u: os.path.relpath(os.path.join(HEDEF, anahtar(u)), cv)
    var = lambda u: os.path.exists(os.path.join(HEDEF, anahtar(u)))

    def soup(ad):
        return BeautifulSoup(coz(open(os.path.join(taban, ad), "rb").read()), "html.parser")

    # ülkeler: her hücre bir ülke, içinde bir veya birkaç bağlantı
    s, ulke = soup("Ciftevergilendirmeturkcemetinleri.htm"), []
    for td in s.find_all("td"):
        al = td.find_all("a", href=True)
        if not al:
            continue
        ad = re.sub(r"\s+", " ", td.get_text(" ", strip=True))
        if not ad:
            continue  # sayfadaki görünmez yinelenen satırlar
        bag = []
        for a in al:
            u = urllib.parse.urljoin("https://cdn.gib.gov.tr/", a["href"].strip()).replace("//TURKCE_METIN", "/TURKCE_METIN")
            etiket = re.sub(r"\s+", " ", a.get_text(" ", strip=True)) or os.path.basename(anahtar(u))
            if var(u):
                bag.append(f"[{etiket}]({yerel(u)}.md) ([PDF]({yerel(u)}))")
            else:
                bag.append(f"{etiket} (GİB bağlantısı çalışmıyor: {u})")
        ulke.append((ad, bag))
    # özelgeler
    s, oz = soup("Ciftevergilendirmeozelgeleri.htm"), []
    for tr in s.find_all("tr"):
        td = [re.sub(r"\s+", " ", x.get_text(" ", strip=True)) for x in tr.find_all("td")]
        a = tr.find("a", href=True)
        if not a or len(td) < 3:
            continue
        u = urllib.parse.urljoin("https://cdn.gib.gov.tr/", a["href"].strip())
        tarih, sayi, konu = td[0], td[-2], td[-1]
        oz.append((tarih, sayi, konu, f"[metin]({yerel(u)}.md)" if var(u) else f"(GİB bağlantısı çalışmıyor: {u})"))
    with open(os.path.join(cv, "README.md"), "w", encoding="utf-8") as o:
        o.write("# Çifte Vergilendirmeyi Önleme Anlaşmaları (ÇVÖA)\n\n"
                "Kaynak: GİB → Mevzuat → Uluslararası Mevzuat → Çifte Vergilendirmeyi Önleme Anlaşmaları "
                "(cdn.gib.gov.tr). Anlaşmalar Anayasa md. 90 uyarınca kanun hükmündedir. Her anlaşmanın özgün PDF'i "
                "ve metne çevrilmiş hali (.md) `../dosyalar/` altındadır.\n\n"
                "- [ÇVÖA özelgeleri](ozelgeler.md) · [ÇVÖA genel tebliğleri ve sirküler](tebligler.md)\n"
                "- Oran tabloları ve listeler: [Sonuçlandırılan anlaşmalar listesi](../dosyalar/arsiv/mevzuat/uluslararasi_mevzuat/Cifte_Vergilendirme/Turkiyenin_Sonuclandirdigi_Vergi_Anlasmalari_Listesi.pdf.md), "
                "[Ek protokoller tablosu](../dosyalar/arsiv/mevzuat/uluslararasi_mevzuat/Cifte_Vergilendirme/Ek_Protokollere_Iliskin_Tablo.pdf.md), "
                "[Temettü oranları](../dosyalar/arsiv/mevzuat/uluslararasi_mevzuat/Cifte_Vergilendirme/Temettuler_Uzerinden_Kaynak_Devlette_Alinacak_Vergi_Oranlari.pdf.md), "
                "[Faiz ve gayrimaddi hak oranları](../dosyalar/arsiv/mevzuat/uluslararasi_mevzuat/Cifte_Vergilendirme/Faiz_ve_Gayrimaddi_Hak_Bedelleri_Uzerinden_Kaynak_Devlette_Alinacak_Vergi_Oranlari.pdf.md), "
                "[İnşaat işyeri süreleri](../dosyalar/arsiv/mevzuat/uluslararasi_mevzuat/Cifte_Vergilendirme/Insaat_Faaliyetlerinde_Isyeri_Tespit_Sureleri.pdf.md)\n\n"
                f"## Anlaşma Türkçe metinleri ({len(ulke)} ülke)\n\n| Ülke | Metin |\n|---|---|\n")
        for ad, bag in ulke:
            o.write(f"| {ad.replace('|','/')} | {' · '.join(bag)} |\n")
    with open(os.path.join(cv, "ozelgeler.md"), "w", encoding="utf-8") as o:
        o.write(f"# ÇVÖA özelgeleri ({len(oz)})\n\nKaynak: GİB ÇVÖA özelgeleri sayfası. En yeni üstte (GİB sırası).\n\n"
                "| Tarih | Sayı | Konu | Metin |\n|---|---|---|---|\n")
        for t, sy, k, m in oz:
            o.write(f"| {t} | {sy.replace('|','/')} | {k.replace('|','/')} | {m} |\n")
    s, tb = soup("Ciftevergilendirmetebligleri.htm"), []
    gor = set()
    for tr in s.find_all("tr"):
        td = [re.sub(r"\s+", " ", x.get_text(" ", strip=True)) for x in tr.find_all("td")]
        al = [urllib.parse.urljoin("https://cdn.gib.gov.tr/", a["href"].strip()) for a in tr.find_all("a", href=True)]
        if not al or td[0] in gor:
            continue
        gor.add(td[0])
        bag = [(f"[{os.path.basename(anahtar(u))}]({yerel(u)}.md)" if var(u) and u.endswith((".htm", ".html", ".pdf")) else
                (f"[{os.path.basename(anahtar(u))}]({yerel(u)})" if var(u) else f"Resmî Gazete: {u}")) for u in al]
        tb.append((td[0], td[1] if len(td) > 1 else "", td[2] if len(td) > 2 else "", bag))
    sirk = os.path.join(taban, "Ciftevergilendirmesirkuleri.htm")
    with open(os.path.join(cv, "tebligler.md"), "w", encoding="utf-8") as o:
        o.write(f"# ÇVÖA genel tebliğleri ({len(tb)})\n\n| Tebliğ | RG sayı | RG tarih | Metin |\n|---|---|---|---|\n")
        for a, b, c, bag in tb:
            o.write(f"| {a.replace('|','/')} | {b} | {c} | {' · '.join(bag)} |\n")
        if os.path.exists(sirk):
            o.write("\n## ÇVÖA sirküleri\n\n" + html_metin(coz(open(sirk, "rb").read()), "https://cdn.gib.gov.tr/") + "\n")
    return len(ulke), len(oz), len(tb)


if __name__ == "__main__":
    if sys.argv[1:] == ["dizin"]:
        print(cvoa_dizin())
    else:
        main()
        print(cvoa_dizin())
