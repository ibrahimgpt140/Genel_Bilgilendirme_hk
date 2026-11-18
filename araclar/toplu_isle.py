#!/usr/bin/env python3
"""mevzuat.gov.tr toplu indirme paketlerini (JSON) depoya yerleştirir.
Kullanım: toplu_isle.py <paket.json> <depo kökü>
Paket türü dosya adından anlaşılır: tuzuk / genelteblig / kanun."""
import json, sys, re, base64, pathlib, subprocess, unicodedata, hashlib

TR = str.maketrans("çğıöşüÇĞİÖŞÜâîûÂÎÛ", "cgiosuCGIOSUaiuAIU")
MEVCUT_KANUN = {("213", "4"), ("6102", "5"), ("4458", "5"), ("3065", "5"), ("5520", "5"), ("193", "4"), ("3568", "5"),
                ("6183", "3"), ("488", "5"), ("492", "5"), ("4760", "5"), ("3218", "5")}


def slug(s, n=60):
    s = s.translate(TR).lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:n].rstrip("-") or "adsiz"


def kaynak(m):
    return f"https://www.mevzuat.gov.tr/mevzuat?MevzuatNo={m['no']}&MevzuatTur={m['tur']}&MevzuatTertip={m['tertip']}"


def baslik(m):
    return (f"KAYNAK: {kaynak(m)}\nADI: {m['ad']}\nTÜR: {m.get('turAd','')}\n"
            f"RESMÎ GAZETE: {m.get('rgTarih','')} / {m.get('rgSayi','')}\nALINMA: 18.11.2026 (mevzuat.gov.tr güncel metni)\n\n")


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


def aile(ad):
    u = ad.upper()
    for k, p in AILE:
        if re.search(p, u):
            return k
    return "diger"


def yaz_ekler(k, hedef):
    out = []
    for e in k.get("ekDosya") or []:
        hedef.mkdir(parents=True, exist_ok=True)
        p = hedef / e["ad"]
        p.write_bytes(base64.b64decode(e["b64"]))
        out.append(p.name)
    return out


def main():
    paket, kok = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    veri = json.loads(paket.read_text(encoding="utf-8"))
    t0 = str(veri[0]["tur"]) if veri else "9"
    tur = {"2": "tuzuk", "9": "genelteblig"}.get(t0, "kanun")
    satirlar, bos = [], []
    for k in veri:
        no, ad = str(k["no"]), k["ad"]
        if tur == "tuzuk":
            d = kok / "tuzukler" / f"{slug(no, 20)}-{slug(ad)}"
            d.mkdir(parents=True, exist_ok=True)
            (d / "tam-metin.txt").write_text(baslik(k) + (k.get("metin") or ""), encoding="utf-8")
            ek = yaz_ekler(k, d / "ekler")
            satirlar.append([d.relative_to(kok).as_posix(), ad, k.get("rgTarih", ""), len(ek)])
        elif tur == "genelteblig":
            d = kok / "tebligler" / "genel-tebligler" / aile(ad)
            d.mkdir(parents=True, exist_ok=True)
            f = d / f"{slug(no, 20)}-{slug(ad, 70)}.txt"
            f.write_text(baslik(k) + (k.get("metin") or ""), encoding="utf-8")
            ek = yaz_ekler(k, d / "ekler" / slug(no, 20))
            satirlar.append([f.relative_to(kok).as_posix(), ad, k.get("rgTarih", ""), len(ek)])
        else:
            if (no, str(k["tertip"])) in MEVCUT_KANUN and str(k["tur"]) == "1":
                satirlar.append(["(mevcut klasör)", ad, k.get("rgTarih", ""), 0])
                continue
            d = kok / "kanunlar" / "tum" / f"{slug(no, 10)}-{slug(ad, 60)}"
            d.mkdir(parents=True, exist_ok=True)
            info = ""
            if k.get("pdf"):
                pdf = kok / "kaynak-dosyalar" / "kanun-pdf" / f"{k['tur']}.{k['tertip']}.{no}.pdf"
                pdf.parent.mkdir(parents=True, exist_ok=True)
                pdf.write_bytes(base64.b64decode(k["pdf"]))
                txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
                (d / "tam-metin.txt").write_text(txt, encoding="utf-8")
                r = subprocess.run(["python3", str(kok / "araclar" / "bol.py"), str(d / "tam-metin.txt"), str(d)],
                                   capture_output=True, text=True)
                durum = "bölündü" if r.returncode == 0 and '"butunluk": true' in r.stdout else "yalnızca tam metin"
                if durum != "bölündü":
                    for f in d.glob("*.txt"):
                        if f.name != "tam-metin.txt":
                            f.unlink()
                info = (f"| PDF | `{pdf.relative_to(kok).as_posix()}` |\n| SHA-256 | `{hashlib.sha256(pdf.read_bytes()).hexdigest()}` |\n"
                        f"| Madde bölme | {durum} |\n")
                if r.stdout.strip():
                    info += "\nBölme betiği çıktısı:\n\n```\n" + r.stdout.strip()[:3000] + "\n```\n"
            else:
                (d / "tam-metin.txt").write_text(baslik(k) + (k.get("metin") or ""), encoding="utf-8")
                info = "| PDF | mevzuat.gov.tr'de PDF yok; HTML metin alındı |\n"
            (d / "KAYNAK.md").write_text(
                f"# {ad}\n\n| | |\n|---|---|\n| Kanun No | {no} |\n| Kaynak | {kaynak(k)} |\n"
                f"| Resmî Gazete | {k.get('rgTarih','')} / {k.get('rgSayi','')} |\n| Kabul | {k.get('kabul','')} |\n"
                f"| Alınma | 18.11.2026 (mevzuat.gov.tr güncel metni) |\n{info}\n"
                "Metin otomatik çıkarıldı; insan gözüyle resmî metinle karşılaştırılmadı. Kullanmadan önce mevzuat.gov.tr ile teyit ediniz.\n",
                encoding="utf-8")
            satirlar.append([d.relative_to(kok).as_posix(), ad, k.get("rgTarih", ""), 0])
        if not k.get("pdf") and len(k.get("metin") or "") < 200:
            bos.append([no, ad])
    print(json.dumps({"paket": paket.name, "adet": len(veri), "bos": bos}, ensure_ascii=False))
    idx = kok / "araclar" / "_toplu_dizin.jsonl"
    with idx.open("a", encoding="utf-8") as fh:
        for s in satirlar:
            fh.write(json.dumps([tur] + s, ensure_ascii=False) + "\n")


main()
