# GİB Mevzuatı (gib.gov.tr)

Gelir İdaresi Başkanlığı portalındaki mevzuatın tam metin arşivi. Kaynak: portalın
kendi API'si (`https://gib.gov.tr/api/gibportal/mevzuat/<tür>/list`). Her kayıt
bir Markdown dosyasıdır: başta künye (tür, GİB id, tarih, sayı, ilgili kanun,
kaynak bağlantısı, GİB güncelleme zamanı), ardından ilgili maddeler, ekler ve tam metin.

| Klasör | İçerik |
|---|---|
| `tebligler/` | Tüm GİB tebliğleri (konsolide metinler dahil) |
| `sirkuler/` | Tüm sirkülerler |
| `ozelgeler/` | Özelgeler — 01.09.2025'ten itibaren (daha eskisi istenirse çekilir) |
| `ic-genelgeler/`, `genel-yazilar/` | İç genelgeler, genel yazılar |
| `yonetmelikler/` | GİB'deki yönetmelikler |
| `bkk/`, `cbk/` | Bakanlar Kurulu ve Cumhurbaşkanı kararları |
| `gerekceler/` | Kanun gerekçeleri |
| `kkdf/`, `taslaklar/`, `uluslararasi/` | KKDF, taslaklar, uluslararası anlaşmalar |

Her klasörün `README.md` dosyası tarih sıralı dizindir. Yeni/değişen kayıtlar
`GUNLUK.md` dosyasına tarihli olarak eklenir.

## Güncelleme

```
python3 araclar/gib/gib_tara.py guncelle                       # günlük tarama
python3 araclar/gib/gib_tara.py guncelle --ozelge-baslangic 2024-01-01   # eski özelgeleri de ekle
```

Metinler GİB HTML'inden düz metne çevrilmiştir; tablolar `|` ile ayrılmış
satırlara dönüşür. Ek PDF'ler (ör. konsolide tebliğ PDF'leri) indirilmemiş,
bağlantıları künyede verilmiştir. Resmî dayanak gerektiğinde Resmî Gazete
metniyle karşılaştırınız.
