#!/usr/bin/env python3
"""Madde dosyalarından yapısal analiz üretir. Yalnızca metinde yazanı sayar; yorum katmaz.
Kullanım: analiz.py <kanun klasörü> <kanun adı>"""
import re, sys, pathlib, collections, datetime
d, ad = pathlib.Path(sys.argv[1]), sys.argv[2]
def key(p):
    n = p.stem
    m = re.match(r"(madde|ek-madde|gecici-madde)-(\d+)(.*)", n)
    grp = {"madde": 0, "ek-madde": 1, "gecici-madde": 2}.get(m.group(1), 3) if m else 3
    return (grp, int(m.group(2)) if m else 0, m.group(3) if m else n)
files = sorted([p for p in d.glob("*.txt") if re.match(r"(madde|ek-madde|gecici-madde)-", p.name)], key=key)
def etiket(stem):
    m = re.match(r"madde-(\d+)(?:-(mukerrer)(-2)?|-([A-Z]))?$", stem)
    if m:
        n = str(int(m.group(1)))
        if m.group(2): return f"Mükerrer {n}"
        if m.group(4): return f"{n}/{m.group(4)}"
        return n
    m = re.match(r"ek-madde-(\d+)", stem)
    if m: return f"Ek {int(m.group(1))}"
    m = re.match(r"gecici-madde-(\d+)", stem)
    if m: return f"Geçici {int(m.group(1))}"
    return stem
ann = re.compile(r"\(\s*([^():]{2,70}?)\s*:\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*[-–]\s*((?:KHK\s*[-/]?\s*)?\d+)\s*/")
head = re.compile(r"(?:Madde|MADDE)[^(]{0,25}\(([^)]*)\)")
tur_say = collections.Counter(); kanun = collections.defaultdict(lambda: {"tarih": None, "maddeler": [], "tur": collections.Counter()})
mulga_baslik = []; toplam_kar = 0
for p in files:
    t = p.read_text(encoding="utf-8"); toplam_kar += len(t)
    flat = re.sub(r"\s+", " ", t)
    hm = head.search(flat[:500])
    if hm and "Mülga" in hm.group(1): mulga_baslik.append(etiket(p.stem))
    for m in ann.finditer(flat):
        tur = m.group(1).strip()
        kat = "Mülga" if tur.startswith("Mülga") else "Değişik" if tur.startswith("Değişik") else "Ek" if tur.startswith("Ek") else "İptal" if tur.startswith("İptal") else "Diğer"
        try: tarih = datetime.date(int(m.group(4)), int(m.group(3)), int(m.group(2)))
        except ValueError: continue
        no = re.sub(r"\s+", "", m.group(5))
        tur_say[kat] += 1
        k = kanun[no]; k["tarih"] = tarih; k["tur"][kat] += 1
        if etiket(p.stem) not in k["maddeler"]: k["maddeler"].append(etiket(p.stem))
# bölüm yapısı
sira = r"(?:BİRİNCİ|İKİNCİ|ÜÇÜNCÜ|DÖRDÜNCÜ|BEŞİNCİ|ALTINCI|YEDİNCİ|SEKİZİNCİ|DOKUZUNCU|ONUNCU|ON\s?BİRİNCİ|ON\s?İKİNCİ|ON\s?ÜÇÜNCÜ|ON\s?DÖRDÜNCÜ|ON\s?BEŞİNCİ|ON\s?ALTINCI)"
bol = re.compile(rf"^\s*({sira})\s+(KİTAP|KISIM)\s*$")
yapi = []
alt = re.compile(rf"^\s*{sira}\s+(KİTAP|KISIM|BÖLÜM|AYIRIM)\s*$")
mad = re.compile(r"^\s*(?:(?:Mükerrer|Geçici|Ek|GEÇİCİ|EK)\s+)?(?:Madde|MADDE)\s*[\dl]")
ana = [p for p in files if p.name.startswith("madde-")]
tara = [(d / "00-baslik.txt", None)] + [(p, n) for n, p in enumerate(ana)]
for p, n in tara:
    ls = p.read_text(encoding="utf-8").split("\n")
    mi = next((i for i, x in enumerate(ls) if mad.match(x)), None)
    for i, ln in enumerate(ls):
        m = bol.match(ln)
        if not m: continue
        bas = []
        for x in ls[i + 1:i + 5]:
            if not x.strip() or alt.match(x) or mad.match(x): break
            bas.append(x.strip())
        if n is None: ilk = etiket(ana[0].stem)
        elif mi is not None and i > mi: ilk = etiket(ana[n + 1].stem) if n + 1 < len(ana) else "-"
        else: ilk = etiket(p.stem)
        yapi.append((m.group(2), f"{m.group(1)} {m.group(2)}", " ".join(bas), ilk))
o = [f"# {ad} — yapısal analiz", "",
     "Bu dosya `araclar/analiz.py` ile madde dosyalarından otomatik üretilmiştir. Yalnızca metinde",
     "yazanları sayar; hiçbir hukuki yorum içermez. Kaynak ve doğrulama durumu için `KAYNAK.md`.", "",
     "## Sayılar", "",
     f"- Madde dosyası: {len(files)} (ana, mükerrer, harfli, ek ve geçici maddeler dahil)",
     f"- Madde numarasından sonraki ilk işlem notunda \"Mülga\" geçen: {len(mulga_baslik)}",
     f"- Parantez içi işlem notu (\"Değişik: tarih-kanun no/madde\" biçiminde): {sum(tur_say.values())}"
     + " (" + ", ".join(f"{k}: {v}" for k, v in tur_say.most_common()) + ")",
     f"- İşlem notlarında adı geçen farklı kanun/KHK sayısı: {len(kanun)}", "",
     "Not: İbare değişiklikleri çoğunlukla dipnotlarda yazıldığı için bu sayıma girmez. Tam liste için",
     "`zz-islenemeyen-hukumler-ve-ekler.txt` dosyasındaki değişiklik tablosuna bakınız.", ""]
if yapi:
    o += ["## Bölüm yapısı (kitap ve kısım düzeyi)", "", "Başlık sonundaki sayılar kaynak metindeki dipnot işaretleridir.", "", "| Bölüm | Başlık | İlk maddesi |", "|---|---|---|"]
    o += [f"| {'' if t == 'KİTAP' else '&nbsp;&nbsp;'}{a} | {b} | {m} |" for t, a, b, m in yapi] + [""]
son = sorted(kanun.items(), key=lambda kv: kv[1]["tarih"], reverse=True)[:15]
o += ["## İşlem notlarına göre en yeni 15 değişiklik", "",
      "Tarih, değişikliği yapan kanunun işlem notunda yazan tarihidir. Madde sütunu, notun bulunduğu",
      "dosyayı gösterir; dipnot ve cetveller PDF'teki sayfa konumunda durduğu için bir not nadiren",
      "komşu maddenin dosyasında yer alabilir. Kullanmadan önce ilgili madde dosyasını açıp teyit ediniz.", "",
      "| Tarih | Kanun/KHK no | İşlem | Maddeler |", "|---|---|---|---|"]
for no, k in son:
    o.append(f"| {k['tarih'].strftime('%d.%m.%Y')} | {no} | " + ", ".join(f"{a}: {b}" for a, b in k["tur"].most_common()) + " | " + ", ".join(k["maddeler"]) + " |")
o += ["", "## İlk işlem notunda \"Mülga\" geçen maddeler", "", ", ".join(mulga_baslik) or "Yok", ""]
(d / "ANALIZ.md").write_text("\n".join(o), encoding="utf-8")
print(len(files), len(mulga_baslik), sum(tur_say.values()), dict(tur_say), len(kanun), len(yapi), toplam_kar)
