# Vergi ve Ticaret Mevzuatı Arşivi

Vergi, ticaret ve gümrük mevzuatının sürümlü arşivi.
Her değişiklik tarihli bir kayıt olarak tutulur; bir maddenin geçmişteki hali
dosyanın geçmişinden (History) görülebilir.

## Klasörler

| Klasör | İçerik |
|---|---|
| `kanunlar/vuk-213/` | 213 sayılı Vergi Usul Kanunu, madde madde |
| `kanunlar/ttk-6102/` | 6102 sayılı Türk Ticaret Kanunu, madde madde |
| `kanunlar/gumruk-4458/` | 4458 sayılı Gümrük Kanunu, madde madde |
| `kanunlar/kdvk-3065/`, `kvk-5520/`, `gvk-193/`, `smmm-ymm-3568/`, `aatuhk-6183/`, `damga-488/`, `harclar-492/`, `otv-4760/`, `serbest-bolgeler-3218/` | KDV, Kurumlar, Gelir, 3568, 6183, Damga, Harçlar, ÖTV ve Serbest Bölgeler kanunları, madde madde (18.11.2026) |
| `kanunlar/tum/` | mevzuat.gov.tr'deki diğer tüm yürürlükteki kanunlar (905), dizin: `kanunlar/tum/README.md` |
| `tuzukler/` | Yürürlükteki tüm tüzükler (107) |
| `tebligler/genel-tebligler/` | Yürürlükteki tüm genel tebliğler (916), konu klasörlerine ayrılmış; dizin: `README.md` |
| `yonetmelikler/` | YMM tasdik, çalışma usul ve esasları, vergi incelemesi, ticaret sicili, belge basım, gümrük yönetmelikleri |
| `tebligler/` | Genel tebliğler, sirküler ve özelgeler |
| `kararlar/danistay/` | Danıştay vergi daireleri ve VDDK kararları (künye + özet + tam metin), karar dizini (`dizin/`), İçtihatları Birleştirme Kurulu kararları (`ibk/`, 98 karar) ve VDDK karar bültenleri ile bültenlerdeki 644 Kurul kararı (`vddk-bultenleri/`) |
| `resmi-gazete/` | Günlük Resmî Gazete taramasının özetleri |
| `sablonlar/` | Boş rapor, dilekçe ve izahat şablonları |
| `kontrol-listeleri/` | Rapor denetim kontrol listeleri |
| `kaynak-dosyalar/` | mevzuat.gov.tr'den indirilen resmî PDF/Word dosyaları |
| `gib/` | gib.gov.tr mevzuatı: 221 kanun madde madde, tüm tebliğ, sirküler, iç genelge, genel yazı, BKK/CBK, gerekçe ve tüm özelgeler (5 yılı aşanlar işaretli); günlük güncellenir (`araclar/gib/gib_tara.py`) |
| `gib/uluslararasi/cvoa/` | Çifte vergilendirmeyi önleme anlaşmaları: 94 ülke, ÇVÖA özelgeleri ve tebliğleri (gib.gov.tr) |
| `kararlar/anayasa-mahkemesi/` | Anayasa Mahkemesinin vergiyle ilgili 595 norm denetimi ve 379 bireysel başvuru kararı, konu başlıklarına göre dizinli (anayasa.gov.tr) |
| `kilavuzlar/` | GİB kılavuzları ve analizleri |
| `araclar/` | Toplu paket işleme (`toplu_isle.py`), maddelere bölme (`bol.py`), yapısal analiz (`analiz.py`), eski GİB KDVGUT PDF metni için bölüm ayırma (`bol_kdvgut.py`) ve Danıştay Karar Arama tarama betikleri (`danistay/`) |

## Kurallar

1. **Müşteri verisi bu depoya girmez.** VKN, unvan, defter, beyanname, sözleşme
   gibi hiçbir mükellef bilgisi burada tutulmaz; yalnızca mevzuat ve boş şablon.
2. **Metinler resmî kaynaktan alınır.** Her kanun dosyasının başında kaynak
   adresi ve alındığı tarih yazar.
3. **Madde metni değiştirilmez.** Yorum ve not gerekiyorsa ayrı dosyada tutulur.
4. **Doğrulanmamış içerik işaretlenir.** Resmî metinle karşılaştırılmamış her
   dosyanın başında `DOĞRULANMADI` ibaresi bulunur.
