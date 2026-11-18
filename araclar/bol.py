#!/usr/bin/env python3
"""Kanun tam metnini (pdftotext çıktısı) madde madde böler; sıra kontrolü yapar."""
import re, sys, json, pathlib
src, outdir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
lines = src.read_text(encoding="utf-8").replace("\f", "\n").split("\n")
pat = re.compile(r"^\s*(?:(Mükerrer|Geçici|Ek|MÜKERRER|GEÇİCİ|EK)\s+)?(?:Madde|MADDE)\s*(\d[\dl]*)?\s*(?:/\s*([A-ZÇĞİÖŞÜ]))?\s*([-–—]|$|\s)")
main = ek = gec = 0
arts = []      # (key, startline)
log = []
done = False
for i, ln in enumerate(lines):
    if done: break
    if re.search(r"KANUNA (İŞLENEMEYEN|EK VE DEĞİŞİKLİK GETİREN)", ln) and main > 10:
        arts.append(("zz-islenemeyen-hukumler-ve-ekler", i)); done = True
        log.append(f"EK BÖLÜM BAŞLANGICI: satır {i+1}: {ln.strip()[:70]}"); break
    m = pat.match(ln)
    if not m:
        continue
    kind = (m.group(1) or "").lower().replace("i̇", "i")
    raw = m.group(2)
    if raw and "l" in raw:
        log.append(f"KAYNAKTA YAZIM HATASI: '{raw}' -> '{raw.replace('l','1')}' (satır {i+1})"); raw = raw.replace("l", "1")
    num = int(raw) if raw else None
    if isinstance(num, int):
        exp = {"main": main + 1, "gec": gec + 1, "ek": ek + 1, "muk": main}[{"mükerrer": "muk", "geçici": "gec", "ek": "ek", "": "main"}.get(kind, kind)]
        if num != exp and str(num).startswith(str(exp)) and len(str(num)) > len(str(exp)) and num > exp + 40:
            log.append(f"DİPNOT İŞARETİ YAPIŞIK: '{num}' -> Madde {exp} (satır {i+1})"); num = exp
    suf = m.group(3)
    dash = m.group(4) in "-–—" and m.group(4) != ""
    kind = {"mükerrer": "muk", "geçici": "gec", "ek": "ek", "": "main"}.get(kind, kind)
    if kind == "main":
        if num is None: continue
        if suf and num == main:
            arts.append((f"madde-{num:04d}-{suf}", i)); continue
        if num == main + 1:
            main = num; arts.append((f"madde-{num:04d}", i)); continue
        if dash and main < num <= main + 40 and gec == 0:
            log.append(f"ATLAMA: Madde {main} -> {num} (satır {i+1}): {ln.strip()[:70]}")
            main = num; arts.append((f"madde-{num:04d}", i)); continue
        log.append(f"red: satır {i+1}: {ln.strip()[:70]}")
    elif kind == "muk":
        if num is not None and main - 1 <= num <= main + 1 and gec == 0:
            key = f"madde-{num:04d}-mukerrer" + (f"-{suf}" if suf else "")
            if any(k == key for k, _ in arts):
                n2 = 2
                while any(k == f"{key}-{n2}" for k, _ in arts): n2 += 1
                key += f"-{n2}"
            arts.append((key, i))
        else:
            log.append(f"red: satır {i+1}: {ln.strip()[:70]}")
    elif kind == "ek":
        if gec > 0: log.append(f"red: satır {i+1}: {ln.strip()[:70]}"); continue
        if num is None:
            arts.append((f"ek-madde-numarasiz-s{i+1}", i))
        elif num == ek + 1:
            ek = num; arts.append((f"ek-madde-{num:02d}", i))
        elif suf and num == ek:
            arts.append((f"ek-madde-{num:02d}-{suf}", i))
        else:
            log.append(f"red: satır {i+1}: {ln.strip()[:70]}")
    elif kind == "gec":
        if num is None: continue
        if num == gec + 1:
            gec = num; arts.append((f"gecici-madde-{num:02d}", i))
        elif suf and num == gec:
            arts.append((f"gecici-madde-{num:02d}-{suf}", i))
        elif num <= gec and gec >= 1:
            arts.append(("zz-islenemeyen-hukumler-ve-ekler", i)); done = True
            log.append(f"EK BÖLÜM BAŞLANGICI: satır {i+1}: {ln.strip()[:70]}")
        else:
            log.append(f"red: satır {i+1}: {ln.strip()[:70]}")
outdir.mkdir(parents=True, exist_ok=True)
(outdir / "00-baslik.txt").write_text("\n".join(lines[:arts[0][1]]).strip() + "\n", encoding="utf-8")
keys = [k for k, _ in arts]
assert len(keys) == len(set(keys)), [k for k in keys if keys.count(k) > 1]
# kenar başlıklarını (maddeden önce gelen başlık satırları) ait olduğu maddeye taşı
starts = [s for _, s in arts]
moved = 0
for n in range(1, len(arts)):
    if arts[n][0].startswith("zz-"): continue
    j, cnt = arts[n][1] - 1, 0
    while j > arts[n - 1][1]:
        t = lines[j].strip()
        if t == "": j -= 1; continue
        u = re.sub(r"\d+$", "", t).rstrip()
        if len(t) < 95 and u and u[-1] not in ".;,)”\"" and cnt < 12: cnt += 1; j -= 1
        else: break
    while j + 1 < arts[n][1] and lines[j + 1].strip() == "": j += 1
    if cnt: moved += 1
    starts[n] = j + 1
arts = [(k, starts[n]) for n, (k, _) in enumerate(arts)]
for n, (k, s) in enumerate(arts):
    e = arts[n + 1][1] if n + 1 < len(arts) else len(lines)
    (outdir / f"{k}.txt").write_text("\n".join(lines[s:e]).rstrip() + "\n", encoding="utf-8")
# bütünlük: parçaların birleşimi kaynağa eşit mi (boşluk hariç)
joined = "".join((outdir / f).read_text(encoding="utf-8") for f in ["00-baslik.txt"] + [k + ".txt" for k in keys])
same = re.sub(r"\s+", "", joined) == re.sub(r"\s+", "", "\n".join(lines))
print(json.dumps({"dosya": src.name, "ana_son": main, "ek_son": ek, "gecici_son": gec, "parca": len(arts), "butunluk": same, "baslik_tasinan": moved}, ensure_ascii=False))
print("\n".join(log))
