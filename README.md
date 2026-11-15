# YMM Mevzuat Bilgi Bankası

Yeminli mali müşavirlik çalışmalarında kullanılan mevzuatın sürümlü arşivi.
Her değişiklik tarihli bir kayıt olarak tutulur; bir maddenin geçmişteki hali
dosyanın geçmişinden (History) görülebilir.

## Klasörler

| Klasör | İçerik |
|---|---|
| `kanunlar/vuk-213/` | 213 sayılı Vergi Usul Kanunu, madde madde |
| `kanunlar/ttk-6102/` | 6102 sayılı Türk Ticaret Kanunu, madde madde |
| `kanunlar/gumruk-4458/` | 4458 sayılı Gümrük Kanunu, madde madde |
| `tebligler/` | Genel tebliğler, sirküler ve özelgeler |
| `resmi-gazete/` | Günlük Resmî Gazete taramasının özetleri |
| `sablonlar/` | Boş rapor, dilekçe ve izahat şablonları |
| `kontrol-listeleri/` | Rapor denetim kontrol listeleri |
| `kaynak-dosyalar/` | mevzuat.gov.tr'den indirilen resmî PDF/Word dosyaları |
| `araclar/` | Kanun metnini maddelere bölen betik (`bol.py`) |

## Kurallar

1. **Müşteri verisi bu depoya girmez.** VKN, unvan, defter, beyanname, sözleşme
   gibi hiçbir mükellef bilgisi burada tutulmaz; yalnızca mevzuat ve boş şablon.
2. **Metinler resmî kaynaktan alınır.** Her kanun dosyasının başında kaynak
   adresi ve alındığı tarih yazar.
3. **Madde metni değiştirilmez.** Yorum ve not gerekiyorsa ayrı dosyada tutulur.
4. **Doğrulanmamış içerik işaretlenir.** Resmî metinle karşılaştırılmamış her
   dosyanın başında `DOĞRULANMADI` ibaresi bulunur.
