#!/usr/bin/env python3
"""sgk/kaysis/dizin.csv'deki kayıtları kaysis_indir.js'nin beklediği {kategori: [id, ...]} biçiminde yazar.
Kullanım: python3 araclar/sgk/kaysis_bilinen.py > /tmp/kaysis_calistir.js  (betiğin __BILINEN__ yeri doldurulmuş hali)"""
import csv, json, pathlib, collections
KOK = pathlib.Path(__file__).resolve().parents[2]
d = collections.defaultdict(list)
with (KOK / "sgk" / "kaysis" / "dizin.csv").open(encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        d[r["kategori"]].append(int(r["kaynak"].rsplit("/", 1)[-1]))
js = (KOK / "araclar" / "sgk" / "kaysis_indir.js").read_text(encoding="utf-8")
js = "\n".join(l for l in js.splitlines() if not l.lstrip().startswith("//"))
print(js.replace("__BILINEN__", json.dumps(d, ensure_ascii=False, separators=(",", ":"))))
