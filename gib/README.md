# GİB Mevzuatı (gib.gov.tr)

Gelir İdaresi Başkanlığı portalındaki mevzuatın tam metin arşivi. Kaynak: portalın
kendi API'si (`https://gib.gov.tr/api/gibportal/mevzuat/<tür>/list`). Her kayıt
bir Markdown dosyasıdır: başta künye (tür, GİB id, tarih, sayı, ilgili kanun,
kaynak bağlantısı, GİB güncelleme zamanı), ardından ilgili maddeler, ekler ve tam metin.

| Klasör | İçerik |
|---|---|
| `kanunlar/` | GİB'deki 221 kanun, madde madde (7.005 madde; maddelerin önceki halleriyle) |
| `tebligler/` | Tüm GİB tebliğleri (konsolide metinler dahil) |
| `sirkuler/` | Tüm sirkülerler |
| `ozelgeler/` | GİB'deki tüm özelgeler (18.435); 5 yılı aşanlar ⚠, tarihsizler ? ile işaretli |
| `ic-genelgeler/`, `genel-yazilar/` | İç genelgeler, genel yazılar |
| `yonetmelikler/` | GİB'deki yönetmelikler |
| `bkk/`, `cbk/` | Bakanlar Kurulu ve Cumhurbaşkanı kararları |
| `gerekceler/` | Kanun gerekçeleri |
| `kkdf/`, `taslaklar/` | KKDF, taslaklar |
| `uluslararasi/` | Uluslararası anlaşma sayfaları; **`uluslararasi/cvoa/`**: çifte vergilendirmeyi önleme anlaşmaları (94 ülke, 107 metin), 228 ÇVÖA özelgesi, 4 genel tebliğ, oran tabloları; `uluslararasi/dosyalar/`: bilgi değişimi, AB ve diğer anlaşmalar dahil 611 dosya (PDF + metin, taranmışlar OCR'lı). 6 bağlantı GİB tarafında bozuk (`_indirme.json`). Araç: `araclar/gib/uluslararasi_cek.py` |

Her klasörün `README.md` dosyası tarih sıralı dizindir. Yeni/değişen kayıtlar
`GUNLUK.md` dosyasına tarihli olarak eklenir.

## 5 yıl kuralı

Belgeler 5 yıl sonunda geçersiz sayılır. Özelgelerin tamamı tutulur, ancak 5 yılı aşanlar
işaretlenir. Künyede `bes_yil: gecerli/ASILDI` alanı, dizinde ⚠ sütunu bulunur; o gün 5 yılı
dolan özelgeler `GUNLUK.md`'ye yazılır. Tebliğ, sirküler, genel yazı, BKK/CBK vb. mevzuat
metinleri yürürlükten kaldırılana kadar geçerli olduğundan tarih sınırı olmadan, güncel
halleriyle tamamı tutulur.

## Güncelleme

```
python3 araclar/gib/gib_tara.py guncelle                       # günlük tarama
```

Metinler GİB HTML'inden düz metne çevrilmiştir; tablolar `|` ile ayrılmış
satırlara dönüşür. Ek PDF'ler (ör. konsolide tebliğ PDF'leri) indirilmemiş,
bağlantıları künyede verilmiştir. Resmî dayanak gerektiğinde Resmî Gazete
metniyle karşılaştırınız.
