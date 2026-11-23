"""Haftalık Danıştay güncellemesi.
Vergi daireleri (VDDK, 3., 7., 9. Daire) için içinde bulunulan ve önceki yılın karar sayısını
depodaki dizinle karşılaştırır; artış varsa o daire-yılın künyelerini yeniden tarar, yeni VDDK
kararlarının tam metnini çeker ve depoya yazar. Kullanım: python3 guncelle.py REPO_KOKU
"""
import sys, os, json, csv, subprocess, datetime, glob
REPO=os.path.abspath(sys.argv[1]); HERE=os.path.dirname(os.path.abspath(__file__))
DANISTAY=os.path.join(REPO,'kararlar','danistay'); IS=os.path.join(HERE,'_calisma'); os.makedirs(IS,exist_ok=True)
DAIRE={'Vergi Dava Daireleri Kurulu':'vddk','3. Daire':'3-daire','7. Daire':'7-daire','9. Daire':'9-daire'}
TAM_METIN={'Vergi Dava Daireleri Kurulu'}
bugun=datetime.date.today(); yillar=[bugun.year-1,bugun.year]; alinma=bugun.strftime('%d.%m.%Y')
def node(*a): subprocess.run(['node',*a],cwd=HERE,check=True)
sayim=os.path.join(IS,'sayim.json')
node('sayim.js',sayim,','.join(map(str,yillar)),','.join(DAIRE))
rapor=[]; hedef=[]
for x in json.load(open(sayim)):
    if not isinstance(x['total'],int): rapor.append(f"{x['daire']} {x['yil']}: sayım alınamadı"); continue
    f=os.path.join(DANISTAY,'dizin',f"{DAIRE[x['daire']]}-{x['yil']}.csv")
    eski=sum(1 for _ in open(f,encoding='utf-8-sig'))-1 if os.path.exists(f) else 0
    if x['total']>eski: hedef.append(x); rapor.append(f"{x['daire']} {x['yil']}: {eski} → {x['total']} (+{x['total']-eski})")
    else: rapor.append(f"{x['daire']} {x['yil']}: değişiklik yok ({eski})")
if hedef:
    json.dump(hedef,open(os.path.join(IS,'hedef.json'),'w'),ensure_ascii=False)
    jl=os.path.join(IS,'dizin.jsonl')
    node('dizin_tara.js',os.path.join(IS,'hedef.json'),jl)
    # tam metni eksik VDDK kararları
    ids=[]
    for l in open(jl,encoding='utf-8'):
        o=json.loads(l)
        if 'id' in o and o['daire'] in TAM_METIN:
            y=o['karar'].split('/')[0]; p=os.path.join(DANISTAY,DAIRE[o['daire']],y,f"E{o['esas'].replace('/','-')}_K{o['karar'].replace('/','-')}.md")
            if not os.path.exists(p): ids.append(o['id'])
    open(os.path.join(IS,'ids.txt'),'w').write('\n'.join(ids))
    if ids: node('metin_cek.js',os.path.join(IS,'ids.txt'),os.path.join(IS,'metin'))
    # mevcut dizinle birleştir (eski satırlar korunur) ve yaz
    mevcut=os.path.join(IS,'mevcut.jsonl')
    with open(mevcut,'w',encoding='utf-8') as w:
        for x in hedef:
            f=os.path.join(DANISTAY,'dizin',f"{DAIRE[x['daire']]}-{x['yil']}.csv")
            if os.path.exists(f):
                for r in csv.DictReader(open(f,encoding='utf-8-sig')):
                    w.write(json.dumps({'id':r['belge_no'],'daire':r['daire'],'esas':r['esas_no'],'karar':r['karar_no'],'tarih':r['karar_tarihi'],'ksira':int(r['karar_no'].split('/')[1])},ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'-I',os.path.join(HERE,'depoya_yaz.py'),REPO,alinma,mevcut,jl,'--',os.path.join(IS,'metin')],check=True)
print('\n'.join(rapor))
open(os.path.join(IS,'rapor.txt'),'w').write('\n'.join(rapor))
