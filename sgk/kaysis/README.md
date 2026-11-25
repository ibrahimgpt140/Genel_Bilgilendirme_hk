# SGK mevzuatı — KAYSİS (kms.kaysis.gov.tr)

Kaynak: Sosyal Güvenlik Kurumu Başkanlığının KAYSİS kurum sayfası (https://kms.kaysis.gov.tr/Home/Kurum/22620739). Son güncelleme: 25.11.2026.
KAYSİS yurt dışından erişime kapalı olduğundan belgeler kullanıcının bilgisayarındaki tarayıcıdan resmî PDF olarak alınır (`araclar/sgk/kaysis_indir.js`) ve `araclar/sgk/kaysis_isle.py` ile metne çevrilir. Her dosyanın başında kaynak bağlantısı, sayı, SHA-256 ve kontrol sonucu yazar.

**Çift kontrol:** (1) indirilen belgenin boyutu KAYSİS'in gönderdiğiyle eşleşiyor ve SHA-256 değeri dosyanın başına yazıldı; (2) belgenin sayısı ya da başlığı metnin başında (ilk ~20.000 karakter) geçiyor. 1003 kaydın 989'i iki kontrolden de geçti. 13 belgede sayı/başlık metnin başında bulunamadı; bunlar ek/form, içindekiler sayfası ya da Resmî Gazete sayfa başlığıyla başlıyor (aşağıda listeli, içerik elle teyit edilmeli). 1 kaydın KAYSİS'te dosyası yok (yalnızca künye). 286 taranmış ya da metin katmanı bozuk PDF Türkçe OCR ile metne çevrildi (dosyalarında işaretli; OCR hatası olabileceğinden rakam ve tarihleri kaynak PDF'ten teyit ediniz). 36 belge KAYSİS'te PDF yerine HTML olarak sunuluyor; metni HTML'den alındı.

Not: KAYSİS'teki genelgeler ve genel yazılar Resmî Gazete'de yayımlanmaz; SGK'nın kendi düzenlemeleridir. Yeni kayıtlar, kullanıcının bilgisayarında çalışan günlük görevle eklenir.

| Klasör | Kategori | Adet |
|---|---|---|
| `genelgeler/` | Kurum Genelgeleri | 402 |
| `genel-yazilar/` | Genel Yazılar | 348 |
| `tebligler/` | Tebliğler | 77 |
| `yonetmelikler/` | Kurum Yönetmelikleri | 56 |
| `usul-ve-esaslar/` | Esas ve Usuller | 37 |
| `uluslararasi-antlasmalar/` | Uluslararası Antlaşmalar | 30 |
| `yonergeler/` | Yönergeler | 18 |
| `talimatlar/` | Talimat/Talimatname/İç emirler | 14 |
| `protokoller/` | Sözleşme / Protokoller | 12 |
| `kanunlar/` | Kanunlar | 4 |
| `bakanlar-kurulu-kararlari/` | Bakanlar Kurulu Kararları | 3 |
| `kurul-kararlari/` | Kurul / Komisyon / Konsey Kararları | 2 |

Tam liste: `dizin.csv`.

## Sayı/başlık metinde bulunamayanlar (elle bakılmalı)

- `uluslararasi-antlasmalar/2004-6753-turkiye-cumhuriyeti-hukumeti-ile-kebek-hukumeti-arasinda-sosyal-guvenl`
- `uluslararasi-antlasmalar/2003-6316-turkiye-cumhuriyeti-hukumeti-ile-gurcistan-hukumeti-arasinda-sosyal-gu`
- `yonetmelikler/2026-149-sosyal-guvenlik-kurumu-merkez-teskilati-calisma-yonetmeligi`
- `genelgeler/2020-22-5434-sayili-kanuna-tabi-olanlarin-is-ve-islemlerine-iliskin-2020-22-sa`
- `genelgeler/2020-22-5434-sayili-kanuna-tabi-olanlarin-is-ve-islemlerine-iliskin-2020-22-sa-206602`
- `genelgeler/2014-11-2013-39-sayili-genelgede-degisiklik-yapilmasi-hakkinda-genelge`
- `genelgeler/2012-26-unvan-bazinda-is-gorev-tanimlari-kitabi-revizyonu-hakkinda-genelge`
- `genelgeler/2010-68-almanyadaki-cocuk-yetistirme-sureleri-hakkinda-2010-68-sayili-genelge`
- `tebligler/2020-2-saglik-hizmetleri-fiyatlandirma-komisyonu-karari`
- `tebligler/2018-5-saglik-hizmetleri-fiyatlandirma-komisyonu-karari`
- `genel-yazilar/1447472-09-03-2018-tarihli-1447472-sayili-4-1-b-gunluk-odeme-konulu-genel-yazi`
- `genel-yazilar/7845553-prim-borclarinin-hakedislerinden-mahsubu-hakkinda-yazi`
- `genel-yazilar/20541-adli-tebligata-iliskin-07-07-2011-tarih-ve-20541-sayili-genel-yazi`
