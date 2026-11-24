# 213 sayılı Vergi Usul Kanunu — yapısal analiz

Bu dosya `araclar/analiz.py` ile madde dosyalarından otomatik üretilmiştir. Yalnızca metinde
yazanları sayar; hiçbir hukuki yorum içermez. Kaynak ve doğrulama durumu için `KAYNAK.md`.

## Sayılar

- Madde dosyası: 470 (ana, mükerrer, harfli, ek ve geçici maddeler dahil)
- Madde numarasından sonraki ilk işlem notunda "Mülga" geçen: 38
- Parantez içi işlem notu ("Değişik: tarih-kanun no/madde" biçiminde): 524 (Ek: 277, Değişik: 180, Mülga: 59, Diğer: 8)
- İşlem notlarında adı geçen farklı kanun/KHK sayısı: 68

Not: İbare değişiklikleri çoğunlukla dipnotlarda yazıldığı için bu sayıma girmez. Tam liste için
`zz-islenemeyen-hukumler-ve-ekler.txt` dosyasındaki değişiklik tablosuna bakınız.

## Bölüm yapısı (kitap ve kısım düzeyi)

Başlık sonundaki sayılar kaynak metindeki dipnot işaretleridir.

| Bölüm | Başlık | İlk maddesi |
|---|---|---|
| BİRİNCİ KİTAP | Vergilendirme | 4 |
| &nbsp;&nbsp;BİRİNCİ KISIM | Genel Esaslar | 4 |
| &nbsp;&nbsp;İKİNCİ KISIM | Tarh ve Tahakkuk Usulü | 25 |
| &nbsp;&nbsp;ÜÇÜNCÜ KISIM | Tahrir Usulü | 50 |
| &nbsp;&nbsp;DÖRDÜNCÜ KISIM | Takdir, Zirai Kazançlar ve Özel Komisyonları14 | 72 |
| &nbsp;&nbsp;BEŞİNCİ KISIM | Tebliğler | 93 |
| &nbsp;&nbsp;ALTINCI KISIM | Vergi Alacağının Kalkması | 110 |
| &nbsp;&nbsp;YEDİNCİ KISIM | Yoklama ve inceleme | 127 |
| İKİNCİ KİTAP | Mükellefin Ödevleri | 153 |
| &nbsp;&nbsp;BİRİNCİ KISIM | Bildirmeler | 153 |
| &nbsp;&nbsp;İKİNCİ KISIM | Defter Tutma | 171 |
| &nbsp;&nbsp;ÜÇÜNCÜ KISIM | Vesikalar | 227 |
| &nbsp;&nbsp;DÖRDÜNCÜ KISIM | Ekim ve Sayım Beyanı | 243 |
| &nbsp;&nbsp;BEŞİNCİ KISIM | Vergi Karnesi Vergi karnesi: Karne mecburiyeti: | 247 |
| &nbsp;&nbsp;ALTINCI KISIM | Muhafaza ve İbraz Ödevleri | 253 |
| ÜÇÜNCÜ KİTAP | Değerleme | 258 |
| &nbsp;&nbsp;BİRİNCİ KISIM | İktisadi Kıymet Değerleri | 258 |
| &nbsp;&nbsp;İKİNCİ KISIM | Vergi Değerleri | 299 |
| &nbsp;&nbsp;ÜÇÜNCÜ KISIM | Amortismanlar | 313 |
| DÖRDÜNCÜ KİTAP | Ceza Hükümleri | 331 |
| &nbsp;&nbsp;BİRİNCİ KISIM | Genel Esaslar | 331 |
| &nbsp;&nbsp;İKİNCİ KISIM | Vergi Cezaları | 344 |
| &nbsp;&nbsp;ÜÇÜNCÜ KISIM | Vergi Cezasının Kesilmesi, Ödenmesi ve Kalkması | 364 |
| BEŞİNCİ KİTAP | Vergi Davaları168 | 377 |

## İşlem notlarına göre en yeni 15 değişiklik

Tarih, değişikliği yapan kanunun işlem notunda yazan tarihidir. Madde sütunu, notun bulunduğu
dosyayı gösterir; dipnot ve cetveller PDF'teki sayfa konumunda durduğu için bir not nadiren
komşu maddenin dosyasında yer alabilir. Kullanmadan önce ilgili madde dosyasını açıp teyit ediniz.

| Tarih | Kanun/KHK no | İşlem | Maddeler |
|---|---|---|---|
| 24.06.2026 | 7587 | Değişik: 1, Ek: 1 | 107/A, Geçici 38 |
| 24.12.2025 | 7571 | Ek: 1 | Geçici 37 |
| 20.07.2025 | 7555 | Ek: 1 | 131 |
| 25.12.2024 | 7537 | Ek: 1 | Geçici 36 |
| 24.10.2024 | 7529 | Ek: 2 | Mükerrer 298, Geçici 33 |
| 28.07.2024 | 7524 | Ek: 12, Mülga: 10, Değişik: 3, Diğer: 1 | 112, 153/A, 274/A, 344, 353, Mükerrer 355, 376, 417, Ek 1, Ek 7, Ek 11, Ek 13, Geçici 35 |
| 27.12.2023 | 7491 | Ek: 2 | Mükerrer 413, Geçici 33 |
| 30.11.2022 | 7423 | Ek: 1 | 359 |
| 16.11.2022 | 7421 | Ek: 1 | Mükerrer 257 |
| 01.07.2022 | 7417 | Ek: 3 | Mükerrer 257, Mükerrer 355 |
| 08.04.2022 | 7394 | Ek: 7 | 4, 359, 367, Geçici 34 |
| 20.01.2022 | 7352 | Ek: 1 | Geçici 33 |
| 14.10.2021 | 7338 | Ek: 42, Değişik: 9, Mülga: 5 | 4, 5, 97, 104, 120, 139, 140, 170/A, 226/A, Mükerrer 227, 234, Mükerrer 242, 261, 262, 268/A, 270, 273, Mükerrer 298, 318, 320, 323, 328, 329, 339, 353, 371, Ek 1, Ek 11, Ek 14, Ek 15, Ek 16, Ek 17, Ek 18, Geçici 30, Geçici 32 |
| 03.06.2021 | 7326 | Ek: 1 | Geçici 31 |
| 29.04.2021 | 7318 | Ek: 5 | 231, Mükerrer 257, Mükerrer 355, 359, 367 |

## İlk işlem notunda "Mülga" geçen maddeler

40, 41, 50, 51, 53, 56, 77, 78, Mükerrer 86, Mükerrer 185, Mükerrer 194, Mükerrer 196, 201, 202, 206, 270, 319, 338, 345, 346, 347, Mükerrer 347, 348, 349, 350, 354, Mükerrer 354, 356, 357, 358, 361, 370, Mükerrer 415, Ek 2, Ek 3, Ek 4, Ek 5, Ek 10
