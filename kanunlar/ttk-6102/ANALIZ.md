# 6102 sayılı Türk Ticaret Kanunu — yapısal analiz

Bu dosya `araclar/analiz.py` ile madde dosyalarından otomatik üretilmiştir. Yalnızca metinde
yazanları sayar; hiçbir hukuki yorum içermez. Kaynak ve doğrulama durumu için `KAYNAK.md`.

## Sayılar

- Madde dosyası: 1551 (ana, mükerrer, harfli, ek ve geçici maddeler dahil)
- Madde numarasından sonraki ilk işlem notunda "Mülga" geçen: 20
- Parantez içi işlem notu ("Değişik: tarih-kanun no/madde" biçiminde): 138 (Değişik: 50, Ek: 48, Mülga: 40)
- İşlem notlarında adı geçen farklı kanun/KHK sayısı: 19

Not: İbare değişiklikleri çoğunlukla dipnotlarda yazıldığı için bu sayıma girmez. Tam liste için
`zz-islenemeyen-hukumler-ve-ekler.txt` dosyasındaki değişiklik tablosuna bakınız.

## Bölüm yapısı (kitap ve kısım düzeyi)

Başlık sonundaki sayılar kaynak metindeki dipnot işaretleridir.

| Bölüm | Başlık | İlk maddesi |
|---|---|---|
| BİRİNCİ KİTAP | Ticari İşletme | 11 |
| &nbsp;&nbsp;BİRİNCİ KISIM | Tacir A) Ticari işletme 1. Bütünlük ilkesi | 11 |
| &nbsp;&nbsp;İKİNCİ KISIM | Ticaret Sicili A) Kuruluş | 24 |
| &nbsp;&nbsp;ÜÇÜNCÜ KISIM | Ticaret Unvanı ve İşletme Adı A) Ticaret unvanı I - Kullanma zorunluluğu 1. Genel olarak | 39 |
| &nbsp;&nbsp;DÖRDÜNCÜ KISIM | Haksız Rekabet A) Genel olarak I - Amaç ve ilke | 54 |
| &nbsp;&nbsp;BEŞİNCİ KISIM | Ticari Defterler A) Defter tutma ve envanter I - Defter tutma yükümlülüğü | 64 |
| &nbsp;&nbsp;ALTINCI KISIM | Cari Hesap A) Tanım ve şekil | 89 |
| &nbsp;&nbsp;YEDİNCİ KISIM | Acentelik A) Genel olarak I - Tanımı | 102 |
| İKİNCİ KİTAP | Ticaret Şirketleri | 124 |
| &nbsp;&nbsp;BİRİNCİ KISIM | Genel Hükümler A) Türleri | 124 |
| &nbsp;&nbsp;İKİNCİ KISIM | Kollektif Şirket | 211 |
| &nbsp;&nbsp;ÜÇÜNCÜ KISIM | Komandit Şirket | 304 |
| &nbsp;&nbsp;DÖRDÜNCÜ KISIM | Anonim Şirket | 329 |
| &nbsp;&nbsp;BEŞİNCİ KISIM | Sermayesi Paylara Bölünmüş Komandit Şirket A) Tanımı | 564 |
| &nbsp;&nbsp;ALTINCI KISIM | Limited Şirket | 573 |
| ÜÇÜNCÜ KİTAP | Kıymetli Evrak | 645 |
| &nbsp;&nbsp;BİRİNCİ KISIM | Genel Hükümler A) Kıymetli evrakın tanımı | 645 |
| &nbsp;&nbsp;İKİNCİ KISIM | Nama Yazılı Senetler A) Tanımı | 654 |
| &nbsp;&nbsp;ÜÇÜNCÜ KISIM | Hamile Yazılı Senetler A) Tanımı | 658 |
| &nbsp;&nbsp;DÖRDÜNCÜ KISIM | Kambiyo Senetleri A) Borçlanma ehliyeti | 670 |
| &nbsp;&nbsp;BEŞİNCİ KISIM | Kambiyo Senetlerine Benzeyen Senetler ve Diğer Emre Yazılı Senetler A) Emre yazılı senet I - Tanımı | 824 |
| &nbsp;&nbsp;ALTINCI KISIM | Makbuz Senedi ve Varant A) Umumi mağazalar I - Genel olarak | 832 |
| DÖRDÜNCÜ KİTAP | Taşıma İşleri | 850 |
| &nbsp;&nbsp;BİRİNCİ KISIM | Genel Hükümler A) Taşıyıcı | 850 |
| &nbsp;&nbsp;İKİNCİ KISIM | Eşya Taşıma A) Taşıma sözleşmesinin uygulanması I - Taşıma senedi | 856 |
| &nbsp;&nbsp;ÜÇÜNCÜ KISIM | Taşınma Eşyası Taşıması A) Uygulanacak hükümler | 894 |
| &nbsp;&nbsp;DÖRDÜNCÜ KISIM | Değişik Tür Araçlar ile Taşıma A) Sözleşme | 902 |
| &nbsp;&nbsp;BEŞİNCİ KISIM | Yolcu Taşıma A) Kurallara uyma zorunluluğu | 906 |
| &nbsp;&nbsp;ALTINCI KISIM | Taşıma İşleri Komisyoncusu A) Taşıma komisyonculuğu sözleşmesi | 917 |
| BEŞİNCİ KİTAP | Deniz Ticareti | 931 |
| &nbsp;&nbsp;BİRİNCİ KISIM | Gemi | 931 |
| &nbsp;&nbsp;İKİNCİ KISIM | Donatan ve Donatma İştiraki | 1061 |
| &nbsp;&nbsp;ÜÇÜNCÜ KISIM | Kaptan A) özen yükümlülüğü | 1088 |
| &nbsp;&nbsp;DÖRDÜNCÜ KISIM | Deniz Ticareti Sözleşmeleri | 1119 |
| &nbsp;&nbsp;BEŞİNCİ KISIM | Deniz Kazaları | 1272 |
| &nbsp;&nbsp;ALTINCI KISIM | Gemi Alacakları A) Gemi alacaklısı hakkı veren alacaklar | 1320 |
| &nbsp;&nbsp;YEDİNCİ KISIM | Sorumluluğun Sınırlanması ve Petrol Kirliliği Zararının Tazmini A) Deniz alacaklarına karşı sorumluluğun sınırlanması I- Kural | 1328 |
| &nbsp;&nbsp;SEKİZİNCİ KISIM | Cebrî İcraya İlişkin Özel Hükümler A) Uygulanacak hukuk | 1350 |
| ALTINCI KİTAP | Sigorta Hukuku | 1401 |
| &nbsp;&nbsp;BİRİNCİ KISIM | Genel Hükümler A) Sigorta sözleşmesi I - Temel kavramlar 1. Tanım | 1401 |
| &nbsp;&nbsp;İKİNCİ KISIM | Sigorta Türlerine İlişkin Özel Hükümler | 1453 |

## İşlem notlarına göre en yeni 15 değişiklik

Tarih, değişikliği yapan kanunun işlem notunda yazan tarihidir. Madde sütunu, notun bulunduğu
dosyayı gösterir; dipnot ve cetveller PDF'teki sayfa konumunda durduğu için bir not nadiren
komşu maddenin dosyasında yer alabilir. Kullanmadan önce ilgili madde dosyasını açıp teyit ediniz.

| Tarih | Kanun/KHK no | İşlem | Maddeler |
|---|---|---|---|
| 04.07.2024 | 7519 | Değişik: 1 | 1259 |
| 23.05.2024 | 7511 | Ek: 3, Değişik: 1 | 375, 392, Geçici 7, Geçici 15 |
| 28.03.2023 | 7445 | Ek: 1 | 4 |
| 02.06.2022 | 7408 | Ek: 1 | 88 |
| 28.01.2021 | 7263 | Değişik: 1, Ek: 1 | 40, 373 |
| 27.12.2020 | 7262 | Ek: 4, Değişik: 2, Mülga: 1 | 64, 415, 417, 486, 489, 562, Geçici 14 |
| 16.04.2020 | 7244 | Ek: 1 | Geçici 13 |
| 06.12.2018 | 7155 | Ek: 2 | 5/A, Geçici 12 |
| 28.02.2018 | 7101 | Değişik: 3 | 4, 377, 634 |
| 15.02.2018 | 7099 | Mülga: 4, Ek: 2 | 64, 428, 430, 431, 585 |
| 20.11.2017 | KHK-696 | Ek: 2 | 401, 403 |
| 15.08.2017 | KHK-694 | Değişik: 2, Ek: 2 | 24, 25 |
| 05.06.2017 | KHK-691 | Ek: 1 | 399 |
| 15.07.2016 | 6728 | Ek: 13, Mülga: 3 | 212, 215, 335, 349, 545, 562, 566, 575, 586, 780, 781, Geçici 11 |
| 10.09.2014 | 6552 | Ek: 3 | 371, 629, Geçici 10 |

## İlk işlem notunda "Mülga" geçen maddeler

148, 170, 187, 341, 349, 351, 428, 430, 431, 458, 469, 524, 525, 526, 563, 615, 628, Geçici 2, Geçici 3, Geçici 5
