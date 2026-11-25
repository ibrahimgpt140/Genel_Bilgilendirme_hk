# SGK mevzuatı (sosyal güvenlik)

Kaynak: mevzuat.gov.tr. `araclar/mevzuat/mevzuat_tara.py` her gün metinleri siteyle karşılaştırır, değişeni yeniler ve başlığına göre sosyal güvenlikle ilgili yeni tebliğ ve yönetmelikleri ekler (kurum içi personel, disiplin, teşkilat yönetmelikleri alınmaz).

SGK kanunları `kanunlar/tum/` altında madde madde bulunur: 5510, 506, 1479, 2925, 4447, 5434, 4857, 6331 (ayrıca 6111, 7103 vb. torba kanunlar).

**Çift kontrol (25.11.2026):** her metin (1) mevzuat.gov.tr listesindeki resmî başlıkla başlıyor mu, (2) mevzuat.gov.tr'nin ayrıca yayımladığı PDF veya Word sürümüyle kelime düzeyinde örtüşüyor mu diye denetlendi. 60 metnin 60'ı geçti; en düşük örtüşme %97,2. Tablodaki son sütun karşılaştırılan biçimi ve örtüşme oranını gösterir.

**SGK genelgeleri, genel yazıları ve diğer kurum düzenlemeleri:** `kaysis/` klasöründe — SGK'nın KAYSİS'teki (kms.kaysis.gov.tr) 1.001 mevzuatının tamamı (401 genelge, 347 genel yazı, 77 tebliğ, 56 yönetmelik, 37 usul ve esas, 18 yönerge, 30 uluslararası antlaşma ve diğerleri), 25.11.2026 itibarıyla. Ayrıntı ve çift kontrol sonuçları: `kaysis/README.md`. KAYSİS yurt dışından erişime kapalı olduğundan bu klasör günlük bulut görevinde güncellenmez; kullanıcının bilgisayarındaki tarayıcıyla yenilenir.

## Tebliğler

| RG tarihi / sayı | Tebliğ | Dosya | 2. kontrol |
|---|---|---|---|
| 31.12.2018 / 30642 (4.Mükerrer) | ÇOK TEHLİKELİ SINIFTA YER ALAN VE ONDAN FAZLA ÇALIŞANI BULUNAN İŞYERLERİNDE İŞSİZLİK SİGORTASI PRİMİ İŞVEREN PAYI TEŞVİKİNDEN YARARLANILMASINA İLİŞKİN USUL VE E | `31138-cok-tehlikeli-sinifta-yer-alan-ve-ondan-fazla-calisani-bulunan-isyerle.txt` | DOC %100.0 |
| 01.04.2015 / 29313 | EV HİZMETLERİNDE 5510 SAYILI KANUNUN EK 9 UNCU MADDESİ KAPSAMINDA SİGORTALI ÇALIŞTIRILMASI HAKKINDA TEBLİĞ | `20641-ev-hizmetlerinde-5510-sayili-kanunun-ek-9-uncu-maddesi-kapsaminda-sigo.txt` | DOC %100.0 |
| 10.06.2014 / 29026 | BANKALAR VE KAMU İDARELERİ TARAFINDAN YAPILACAK OLAN SİGORTALILIK KONTROLÜ İLE KURUM VE KURULUŞLARDAN ALINACAK BİLGİ VE BELGELERE DAİR TEBLİĞ | `19774-bankalar-ve-kamu-idareleri-tarafindan-yapilacak-olan-sigortalilik-kont.txt` | DOC %100.0 |
| 24.03.2013 / 28597 | SOSYAL GÜVENLİK KURUMU SAĞLIK UYGULAMA TEBLİĞİ | `17229-sosyal-guvenlik-kurumu-saglik-uygulama-tebligi.txt` | PDF %100.0 |
| 01.03.2013 / 28574 | TARIMSAL FAALİYETTE BULUNANLARIN PRİM BORÇLARININ SATTIKLARI TARIMSAL ÜRÜN BEDELLERİNDEN KESİNTİ YAPILMAK SURETİYLE TAHSİL EDİLMESİNE DAİR TEBLİĞ | `17166-tarimsal-faaliyette-bulunanlarin-prim-borclarinin-sattiklari-tarimsal.txt` | PDF %100.0 |
| 02.05.2012 / 28280 | GENEL SAĞLIK SİGORTASI GEÇİŞ SÜRESİNİN TAMAMLANMASI VE KURUMLARIN SAĞLIK YARDIMLARININ SOSYAL GÜVENLİK KURUMUNA DEVİR İŞLEMLERİNE İLİŞKİN TEBLİĞ | `16111-genel-saglik-sigortasi-gecis-suresinin-tamamlanmasi-ve-kurumlarin-sagl.txt` | DOC %100.0 |
| 12.05.2010 / 27579 | SOSYAL GÜVENLİK KURUMU ASGARİ İŞÇİLİK TESPİT KOMİSYONUNCA BELİRLENEN ÇEŞİTLİ İŞKOLLARINA AİT ASGARİ İŞÇİLİK ORANLARINI GÖSTERİR TEBLİĞ | `13976-sosyal-guvenlik-kurumu-asgari-iscilik-tespit-komisyonunca-belirlenen-c.txt` | PDF %100.0 |
| 14.01.2009 / 27110 | 5510 SAYILI KANUN GEREĞİNCE KENDİ ADINA VE HESABINA BAĞIMSIZ ÇALIŞANLARDAN 5 YILI AŞAN SÜREYE İLİŞKİN PRİM BORCU BULUNANLAR İÇİN YAPILACAK İŞLEMLER HAKKINDA TEB | `12789-5510-sayili-kanun-geregince-kendi-adina-ve-hesabina-bagimsiz-calisanla.txt` | DOC %100.0 |
| 09.10.2008 / 27019 | SİGORTALININ ÖLÜMÜNDE HAK SAHİBİ OLAN ANA VE BABAYA AYLIK BAĞLANMASININ TESPİTİNE İLİŞKİN TEBLİĞ | `12504-sigortalinin-olumunde-hak-sahibi-olan-ana-ve-babaya-aylik-baglanmasini.txt` | DOC %100.0 |
| 28.09.2008 / 27011 | İŞ KAZASI VE MESLEK HASTALIĞI SİGORTASI BAKIMINDAN İŞVERENİN, ÜÇÜNCÜ KİŞİLERİN VE SİGORTALILARIN SORUMLULUĞU İLE PEŞİN SERMAYE DEĞERLERİNİN HESAPLANMASIYLA İLGİ | `12491-is-kazasi-ve-meslek-hastaligi-sigortasi-bakimindan-isverenin-ucuncu-ki.txt` | DOC %100.0 |
| 28.09.2008 / 27011 | İŞVERENLERE VERİLEN DEVLET YARDIMI, TEŞVİK VE DESTEKLERDE SOSYAL GÜVENLİK KURUMUNDAN ALINACAK BORCU YOKTUR BELGESİNİN DÜZENLENMESİNE İLİŞKİN USUL VE ESASLARA DA | `12485-isverenlere-verilen-devlet-yardimi-tesvik-ve-desteklerde-sosyal-guvenl.txt` | DOC %100.0 |
| 18.08.2007 / 26617 | 506 SAYILI KANUNUN EK 5’İNCİ MADDESİNİN IV NUMARALI BENDİNİN UYGULANMASI HAKKINDA TEBLİĞ | `11525-506-sayili-kanunun-ek-5inci-maddesinin-iv-numarali-bendinin-uygulanmas.txt` | DOC %97.2 |
| 19.10.2006 / 26324 | İŞVERENLER TARAFINDAN AYLIK PRİM VE HİZMET BELGESİNİN İNTERNET ORTAMINDA SOSYAL SİGORTALAR KURUMUNA GÖNDERİLMESİNE (E-BİLDİRGE UYGULAMASI) İLİŞKİN TEBLİĞDE DEĞİ | `10705-isverenler-tarafindan-aylik-prim-ve-hizmet-belgesinin-internet-ortamin.txt` | DOC %100.0 |
| 30.05.2006 / 26183 | 2006 YILI SOSYAL SİGORTALAR KURUMU BAŞKANLIĞI İLAÇ LİSTESİ VE UYGULAMA TEBLİĞİ (SERİ NO: 2006/1) | `10350-2006-yili-sosyal-sigortalar-kurumu-baskanligi-ilac-listesi-ve-uygulama.txt` | DOC %100.0 |
| 04.05.2006 / 26158 | SOSYAL SİGORTALAR KURUMU TARAFINDAN İŞVERENLERE BORCU YOKTUR BELGELERİNİN İNTERNET ORTAMINDA VERİLMESİ (E-BORCU YOKTUR UYGULAMASI) HAKKINDA TEBLİĞ | `10256-sosyal-sigortalar-kurumu-tarafindan-isverenlere-borcu-yoktur-belgeleri.txt` | DOC %100.0 |
| 05.01.2006 / 26044 | 2005 YILI SOSYAL SİGORTALAR KURUMU BAŞKANLIĞI İLAÇ LİSTESİ VE UYGULAMA TALİMATI (Seri No: 2005/2) | `9822-2005-yili-sosyal-sigortalar-kurumu-baskanligi-ilac-listesi-ve-uygulama.txt` | DOC %100.0 |
| 22.07.2005 / 25883 | CARİ AYA AİT EK VE İPTAL NİTELİKTEKİ AYLIK PRİM VE HİZMET BELGELERİNİN İŞVERENLER TARAFINDAN İNTERNET ORTAMINDA SOSYAL SİGORTALAR KURUMUNA GÖNDERİLMESİ (E-BİLDİ | `9139-cari-aya-ait-ek-ve-iptal-nitelikteki-aylik-prim-ve-hizmet-belgelerinin.txt` | DOC %100.0 |
| 08.12.2004 / 25664 | SOSYAL SİGORTALAR KURUMU SERBEST MUHASEBECİ MALİ MÜŞAVİRLER İLE YEMİNLİ MALİ MÜŞAVİRLERCE İŞYERİ KAYITLARININ İNCELENMESİNİN USUL VE ESASLARI HAKKINDA YÖNETMELİ | `5995-sosyal-sigortalar-kurumu-serbest-muhasebeci-mali-musavirler-ile-yeminl.txt` | DOC %100.0 |
| 29.01.2004 / 25361 | SİGORTA PRİMLERİNİN HESABINA ESAS TUTULACAK KAZANÇLARIN AYLIK TUTARININ TESPİTİNDE NAZARA ALINMAYACAK OLAN YEMEK PARASI İLE ÇOCUK VE AİLE ZAMLARININ GÜNLÜK VE A | `5884-sigorta-primlerinin-hesabina-esas-tutulacak-kazanclarin-aylik-tutarini.txt` | DOC %100.0 |

Not: Muhtasar ve Prim Hizmet Beyannamesi Genel Tebliği (Sıra No: 1) `tebligler/genel-tebligler/` altındadır.

## Yönetmelikler

| RG tarihi / sayı | Yönetmelik | Dosya | 2. kontrol |
|---|---|---|---|
| 03.03.2026 / 33185 | SOSYAL GÜVENLİK KURUMU KLİNİK ARAŞTIRMALARDA SUNULAN SAĞLIK HİZMETLERİNİN ÖDENMESİNE İLİŞKİN YÖNETMELİK | `45054-sosyal-guvenlik-kurumu-klinik-arastirmalarda-sunulan-saglik-hizmetleri.txt` | PDF %100.0 |
| 24.04.2025 / 32880 | YÜKÜMLÜ ERBAŞ VE ERLERİN GENEL SAĞLIK SİGORTASI KAPSAMINDA SAĞLIK HİZMETİ SUNUCULARINDAN ALMIŞ OLDUKLARI SAĞLIK HİZMETİ GİDERLERİNDEN OLUŞAN FARK ÜCRETLERİNİN Ö | `42374-yukumlu-erbas-ve-erlerin-genel-saglik-sigortasi-kapsaminda-saglik-hizm.txt` | PDF %100.0 |
| 12.05.2023 / 32188 | SOSYAL GÜVENLİK KURUMU GENEL SAĞLIK SİGORTASI ALTERNATİF GERİ ÖDEME YÖNETMELİĞİ | `40192-sosyal-guvenlik-kurumu-genel-saglik-sigortasi-alternatif-geri-odeme-yo.txt` | PDF %100.0 |
| 03.03.2023 / 32121 | KÖMÜR VE LİNYİT MADENLERİNİN YER ALTI İŞLERİNDE MEYDANA GELEN İŞ KAZASI SONUCUNDA HAYATINI KAYBEDEN SİGORTALILARIN YAKINLARININ KAMUDA İSTİHDAMINA İLİŞKİN USUL  | `40100-komur-ve-linyit-madenlerinin-yer-alti-islerinde-meydana-gelen-is-kazas.txt` | PDF %100.0 |
| 25.08.2022 / 31934 (Mükerrer) | SOSYAL GÜVENLİK KURUMU İLAÇ GERİ ÖDEME YÖNETMELİĞİ | `39683-sosyal-guvenlik-kurumu-ilac-geri-odeme-yonetmeligi.txt` | PDF %100.0 |
| 28.09.2021 / 31612 | MALULİYET VE ÇALIŞMA GÜCÜ KAYBI TESPİTİ İŞLEMLERİ YÖNETMELİĞİ | `38968-maluliyet-ve-calisma-gucu-kaybi-tespiti-islemleri-yonetmeligi.txt` | DOC %100.0 |
| 24.09.2021 / 31608 | SOSYAL GÜVENLİK KURUMUNCA ELEKTRONİK ORTAMDA YAPILACAK TEBLİGATA İLİŞKİN YÖNETMELİK | `38955-sosyal-guvenlik-kurumunca-elektronik-ortamda-yapilacak-tebligata-ilisk.txt` | DOC %100.0 |
| 25.06.2021 / 31522 | SOSYAL GÜVENLİK KURUMU MUHASEBE YÖNETMELİĞİ | `38739-sosyal-guvenlik-kurumu-muhasebe-yonetmeligi.txt` | DOC %100.0 |
| 07.11.2018 / 30588 | SOSYAL GÜVENLİK KURUMU GENEL KURULUNUN TOPLANMASI, ÇALIŞMASI, TEMSİLCİLERİN GÖREVLENDİRİLMESİ VE YÖNETİM KURULUNUN SEÇİLMESİNE İLİŞKİN USUL VE ESASLAR HAKKINDA  | `28943-sosyal-guvenlik-kurumu-genel-kurulunun-toplanmasi-calismasi-temsilcile.txt` | DOC %100.0 |
| 31.05.2018 / 30437 | SOSYAL GÜVENLİK KURUMU ALACAKLARININ 6183 SAYILI AMME ALACAKLARININ TAHSİL USULÜ HAKKINDA KANUNUN 48/A MADDESİNE GÖRE TECİL VE TAKSİTLENDİRİLMESİNE İLİŞKİN YÖNE | `24634-sosyal-guvenlik-kurumu-alacaklarinin-6183-sayili-amme-alacaklarinin-ta.txt` | PDF %100.0 |
| 26.03.2016 / 29665 | SOSYAL GÜVENLİK KURUMU SAĞLIK HİZMETİ SATIN ALIM SÖZLEŞMELERİNİN/PROTOKOLLERİNİN HAZIRLANMASI VE AKDEDİLMESİNE İLİŞKİN YÖNETMELİK | `21480-sosyal-guvenlik-kurumu-saglik-hizmeti-satin-alim-sozlesmelerinin-proto.txt` | PDF %100.0 |
| 02.02.2016 / 29612 | TÜRKİYE İŞ KURUMU TARAFINDAN SUNULAN HİZMETLER İÇİN İŞSİZLİK SİGORTASI FONUNDAN KAYNAK AKTARIMINA İLİŞKİN USUL VE ESASLAR HAKKINDA YÖNETMELİK | `21401-turkiye-is-kurumu-tarafindan-sunulan-hizmetler-icin-issizlik-sigortasi.txt` | DOC %100.0 |
| 18.04.2014 / 28976 | GENEL SAĞLIK SİGORTASI TESCİL, PRİM VE MÜSTEHAKLIK İŞLEMLERİ YÖNETMELİĞİ | `19594-genel-saglik-sigortasi-tescil-prim-ve-mustehaklik-islemleri-yonetmelig.txt` | DOC %100.0 |
| 18.04.2014 / 28976 | GENEL SAĞLIK SİGORTASI UYGULAMALARI YÖNETMELİĞİ | `19593-genel-saglik-sigortasi-uygulamalari-yonetmeligi.txt` | PDF %100.0 |
| 06.12.2013 / 28843 | BANKALAR VE KAMU İDARELERİ TARAFINDAN YAPILACAK OLAN SİGORTALILIK KONTROLÜ İLE KURUM VE KURULUŞLARDAN BİLGİ VE BELGELERİN ALINMASINA İLİŞKİN USUL VE ESASLAR HAK | `19088-bankalar-ve-kamu-idareleri-tarafindan-yapilacak-olan-sigortalilik-kont.txt` | DOC %100.0 |
| 02.07.2013 / 28695 | SOSYAL SİGORTA YÜKSEK SAĞLIK KURULUNUN GÖREV, YETKİ, ÇALIŞMA USUL VE ESASLARI HAKKINDA YÖNETMELİK | `18541-sosyal-sigorta-yuksek-saglik-kurulunun-gorev-yetki-calisma-usul-ve-esa.txt` | DOC %100.0 |
| 28.12.2011 / 28156 | GENEL SAĞLIK SİGORTASI KAPSAMINDA GELİR TESPİTİ, TESCİL VE İZLEME SÜRECİNE İLİŞKİN USUL VE ESASLAR HAKKINDA YÖNETMELİK | `20112512-genel-saglik-sigortasi-kapsaminda-gelir-tespiti-tescil-ve-izleme-surec.txt` | PDF %100.0 |
| 13.08.2010 / 27671 | SOSYAL GÜVENLİK KURUMU İCRA MEMURLARI YÖNETMELİĞİ | `14204-sosyal-guvenlik-kurumu-icra-memurlari-yonetmeligi.txt` | DOC %100.0 |
| 12.05.2010 / 27579 | SOSYAL SİGORTA İŞLEMLERİ YÖNETMELİĞİ | `13973-sosyal-sigorta-islemleri-yonetmeligi.txt` | PDF %100.0 |
| 21.07.2009 / 27295 | SOSYAL GÜVENLİK KURUMUNA YAPILAN SİGORTALI VE İŞYERİ BİLDİRİMLERİNİN BAZI KURUMLARA YAPILMASI GEREKEN BİLDİRİMLER YERİNE GEÇMESİNE DAİR USUL VE ESASLARI HAKKIND | `13236-sosyal-guvenlik-kurumuna-yapilan-sigortali-ve-isyeri-bildirimlerinin-b.txt` | DOC %100.0 |
| 14.03.2009 / 27169 | SOSYAL GÜVENLİK KURUMU TAŞINIR SATIŞ İŞLEMLERİ YÖNETMELİĞİ | `12929-sosyal-guvenlik-kurumu-tasinir-satis-islemleri-yonetmeligi.txt` | DOC %100.0 |
| 29.09.2008 / 27012 (Mükerrer) | SOSYAL GÜVENLİK KURUMU PRİM VE İDARİ PARA CEZASI BORÇLARININ HAKEDİŞLERDEN MAHSUBU, ÖDENMESİ VE İLİŞİKSİZLİK BELGESİNİN ARANMASI HAKKINDA YÖNETMELİK | `200814174-sosyal-guvenlik-kurumu-prim-ve-idari-para-cezasi-borclarinin-hakedisle.txt` | PDF %100.0 |
| 27.09.2008 / 27010 | SOSYAL GÜVENLİK KURUMU ASGARİ İŞÇİLİK TESPİT KOMİSYONUNUN ÇALIŞMA USUL VE ESASLARI HAKKINDA YÖNETMELİK | `12462-sosyal-guvenlik-kurumu-asgari-iscilik-tespit-komisyonunun-calisma-usul.txt` | DOC %100.0 |
| 27.09.2008 / 27010 | SOSYAL GÜVENLİK KURUMUNCA 6183 SAYILI AMME ALACAKLARININ TAHSİL USULÜ HAKKINDA KANUNA GÖRE KULLANILACAK YETKİLERE İLİŞKİN YÖNETMELİK | `12464-sosyal-guvenlik-kurumunca-6183-sayili-amme-alacaklarinin-tahsil-usulu.txt` | DOC %100.0 |
| 27.09.2008 / 27010 | SERBEST MUHASEBECİ MALÎ MÜŞAVİRLER İLE YEMİNLİ MALÎ MÜŞAVİRLERCE İŞYERİ KAYITLARININ İNCELENMESİ HAKKINDA YÖNETMELİK | `12465-serbest-muhasebeci-mali-musavirler-ile-yeminli-mali-musavirlerce-isyer.txt` | DOC %100.0 |
| 23.08.2008 / 26976 | SOSYAL GÜVENLİK KURUMU SAĞLIK HİZMETLERİ FİYATLANDIRMA KOMİSYONU ÇALIŞMA USUL VE ESASLARI HAKKINDA YÖNETMELİK | `12376-sosyal-guvenlik-kurumu-saglik-hizmetleri-fiyatlandirma-komisyonu-calis.txt` | DOC %100.0 |
| 10.08.2007 / 26609 | SOSYAL GÜVENLİK KURUMU REHBERLİK VE TEFTİŞ BAŞKANLIĞI YÖNETMELİĞİ | `11502-sosyal-guvenlik-kurumu-rehberlik-ve-teftis-baskanligi-yonetmeligi.txt` | DOC %100.0 |
| 22.05.2007 / 26529 | SOSYAL GÜVENLİK KURUMUNA PRİM BORCU OLAN İŞVERENLERİN KAMUOYUNA AÇIKLANMASINA DAİR USUL VE ESASLAR HAKKINDA YÖNETMELİK | `11326-sosyal-guvenlik-kurumuna-prim-borcu-olan-isverenlerin-kamuoyuna-acikla.txt` | DOC %100.0 |
| 14.07.2006 / 26228 | KÜLTÜR YATIRIM VE GİRİŞİMLERİNE GELİR VERGİSİ STOPAJI, SİGORTA PRİMİ İŞVEREN PAYI VE SU BEDELİ İNDİRİMİ İLE ENERJİ DESTEĞİ UYGULAMASINA DAİR YÖNETMELİK | `10500-kultur-yatirim-ve-girisimlerine-gelir-vergisi-stopaji-sigorta-primi-is.txt` | DOC %100.0 |
| 13.08.2005 / 25905 | BAĞ-KUR SİGORTA YARDIMLARI İŞLEMLERİ YÖNETMELİĞİ | `9305-bag-kur-sigorta-yardimlari-islemleri-yonetmeligi.txt` | DOC %100.0 |
| 11.08.2005 / 25903 | BAĞ-KUR SİGORTALILARININ ÖDEMEK ZORUNDA BULUNDUKLARI PRİMLERİN HESAPLANMASI, ÖDENMESİ VE TAHSİLİ USULLERİ HAKKINDA YÖNETMELİK | `9286-bag-kur-sigortalilarinin-odemek-zorunda-bulunduklari-primlerin-hesapla.txt` | DOC %100.0 |
| 03.08.2005 / 25895 | BAĞ-KUR SAĞLIK SİGORTASI YARDIMLARI YÖNETMELİĞİ | `9230-bag-kur-saglik-sigortasi-yardimlari-yonetmeligi.txt` | DOC %100.0 |
| 01.08.2005 / 25893 | TARIM SİGORTALILARININ ÖDEMEK ZORUNDA OLDUKLARI PRİMLERİN HESAPLANMASI, ÖDENMESİ VE TAHSİLİ USULLERİ HAKKINDA YÖNETMELİK | `9208-tarim-sigortalilarinin-odemek-zorunda-olduklari-primlerin-hesaplanmasi.txt` | DOC %100.0 |
| 31.07.2005 / 25892 | TARIMDA KENDİ ADINA VE HESABINA ÇALIŞAN SİGORTALILARIN TESCİLİ İLE İLGİLİ İŞLEMLER, BAŞVURMA VE UYMAK ZORUNDA OLDUKLARI USUL VE ESASLAR HAKKINDA YÖNETMELİK | `9212-tarimda-kendi-adina-ve-hesabina-calisan-sigortalilarin-tescili-ile-ilg.txt` | DOC %100.0 |
| 12.01.2005 / 25698 | BAĞ-KUR İSTEĞE BAĞLI SİGORTALILIK YÖNETMELİĞİ | `7257-bag-kur-istege-bagli-sigortalilik-yonetmeligi.txt` | DOC %100.0 |
| 16.09.2004 / 25585 | TARIMDA KENDİ ADINA VE HESABINA ÇALIŞANLAR SOSYAL SİGORTALAR KANUNU KAPSAMINDA TARIMSAL FAALİYETTE BULUNANLARIN TESPİT, TESCİL VE TAKİBİ HAKKINDA YÖNETMELİK | `7175-tarimda-kendi-adina-ve-hesabina-calisanlar-sosyal-sigortalar-kanunu-ka.txt` | DOC %100.0 |
| 01.09.2004 / 25570 | İŞSİZLİK SİGORTASI FONU KAYNAKLARININ DEĞERLENDİRİLMESİNE İLİŞKİN USUL VE ESASLAR HAKKINDA YÖNETMELİK | `20047753-issizlik-sigortasi-fonu-kaynaklarinin-degerlendirilmesine-iliskin-usul.txt` | PDF %100.0 |
| 10.10.2000 / 24196 | T.C. EMEKLİ SANDIĞI GENEL MÜDÜRLÜĞÜ DİNLENME VE BAKIMEVLERİ (HUZUREVLERİ) İŞLETME YÖNETMELİĞİ | `4598-t-c-emekli-sandigi-genel-mudurlugu-dinlenme-ve-bakimevleri-huzurevleri.txt` | DOC %100.0 |
| 11.09.1990 / 20632 | T.C. EMEKLİ SANDIĞI YOKLAMA YÖNETMELİĞİ | `4589-t-c-emekli-sandigi-yoklama-yonetmeligi.txt` | DOC %100.0 |
| 12.02.1987 / 19370 | 506 SAYILI KANUNA TABİ SiGORTALILARA VE BUNLARIN EMEKLİLERİNE AÇILACAK FAİZSİZ KONUT KREDİSİ YÖNETMELİĞİ | `4353-506-sayili-kanuna-tabi-sigortalilara-ve-bunlarin-emeklilerine-acilacak.txt` | DOC %100.0 |
| 18.05.1984 / 18405 | 2925 SAYILI TARIM İŞCİLERİ SOSYAL SİGORTALAR KANUNUNUN UYGULANMASINA DAİR YÖNETMELİK | `8885-2925-sayili-tarim-iscileri-sosyal-sigortalar-kanununun-uygulanmasina-d.txt` | DOC %100.0 |
