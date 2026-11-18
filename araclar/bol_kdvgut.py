import re,os,sys
src,out=sys.argv[1],sys.argv[2]
L=open(src,encoding='utf8').read().split('\n')
TOC=next(i for i,l in enumerate(L) if re.match(r'^\s*I- MÜKELLEFİYET \.{5,}',l))
H=[("00","BAŞLANGIÇ",None),("I-A","I/A VERGİNİN KONUSU",r"^\s*I- ?MÜKELLEFİYET"),
("I-B","I/B VERGİNİN KONUSU İLE İLGİLİ ÇEŞİTLİ HUSUSLAR",r"^\s*B\.\s*VERGİNİN KONUSU İLE"),
("I-C","I/C MÜKELLEF VE VERGİ SORUMLUSU",r"^\s*C\.\s*MÜKELLEF VE VERGİ SORUMLUSU"),
("II-A","II/A İHRACAT İSTİSNASI",r"^\s*II\.\s*İSTİSNALAR"),
("II-B","II/B ARAÇLAR, KIYMETLİ MADEN VE PETROL ARAMALARI, ULUSAL GÜVENLİK",r"^\s*B\.\s*ARAÇLAR, KIYMETLİ"),
("II-C","II/C TAŞIMACILIK İSTİSNASI",r"^\s*C\.\s*TAŞIMACILIK İSTİSNASI"),
("II-D","II/D İTHALAT İSTİSNASI",r"^\s*D\.\s*İTHALAT İSTİSNASI"),
("II-E","II/E İNDİRİM VE İADE HAKKI TANINAN DİĞER İSTİSNALAR",r"^\s*E\.\s*İNDİRİM VE İADE HAKKI"),
("II-F","II/F SOSYAL VE ASKERİ AMAÇLI İSTİSNALARLA DİĞER İSTİSNALAR",r"^\s*F\.\s*SOSYAL VE ASKERİ"),
("II-G","II/G GEÇİCİ MADDELERDE YER ALAN İSTİSNALAR",r"^\s*G\.\s*GEÇİCİ MADDELERDE"),
("III-A","III/A MATRAH",r"^\s*III\. MATRAH, NİSPET"),
("III-B","III/B ORAN",r"^\s*B\.\s*ORAN\s*\d*$"),
("III-C","III/C İNDİRİM",r"^\s*C\.\s*İNDİRİM\s*\d*$"),
("IV-A1","IV/A1 İADE – GENEL AÇIKLAMA",r"^\s*IV\.\s*KDV İADESİNDE"),
("IV-A2","IV/A2 İADELERİ VERGİ İNCELEMESİNE TABİ OLANLAR",r"^\s*A2\d*\.\s*İADELERİ VERGİ"),
("IV-A3","IV/A3 İADE TUTARININ HESABI VE İADEYE DAYANAK İŞLEM VE BELGELER",r"^\s*A3\d*\.\s*İADE TUTARININ"),
("IV-B","IV/B İNDİRİMLİ TEMİNAT UYGULAMASI SİSTEMİ (İTUS)",r"^\s*B\.\s*İNDİRİMLİ TEMİNAT"),
("IV-C","IV/C HIZLANDIRILMIŞ İADE SİSTEMİ (HİS)",r"^\s*C\.\s*HIZLANDIRILMIŞ İADE"),
("IV-D","IV/D DİĞER HUSUSLAR",r"^\s*D\.\s*DİĞER HUSUSLAR"),
("V-A","V/A VERGİLENDİRME USULLERİ",r"^\s*V\.\s*VERGİNİN TARHI"),
("V-B","V/B VERGİLENDİRME DÖNEMİ VE BEYAN ESASI",r"^\s*B\.\s*VERGİLENDİRME DÖNEMİ"),
("V-C","V/C TARH İŞLEMLERİ",r"^\s*C\.\s*TARH İŞLEMLERİ"),
("V-D","V/D VERGİNİN ÖDENMESİ",r"^\s*D\.\s*VERGİNİN ÖDENMESİ"),
("VI-A","VI/A USUL HÜKÜMLERİ",r"^\s*VI\.\s*USUL HÜKÜMLERİ"),
("VI-B","VI/B ÇEŞİTLİ HUSUSLAR",r"^\s*B\.\s*ÇEŞİTLİ HUSUSLAR"),
("VI-C","VI/C YÜRÜRLÜKTEN KALDIRILAN TEBLİĞLER",r"^\s*C\.\s*YÜRÜRLÜKTEN KALDIRILAN"),
("VI-D","VI/D YÜRÜRLÜK",r"^\s*D\.\s*YÜRÜRLÜK\s*\d*$"),
("ZZ","İÇİNDEKİLER (tebliğ metnindeki)",None)]
pos=[0];start=0
for k,t,p in H[1:-1]:
    rx=re.compile(p); i=next((j for j in range(start,TOC) if rx.match(L[j])),None)
    assert i is not None,(k,start); pos.append(i); start=i+1
pos.append(TOC); pos.append(len(L))
os.makedirs(out,exist_ok=True); idx=[]
for n,(k,t,_) in enumerate(H):
    a,b=pos[n],pos[n+1]; fn=f"{n:02d}-{k}.txt"
    open(os.path.join(out,fn),'w',encoding='utf8').write('\n'.join(L[a:b])+'\n')
    idx.append((fn,t,a+1,b))
for r in idx: print("|".join(map(str,r)))
