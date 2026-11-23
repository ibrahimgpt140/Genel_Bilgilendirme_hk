# Kullanım: python3 depoya_yaz.py REPO ALINMA_TARIHI dizin1.jsonl [dizin2.jsonl ...] -- metin_klasoru1 [...]
import sys, os, json, csv, re, html, glob
args=sys.argv[1:]; REPO, ALINMA = args[0], args[1]; rest=args[2:]
sep=rest.index('--'); dizinler=rest[:sep]; metinler=rest[sep+1:]
OUT=os.path.join(REPO,'kararlar','danistay')
def slug(d):
    if d=='Vergi Dava Daireleri Kurulu': return 'vddk'
    if d=='İdare Dava Daireleri Kurulu': return 'iddk'
    m=re.search(r'(\d+)\. Daire',d); return f"{m.group(1)}-daire"
def ad(x): return f"E{x['esas'].replace('/','-')}_K{x['karar'].replace('/','-')}"
GRUP={'sahte_belge':'Sahte belge','sahte_fatura':'Sahte belge','kdv_iadesi':'KDV iadesi','kdv_iadesi_2':'KDV iadesi',
      'iade_talebi_kdv':'KDV iadesi','mahsuben_iade':'KDV iadesi','ozel_esaslar':'KDV iadesi','vergi_ziyai':'Vergi ziyaı','tebligat':'Tebligat'}
# Konu kelimeleri (Karar Arama'daki konu aramalarının metin içi karşılığı)
KONU_RE=[('Sahte belge',r'sahte\s+(belge|fatura)'),
         ('KDV iadesi',r'kdv\s+iades|katma\s+değer\s+vergisi\s+iades|mahsuben\s+iade|özel\s+esaslar'),
         ('Vergi ziyaı',r'vergi\s+ziyaı\s+cezas'),('Tebligat',r'tebligat')]
def kucuk(t): return t.replace('İ','i').replace('I','ı').lower()
def konu_tespit(t):
    k=kucuk(t); r={g for g,p in KONU_RE if re.search(p,k)}
    if 'KDV iadesi' not in r and re.search(r'iade\s+talebi',k) and re.search(r'katma\s+değer\s+vergisi',k): r.add('KDV iadesi')
    return r
TUM_METIN={'Vergi Dava Daireleri Kurulu'}   # bu dairelerde konu aranmadan tüm kararlar yazılır
kayit={}
for f in dizinler:
    for l in open(f,encoding='utf-8'):
        o=json.loads(l)
        if 'id' not in o: continue
        k=kayit.setdefault(o['id'],dict(o,konular=set()))
        if o.get('konu'): k['konular'].add(GRUP.get(o['konu'],o['konu']))
        for g in o.get('konular') or []: k['konular'].add(g)
htmls={}
for d in metinler:
    for f in glob.glob(os.path.join(d,'*.html')): htmls[os.path.basename(f)[:-5]]=f
def metne(h):
    t=re.sub(r'<br\s*/?>','\n',h,flags=re.I); t=re.sub(r'</p\s*>','\n',t,flags=re.I)
    t=re.sub(r'<[^>]+>','',t); t=html.unescape(t).replace('\xa0',' ')
    t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n\n',t)
    return '\n'.join(s.strip() for s in t.split('\n')).strip()
yazilan=0; dogrulanmayan=[]
for id_,x in kayit.items():
    if id_ not in htmls: continue
    yil=x['karar'].split('/')[0]; hedef=os.path.join(OUT,slug(x['daire']),yil); os.makedirs(hedef,exist_ok=True)
    yol=os.path.join(hedef,ad(x)+'.md')
    if os.path.exists(yol): continue   # önceki aktarımın özetli dosyası korunur
    t=metne(open(htmls[id_],encoding='utf-8').read())
    x['konular']|=konu_tespit(t)
    if x['daire'] not in TUM_METIN and not x['konular']: continue   # konu dışı karar: yalnızca dizinde
    tn=re.sub(r'\s+','',t)
    ok=(x['esas'].replace(' ','') in tn and x['karar'].replace(' ','') in tn)
    if not ok: dogrulanmayan.append(id_)
    url=f"https://karararama.danistay.gov.tr/karar/{id_}"
    md=f'''---
mahkeme: Danıştay
daire: {x['daire']}
esas_no: "{x['esas']}"
karar_no: "{x['karar']}"
karar_tarihi: "{x['tarih']}"
belge_no: "{id_}"
kaynak: {url}
alinma_tarihi: "{ALINMA}"
konular: [{', '.join(sorted(x['konular']))}]
dogrulama: "{'Esas ve karar numarası karar metninde bulundu' if ok else 'DOĞRULANMADI – künye karar metninde bulunamadı'}"
---

# Danıştay {x['daire']} – E: {x['esas']}, K: {x['karar']} ({x['tarih']})

**Kaynak:** [Danıştay Karar Arama, belge no {id_}]({url}) · İndirilme: {ALINMA}{(' · **Konular:** '+', '.join(sorted(x['konular']))) if x['konular'] else ''}

## Karar metni

{t}
'''
    open(yol,'w',encoding='utf-8').write(md); yazilan+=1
# dizin CSV'leri: daire-yıl başına
from collections import defaultdict
gr=defaultdict(list)
for id_,x in kayit.items(): gr[(slug(x['daire']),x['karar'].split('/')[0])].append(x)
# özetli ilk aktarım dosyaları gibi önceden var olan dosyaların konusu: metinden tespit
for id_,x in kayit.items():
    if x['konular']: continue
    p=os.path.join(OUT,slug(x['daire']),x['karar'].split('/')[0],ad(x)+'.md')
    if os.path.exists(p): x['konular']|=konu_tespit(open(p,encoding='utf-8').read())
os.makedirs(os.path.join(OUT,'dizin'),exist_ok=True)
for (s,y),xs in gr.items():
    xs.sort(key=lambda x:(x.get('ksira') or 0))
    with open(os.path.join(OUT,'dizin',f'{s}-{y}.csv'),'w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['daire','esas_no','karar_no','karar_tarihi','belge_no','konular','tam_metin','kaynak','alinma_tarihi'])
        for x in xs:
            p=os.path.join(s,y,ad(x)+'.md')
            w.writerow([x['daire'],x['esas'],x['karar'],x['tarih'],x['id'],'; '.join(sorted(x['konular'])),p if os.path.exists(os.path.join(OUT,p)) else '',f"https://karararama.danistay.gov.tr/karar/{x['id']}",ALINMA])
print('yazılan',yazilan,'doğrulanmayan',len(dogrulanmayan),dogrulanmayan[:10]); print({f'{s}-{y}':len(v) for (s,y),v in sorted(gr.items())})
