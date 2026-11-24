#!/usr/bin/env python3
"""Danıştay İçtihatları Birleştirme Kurulu (İBK) kararları ve Vergi Dava Daireleri Kurulu (VDDK)
gündem karar bültenlerini danistay.gov.tr'den çeker.

İBK : Danıştay İçtihat, Raporlama ve İstatistik Birimi'nin "İçtihatları Birleştirme Kurulu
      Kararları Hakkında Karar Bülteni (1965–2024)" yayını; bültendeki her kararın resmî PDF'i
      (danistay.gov.tr/assets/pdf/upload/...) indirilir.
VDDK: api.danistay.gov.tr/api/v1/tr/yayin/kararlarBultenler listesindeki tüm bültenler.

Çıktı: kararlar/danistay/ibk/<sıra>.pdf + .md, ibk/README.md
       kararlar/danistay/vddk-bultenleri/<gündem tarihi>.pdf + .md, README.md
Kullanım: python3 araclar/danistay/ibk_bulten_cek.py <depo kökü>
"""
import json, os, re, subprocess, sys, time, urllib.request

IBK_BULTEN = "https://www.danistay.gov.tr/assets/images/yayinlar/dergi/2025-10-09-02-08-8628769.pdf"
VDDK_LISTE = "https://api.danistay.gov.tr/api/v1/tr/yayin/kararlarBultenler"
VDDK_DOSYA = "https://www.danistay.gov.tr/assets/pdf/yayinlar/kararlarBulteni/"
VERGI = re.compile(r"(vergi|harç|resim|tarh|mükellef|amme alaca|tahsil|gümrük|vergi ziya|ceza ihbarname|"
                   r"katma değer|gelir vergisi|kurumlar vergisi|emlak|damga|matrah|ödeme emri|213 sayılı|6183)", re.I)


def getir(u):
    for d in range(4):
        try:
            r = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 ymm-mevzuat-bankasi"})
            with urllib.request.urlopen(r, timeout=180) as y:
                return y.read()
        except Exception as e:
            print(f"  ! {u}: {e}", file=sys.stderr, flush=True)
            time.sleep(4 * (d + 1))
    return None


def pdf_metin(yol, layout=False):
    a = ["pdftotext"] + (["-layout"] if layout else []) + [yol, "-"]
    try:
        return subprocess.run(a, capture_output=True, timeout=300).stdout.decode("utf-8", "replace")
    except Exception:
        return ""


def temiz(s):
    s = re.sub(r"[\x00-\x08\x0b-\x1f]", "", s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def ibk(depo):
    kok = os.path.join(depo, "kararlar", "danistay", "ibk")
    os.makedirs(kok, exist_ok=True)
    b = getir(IBK_BULTEN)
    bp = os.path.join(kok, "_bulten-1965-2024.pdf")
    open(bp, "wb").write(b)
    t = re.sub(r"[\x00-\x08\x0b-\x1f]", "", pdf_metin(bp))
    # URL'ler satır sonlarında bölünmüş olabilir
    desen = re.compile(r"h\s*t\s*t\s*p\s*s?\s*:\s*/\s*/[^\n]*?(?:\n[^\n]*?)?\.pdf")
    bolum, onceki, kayit = "", 0, []
    basliklar = list(re.finditer(r"\n([A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ ,'’-]{10,}KARARLAR)\n", t))
    for m in desen.finditer(t):
        url = re.sub(r"\s+", "", m.group(0)).replace("http://", "https://")
        parca = t[onceki:m.start()]
        for h in basliklar:
            if h.start() < m.start():
                bolum = h.group(1).strip()
        parca = parca.replace("İçtihatları Birleştirme Kurulu", "")
        parca = re.sub(r"\n\s*\d{1,3}\s*\n", "\n", "\n" + parca + "\n")
        for h in basliklar:
            parca = parca.replace(h.group(1), "")
        ozet = re.sub(r"\s+", " ", parca).strip()
        ozet = re.sub(r"^.*?(KARAR BÜLTENİ.*?güncellenmiştir\.)", "", ozet).strip()
        onceki = m.end()
        kayit.append({"sira": len(kayit) + 1, "url": url, "bolum": bolum, "ozet": ozet})
    for k in kayit:
        pdf = os.path.join(kok, f"{k['sira']:03d}.pdf")
        b = getir(k["url"])
        if b:
            open(pdf, "wb").write(b)
        metin = temiz(pdf_metin(pdf)) if b else ""
        e = re.search(r"Esas\s*(?:No|Sayısı)\s*[:.]?\s*(\d{4}\s*/\s*\d+)", metin, re.I)
        kk = re.search(r"Karar\s*(?:No|Sayısı)\s*[:.]?\s*(\d{4}\s*/\s*\d+)", metin, re.I)
        tr = re.search(r"Karar\s*Tarihi\s*[:.]?\s*(\d{1,2}[./]\d{1,2}[./]\d{4})", metin, re.I)
        k.update(esas=(e.group(1).replace(" ", "") if e else ""), karar=(kk.group(1).replace(" ", "") if kk else ""),
                 tarih=(tr.group(1) if tr else ""), vergi=bool(VERGI.search(k["ozet"]) or VERGI.search(metin[:4000])),
                 metin=len(metin))
        open(pdf[:-4] + ".md", "w", encoding="utf-8").write("\n".join([
            "---", "tur: Danıştay İçtihatları Birleştirme Kurulu kararı", f"sira: {k['sira']}",
            f"esas_no: {k['esas']}", f"karar_no: {k['karar']}", f"karar_tarihi: {k['tarih']}",
            f"bulten_bolumu: {json.dumps(k['bolum'], ensure_ascii=False)}", f"vergi_ile_ilgili: {str(k['vergi']).lower()}",
            f"kaynak: {k['url']}", f"bulten: {IBK_BULTEN}", f"alindi: {time.strftime('%Y-%m-%d')}", "---", "",
            f"# Danıştay İBK — E.{k['esas']} K.{k['karar']}", "", "## Bültendeki özet", "", k["ozet"], "",
            "## Karar metni", "", metin or "_(Metin çıkarılamadı: taranmış görüntü olabilir; PDF'e bakınız.)_", ""]))
        print(f"İBK {k['sira']}: {k['esas']} {k['karar']} vergi={k['vergi']} metin={k['metin']}", flush=True)
    with open(os.path.join(kok, "README.md"), "w", encoding="utf-8") as o:
        v = sum(1 for k in kayit if k["vergi"])
        o.write(f"# Danıştay İçtihatları Birleştirme Kurulu kararları ({len(kayit)} karar; {v}'i vergiyle ilgili)\n\n"
                f"Kaynak: Danıştay İçtihat, Raporlama ve İstatistik Birimi, *İçtihatları Birleştirme Kurulu Kararları "
                f"Hakkında Karar Bülteni (1965–2024)*, 09.10.2025 güncellemesi — {IBK_BULTEN}. İBK kararları idareyi ve "
                "idari yargı mercilerini bağlar. \"Vergi\" sütunu özet ve metindeki ifadelere göre otomatik işaretlenmiştir.\n\n"
                "| Sıra | Esas / Karar | Karar tarihi | Vergi | Bülten bölümü | Özet |\n|---|---|---|---|---|---|\n")
        for k in kayit:
            o.write(f"| {k['sira']} | [E.{k['esas']} K.{k['karar']}]({k['sira']:03d}.md) | {k['tarih']} | {'✓' if k['vergi'] else ''} | "
                    f"{k['bolum'].title()} | {k['ozet'][:220].replace('|', '/')} |\n")
    return kayit


def vddk(depo):
    kok = os.path.join(depo, "kararlar", "danistay", "vddk-bultenleri")
    os.makedirs(kok, exist_ok=True)
    liste = json.loads(getir(VDDK_LISTE))
    kayit = []
    for x in liste:
        baslik = re.sub(r"\s+", " ", x["baslik"]).strip()
        g = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", baslik)
        ad = f"{g.group(3)}-{int(g.group(2)):02d}-{int(g.group(1)):02d}" if g else f"id-{x['id']}"
        url = VDDK_DOSYA + x["dokuman"].strip()
        pdf = os.path.join(kok, f"{ad}_{x['id']}.pdf")
        b = getir(url)
        if not b or not b.startswith(b"%PDF"):
            kayit.append({"ad": ad, "baslik": baslik, "url": url, "hata": True})
            continue
        open(pdf, "wb").write(b)
        metin = temiz(pdf_metin(pdf))
        open(pdf[:-4] + ".md", "w", encoding="utf-8").write("\n".join([
            "---", "tur: Danıştay VDDK gündem karar bülteni", f"baslik: {json.dumps(baslik, ensure_ascii=False)}",
            f"gundem_tarihi: {ad}", f"yayim: {x.get('tarih','')}", f"kaynak: {url}", f"alindi: {time.strftime('%Y-%m-%d')}",
            "---", "", f"# {baslik}", "", metin or "_(Metin çıkarılamadı.)_", ""]))
        kayit.append({"ad": ad, "baslik": baslik, "url": url, "dosya": os.path.basename(pdf)[:-4] + ".md", "metin": len(metin)})
        print(f"VDDK {ad}: {len(metin)}", flush=True)
    kayit.sort(key=lambda k: k["ad"], reverse=True)
    with open(os.path.join(kok, "README.md"), "w", encoding="utf-8") as o:
        o.write(f"# Danıştay Vergi Dava Daireleri Kurulu gündem karar bültenleri ({sum(1 for k in kayit if not k.get('hata'))} bülten)\n\n"
                f"Kaynak: Danıştay, Yayınlar → Kararlar Bülteni ({VDDK_LISTE}). Her bülten bir Kurul gündeminde verilen "
                "kararların künye ve özetlerini içerir. En yeni üstte.\n\n| Gündem tarihi | Bülten |\n|---|---|\n")
        for k in kayit:
            o.write(f"| {k['ad']} | " + (f"[{k['baslik']}]({k['dosya']})" if not k.get("hata") else f"{k['baslik']} (indirilemedi: {k['url']})") + " |\n")
    return kayit


if __name__ == "__main__":
    d = sys.argv[1]
    a = ibk(d)
    v = vddk(d)
    print(json.dumps({"ibk": len(a), "ibk_vergi": sum(1 for k in a if k["vergi"]), "ibk_metinsiz": sum(1 for k in a if k["metin"] < 300),
                      "vddk_bulten": sum(1 for k in v if not k.get("hata")), "vddk_hata": sum(1 for k in v if k.get("hata"))}, ensure_ascii=False))
