# CLAUDE.md: Mevzuat bankasından soru yanıtlama kuralları

Bu depo YMM çalışmaları için hazırlanmış mevzuat bilgi bankasıdır. Vergi, mevzuat,
içtihat veya YMM uygulamasıyla ilgili **her soruda** yanıt önce bu depodan çekilir,
doğrulanır ve kaynağıyla birlikte verilir. Hafızadan, kaynaksız yanıt verilmez.

## 1. Zorunlu yanıt akışı

1. **Bankada ara.** Soruyla ilgili kanun maddesini, tebliği, sirküleri, özelgeyi ve
   kararı aşağıdaki haritaya göre `Grep`/`Glob` ile bul. Yalnızca başlığa bakma:
   ilgili dosyayı aç ve metni oku.
2. **Çapraz doğrula.** Aynı hükmü en az iki yerden teyit et:
   - Kanun maddesi: `kanunlar/<kanun>/` (mevzuat.gov.tr) ile `gib/kanunlar/<no>-.../` (gib.gov.tr)
   - Tebliğ: `tebligler/genel-tebligler/` (mevzuat.gov.tr) ile `gib/tebligler/` (gib.gov.tr)
   - İki kaynak farklıysa farkı yanıtta açıkça belirt ve daha güncel olanı tarihleriyle göster.
3. **Güncelliği kontrol et.** Hükmü değiştiren sonraki düzenlemeyi ara:
   - Değişiklik kanunu ve geçici maddeler
   - Yeni tebliğ, sirküler, CBK/BKK (`gib/cbk`, `gib/bkk`)
   - Yürürlük tarihleri ve iptal eden Anayasa Mahkemesi kararı (`kararlar/anayasa-mahkemesi/`)
   - Banka verisi en son şu tarihlerde alındı: kanun ve tebliğler 18.11.2026, GİB günlük taraması `gib/_durum.json` → `son_tarama`. Bu tarihten sonraki bir değişiklik olabileceğini düşünüyorsan ve ağ erişimi varsa resmî kaynağa (mevzuat.gov.tr, gib.gov.tr, resmigazete.gov.tr, karararama.danistay.gov.tr) bakarak teyit et. Teyit edemediysen bunu söyle.
4. **İçtihadı kontrol et.** Konuyla ilgili Danıştay kararları için `kararlar/danistay/dizin/*.csv` (konular sütunu) üzerinden ara. Ardından İBK ve VDDK kararlarına bak; idare görüşüyle çelişen karar varsa belirt.
5. **Yanıtı ver.** Her iddianın yanında kaynağı yazılır:
   - Mevzuat adı, madde/bölüm numarası
   - Depodaki dosya yolu (`dosya:satır`)
   - Resmî kaynak adresi (dosyanın başındaki `kaynak` alanı / `KAYNAK.md`)
   - Gerekiyorsa ilgili cümle **aynen alıntılanır**; madde metni yorumla karıştırılmaz.
6. **Bulunamazsa uydurma.** Bankada karşılığı yoksa "bankada bulunamadı" de. Genel bilgi verirsen bunu doğrulanmamış genel bilgi olarak işaretle.

## 2. Uyarı işaretleri (yanıtta mutlaka belirtilir)

- `bes_yil: ASILDI` olan özelge: 5 yılı aşmıştır, güncelliği ayrıca teyit edilmeli.
- `bes_yil: TARIHSIZ` olan özelge: tarihi yoktur, dikkatle kullanılmalı.
- `DOĞRULANMADI` ibaresi veya OCR ile alınmış metin (`ocr-metin.txt`, ör. `tebligler/3568-gt-27/`): resmî metinle karşılaştırılmamıştır, yanıtta belirtilir.
- `eski-gib-*` klasörleri (ör. `tebligler/kdv-genel-uygulama-28983/eski-gib-2026-04/`) arşiv sürümüdür. Güncel metin üst klasördedir.
- Özelgeler yalnızca soran mükellefi bağlar; genel hüküm gibi sunulmaz.
- Mülga, iptal edilmiş veya yürürlüğe girmemiş hükümlerin bu durumu belirtilir.

## 3. Kaynak haritası

| Ne aranıyor | Nerede |
|---|---|
| Temel vergi kanunları (madde madde) | `kanunlar/vuk-213`, `kdvk-3065`, `gvk-193`, `kvk-5520`, `otv-4760`, `damga-488`, `harclar-492`, `aatuhk-6183`, `smmm-ymm-3568`, `ttk-6102`, `gumruk-4458`, `serbest-bolgeler-3218`; dosyalar `madde-0029.txt`, `gecici-madde-NN.txt`, `ek-madde-NN.txt`; kaynak bilgisi `KAYNAK.md` |
| Diğer tüm kanunlar (905) | `kanunlar/tum/` (dizin `kanunlar/tum/README.md`) |
| GİB kanun metinleri (221 kanun) | `gib/kanunlar/<no>-<ad>/NNNN-<id>-madde-N.md` |
| Genel tebliğler (916) | `tebligler/genel-tebligler/<konu>/` (dizin `README.md`), ekleri `ekler/<no>/` |
| KDV Genel Uygulama Tebliği | `tebligler/kdv-genel-uygulama-28983/` (`bolumler/` bölüm bölüm) |
| YMM'ye özgü tebliğler | `tebligler/3568-gt-*`, `e-ymm-rapor-gt-1`, `ymm-karsit-inceleme-elektronik`, `ymm-sozlesme-bildirim-elektronik`, `tebligler/genel-tebligler/3568-smmm-ymm/` |
| Yönetmelikler | `yonetmelikler/` ve `gib/yonetmelikler/` |
| Tüzükler | `tuzukler/` |
| GİB tebliğ, sirküler, iç genelge, genel yazı | `gib/tebligler`, `gib/sirkuler`, `gib/ic-genelgeler`, `gib/genel-yazilar` |
| CBK / BKK, KKDF, gerekçeler, taslaklar | `gib/cbk`, `gib/bkk`, `gib/kkdf`, `gib/gerekceler`, `gib/taslaklar` |
| Özelgeler (18.435) | `gib/ozelgeler/` (frontmatter: `tarih`, `kanun`, `bes_yil`, `kaynak`) |
| Çifte vergilendirmeyi önleme anlaşmaları (94 ülke) | `gib/uluslararasi/cvoa/` |
| Danıştay 3./4./7./9. Daire ve VDDK | `kararlar/danistay/<daire>/<yıl>/E..._K....md`; dizin `kararlar/danistay/dizin/*.csv` |
| İBK kararları ve VDDK bültenleri | `kararlar/danistay/ibk/`, `kararlar/danistay/vddk-bultenleri/` |
| Anayasa Mahkemesi | `kararlar/anayasa-mahkemesi/` (`konular.md`, `_dizin.json`) |
| Kılavuzlar | `kilavuzlar/` |
| Kaynak PDF'ler | `kaynak-dosyalar/` |

Arama ipuçları: Türkçe karakterli ve karaktersiz biçimleri birlikte dene
(ör. `istisna|istisnâ`, `ğ/g`, `ı/i`). Madde numarasıyla ararken `Madde 29 –` ve
`MADDE 29-` biçimlerinin ikisine de bak. Büyük klasörlerde önce dizin/README dosyalarını tara.

## 4. Depo kuralları

1. Müşteri verisi (VKN, unvan, defter, beyanname vb.) bu depoya girmez.
2. Metinler resmî kaynaktan alınır; her dosyanın başında kaynak ve alınma tarihi bulunur.
3. Madde metni değiştirilmez; yorum ve notlar ayrı dosyada tutulur.
4. Doğrulanmamış içerik `DOĞRULANMADI` ile işaretlenir.
