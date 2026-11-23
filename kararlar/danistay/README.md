# Danıştay Kararları

Danıştay vergi dairelerinin ve Vergi Dava Daireleri Kurulunun (VDDK) kararları.
Kararlar yalnızca resmî kaynaktan, **Danıştay Karar Arama** (karararama.danistay.gov.tr,
arka ucu bedesten.adalet.gov.tr) sisteminden alınır.

## Klasörler ve dosyalar

| Yol | İçerik |
|---|---|
| `vddk/<yıl>/`, `3-daire/<yıl>/`, `4-daire/<yıl>/`, `7-daire/<yıl>/`, `9-daire/<yıl>/` | Tam metni alınmış kararlar; klasör yılı **karar** yılıdır. Her karar `E<esas>_K<karar>.md` (künye + karar metni; ilk aktarımdaki 44 kararda ayrıca özet ve aynı adla `.pdf`) |
| `dizin/<daire>-<yıl>.csv` | Karar dizini: o daire ve karar yılındaki **tüm** kararların künyesi (daire, E/K, tarih, belge no, tam metin dosyası, kaynak bağlantısı) |
| `dizin/vergi-emsal-aramalari-2026-11-20.csv` | Önceki konu aramalarının (sahte belge, KDV iadesi, vergi ziyaı) 1.641 kararlık sonuç listesi |
| `../../araclar/danistay/` | Tarama betikleri: `sayim.js` (daire × yıl sayımı), `dizin_tara.js` (künye dizini), `metin_cek.js` (tam metin), `depoya_yaz.py` (depoya yazma), `guncelle.py` (haftalık güncelleme) |

## Kapsam (23.11.2026 itibarıyla)

| Daire | Karar yılı | Dizindeki karar | Tam metin |
|---|---|---|---|
| Vergi Dava Daireleri Kurulu | 2024 | 1.012 | Tamamı |
| Vergi Dava Daireleri Kurulu | 2025 | 933 | Tamamı |
| Vergi Dava Daireleri Kurulu | 2026 | 98 | Tamamı |
| 3. Daire | 2024 / 2025 / 2026 | 7.709 / 3.833 / 67 | İlk aktarımdakiler |
| 7. Daire | 2024 / 2025 / 2026 | 4.929 / 2.546 / 12 | İlk aktarımdakiler |
| 9. Daire | 2024 / 2025 | 7.939 / 4.620 | İlk aktarımdakiler |
| **Toplam** | | **33.698** | VDDK: 2.028 tekil karar |

- Dizindeki sayılar, Karar Arama'nın aynı daire ve karar yılı için verdiği toplamla birebir eşleşti.
- Karar Arama'da bazı kararlar iki ayrı belge numarasıyla kayıtlı (yeniden yüklenmiş kayıtlar). VDDK'da 15 karar böyle; eski belge numaralarından 13'ünün metni sistemde "bulunamadı" hatası veriyor, aynı kararın yeni belge numarasındaki metni alındı. Dizinde iki belge numarası da durur, tam metin dosyası tektir.
- 9. Daire 2026 ve diğer dairelerin 2026 kararları sisteme gecikmeli yükleniyor; haftalık güncellemeyle eklenir.
- İdari dava daireleri (2., 4. [19.07.2023 sonrası], 5., 6., 8., 10., 12., 13. Daire ve İDDK) bu kapsamda değil; 2024–2026 için toplam ~120.000 karar.

## Haftalık güncelleme

`python3 araclar/danistay/guncelle.py .` (depo kökünden; önce `araclar/danistay` içinde `npm install` ve `npx playwright install chromium`).
İçinde bulunulan ve önceki yıl için VDDK, 3., 7. ve 9. Dairenin karar sayısını dizinle karşılaştırır; artan daire-yılın künyelerini yeniden tarar, yeni VDDK kararlarının tam metnini çeker ve dosyaları yazar.

## Karar dosyası şablonu

Her `.md` dosyasının başında şu alanlar bulunur: `daire`, `esas_no`, `karar_no`,
`karar_tarihi`, `belge_no`, `konu_grubu`, `sonuc`, `lehine` (Mükellef / İdare / Kısmen / Usul),
`oy`, `kesinlik`, `kaynak` (resmî bağlantı), `alinma_tarihi`, `dogrulama`.
Ardından kısa özet ve karar metni gelir.

## Kurallar

1. **Karar metni değiştirilmez.** Özet ve yorum ayrı başlık altındadır ve resmî metin değildir.
2. **Künye programla doğrulanır.** E/K numarası ve karar tarihi karar metninde aranır;
   bulunamazsa `dogrulama` alanına `DOĞRULANMADI` yazılır.
3. **Gerekçenin sahibi yazılır.** VDDK "Dairenin gerekçesiyle" diyorsa özet, gerekçenin
   hangi Daireye ait olduğunu belirtir.
4. **Oy ve kesinlik gösterilir** (oybirliği/oyçokluğu; kesin / karar düzeltme yolu açık).
5. Kararlar anonimleştirilmiş hâliyle saklanır; müşteri verisi bu klasöre girmez.

## Bilinen kısıtlar (Karar Arama)

- Her arama en fazla 100 sonuç döndürür; sayfalama yoktur. Varsayılan sıralama esas numarasına göre en yeniden eskiye.
- Tırnaklı kelime öbekleri kök yakalamaz (`"sahte belge düzenle"` 0 sonuç, `"sahte belge düzenleme"` çalışır).
- Detaylı aramadaki "Karar Numarası – Yıl" alanı otomasyonla güvenilir dolmuyor.
- Karar sayfası `?aranacakKelimeler=` parametresi olmadan içerik yüklemiyor.
- 2026 kararları sisteme gecikmeli yükleniyor.
- bedesten.adalet.gov.tr'ye doğrudan API isteği güvenlik kontrolüne takılıyor; arama yalnızca sitenin kendi arayüzüyle yapılır.
- 4. Daire, Danıştay Başkanlık Kurulunun 19.07.2023 tarihli ve 2023/32 sayılı kararıyla idari dava dairesine dönüştü; 4. Daire vergi kararları 2023'te biter. Sonrasında vergi uyuşmazlıklarına 3., 7., 9. Daire ve VDDK bakar.

## Hacim (20.11.2026 sayımı, "vergi" kelimesi geçen kararlar, tüm yıllar)

| Daire | Karar sayısı |
|---|---|
| VDDK | 6.537 |
| 3. Daire | 29.979 |
| 4. Daire (19.07.2023'e kadar) | 26.392 |
| 7. Daire | 23.531 |
| 9. Daire | 32.263 |
| Tüm Danıştay (idari daireler dahil) | 199.416 |

## Kayıt geçmişi

- **23.11.2026 – İlk aktarım.** 20–23.11.2026 tarihli önceki çalışmadan (ayrı Claude hesabı):
  44 kararın tam metni ve özeti, 1.641 tekil kararlık dizin, `danistay.js` betiği.
  Önceki çalışmada 44 kararın künyesi karar metinleriyle tek tek doğrulanmış, 13 özette
  düzeltme yapılmıştı. Aktarımda künyeler PDF metniyle yeniden programla karşılaştırıldı: 44/44 eşleşti.
  Aramalar: sahte belge kullanma, sahte belge düzenleme, KDV iadesi, vergi ziyaı cezası; VDDK, 3., 4., 7. ve 9. Daire.

- **23.11.2026 – 2024–2026 taraması.** VDDK, 3., 7. ve 9. Dairenin 2024, 2025 ve 2026 karar yıllarına ait tüm kararlarının künye dizini (33.698 kayıt) ve VDDK kararlarının tamamının tam metni (2.028 tekil karar). Tüm tam metinlerde esas ve karar numarası karar metninde programla bulundu.

## İlk aktarımdaki özetli kararlar (44)

Lehine dağılımı: Mükellef 18, İdare 18, Kısmen 7, Usul 1.

### Sahte Belge Kullanma (SMİYB) (11 karar)

| Daire | Esas | Karar | Tarih | Sonuç | Lehine | Oy / kesinlik |
|---|---|---|---|---|---|---|
| Vergi Dava Daireleri Kurulu | [2026/5](vddk/2026/E2026-5_K2026-158.md) | 2026/158 | 11.03.2026 | Temyiz reddi – onama | İdare | Oybirliği, Kesin |
| Vergi Dava Daireleri Kurulu | [2024/572](vddk/2026/E2024-572_K2026-89.md) | 2026/89 | 18.02.2026 | Davalı temyizi reddi (karar düzeltme yolu açık) | Usul | Oybirliği, Karar düzeltme yolu açık |
| 3. Daire | [2025/182](3-daire/2026/E2025-182_K2026-18.md) | 2026/18 | 26.01.2026 | Kısmen onama, kısmen bozma | Kısmen | Oyçokluğu, Kesin |
| 4. Daire | [2022/4298](4-daire/2023/E2022-4298_K2023-4242.md) | 2023/4242 | 19.06.2023 | Bozma | İdare | Oyçokluğu, Metinde kesin ibaresi yok |
| 4. Daire | [2022/7460](4-daire/2023/E2022-7460_K2023-3419.md) | 2023/3419 | 08.06.2023 | Onama | Mükellef | Oyçokluğu, Metinde kesin ibaresi yok |
| 9. Daire | [2025/4070](9-daire/2025/E2025-4070_K2025-5032.md) | 2025/5032 | 24.11.2025 | Kısmen bozma, kısmen onama | Kısmen | Oybirliği, Kesin |
| 9. Daire | [2023/6981](9-daire/2025/E2023-6981_K2025-4963.md) | 2025/4963 | 19.11.2025 | Kısmen bozma | Kısmen | Oybirliği, Kesin |
| 4. Daire | [2023/3461](4-daire/2023/E2023-3461_K2023-3756.md) | 2023/3756 | 14.06.2023 | Onama | Kısmen | Oybirliği, Metinde kesin ibaresi yok |
| Vergi Dava Daireleri Kurulu | [2024/128](vddk/2026/E2024-128_K2026-32.md) | 2026/32 | 28.01.2026 | Davalı temyizi reddi – onama | Mükellef | Oyçokluğu, Kesin |
| 4. Daire | [2023/4238](4-daire/2023/E2023-4238_K2023-4840.md) | 2023/4840 | 13.07.2023 | Düzelterek onama | Kısmen | Oybirliği, Metinde kesin ibaresi yok |
| 4. Daire | [2023/3276](4-daire/2023/E2023-3276_K2023-4918.md) | 2023/4918 | 13.07.2023 | Onama | İdare | Oybirliği, Metinde kesin ibaresi yok |

### Sahte Belge Düzenleme / İştirak (14 karar)

| Daire | Esas | Karar | Tarih | Sonuç | Lehine | Oy / kesinlik |
|---|---|---|---|---|---|---|
| Vergi Dava Daireleri Kurulu | [2024/157](vddk/2025/E2024-157_K2025-1058.md) | 2025/1058 | 03.12.2025 | Israr kararı bozuldu | İdare | Oybirliği, Kesin |
| Vergi Dava Daireleri Kurulu | [2024/338](vddk/2026/E2024-338_K2026-4.md) | 2026/4 | 28.01.2026 | Davalı temyizi reddi (karar düzeltme yolu açık) | Mükellef | Oyçokluğu, Karar düzeltme yolu açık |
| Vergi Dava Daireleri Kurulu | [2024/302](vddk/2026/E2024-302_K2026-44.md) | 2026/44 | 28.01.2026 | Davalı temyizi reddi – onama | Mükellef | Oyçokluğu, Kesin |
| Vergi Dava Daireleri Kurulu | [2025/491](vddk/2025/E2025-491_K2025-1162.md) | 2025/1162 | 24.12.2025 | Israr kararı bozuldu | İdare | Oybirliği, Kesin |
| Vergi Dava Daireleri Kurulu | [2024/1135](vddk/2025/E2024-1135_K2025-1154.md) | 2025/1154 | 24.12.2025 | Israr kararı bozuldu | İdare | Oyçokluğu, Kesin |
| 3. Daire | [2025/602](3-daire/2026/E2025-602_K2026-1739.md) | 2026/1739 | 09.04.2026 | Bozma | İdare | Oyçokluğu, Kesin |
| 3. Daire | [2025/2349](3-daire/2026/E2025-2349_K2026-471.md) | 2026/471 | 09.02.2026 | Bozma | İdare | Oybirliği, Kesin |
| 4. Daire | [2023/4014](4-daire/2023/E2023-4014_K2023-4415.md) | 2023/4415 | 21.06.2023 | Bozma | Mükellef | Oybirliği, Metinde kesin ibaresi yok |
| 9. Daire | [2025/2557](9-daire/2025/E2025-2557_K2025-6054.md) | 2025/6054 | 23.12.2025 | Bozma | İdare | Oybirliği, Kesin |
| 9. Daire | [2025/2556](9-daire/2025/E2025-2556_K2025-6058.md) | 2025/6058 | 23.12.2025 | Bozma | İdare | Oybirliği, Kesin |
| Vergi Dava Daireleri Kurulu | [2024/606](vddk/2026/E2024-606_K2026-87.md) | 2026/87 | 18.02.2026 | Davalı temyizi reddi – onama | Mükellef | Oybirliği, Kesin |
| Vergi Dava Daireleri Kurulu | [2024/118](vddk/2026/E2024-118_K2026-26.md) | 2026/26 | 28.01.2026 | Kısmen bozma, kısmen temyiz reddi | Kısmen | Oyçokluğu, Kesin |
| 9. Daire | [2025/2853](9-daire/2025/E2025-2853_K2025-5672.md) | 2025/5672 | 11.12.2025 | Bozma | İdare | Oybirliği, Kesin |
| 9. Daire | [2025/2309](9-daire/2025/E2025-2309_K2025-5671.md) | 2025/5671 | 11.12.2025 | Bozma | İdare | Oybirliği, Kesin |

### KDV (ve ÖTV) İadesi (12 karar)

| Daire | Esas | Karar | Tarih | Sonuç | Lehine | Oy / kesinlik |
|---|---|---|---|---|---|---|
| 3. Daire | [2025/5178](3-daire/2026/E2025-5178_K2026-529.md) | 2026/529 | 10.02.2026 | Bozma | Mükellef | Oyçokluğu, Kesin |
| 7. Daire | [2025/1557](7-daire/2025/E2025-1557_K2025-3790.md) | 2025/3790 | 20.11.2025 | Bozma | Mükellef | Oyçokluğu, Kesin |
| Vergi Dava Daireleri Kurulu | [2025/889](vddk/2026/E2025-889_K2026-137.md) | 2026/137 | 11.03.2026 | Davalı temyizi reddi – onama | Mükellef | Oybirliği, Kesin |
| Vergi Dava Daireleri Kurulu | [2025/888](vddk/2026/E2025-888_K2026-136.md) | 2026/136 | 11.03.2026 | Davalı temyizi reddi – onama | Mükellef | Oybirliği, Kesin |
| Vergi Dava Daireleri Kurulu | [2026/84](vddk/2026/E2026-84_K2026-65.md) | 2026/65 | 18.02.2026 | Davalı temyizi reddi | Mükellef | Oyçokluğu, Kesin |
| Vergi Dava Daireleri Kurulu | [2024/642](vddk/2026/E2024-642_K2026-66.md) | 2026/66 | 18.02.2026 | Davalı temyizi reddi | Mükellef | Oyçokluğu, Kesin |
| 4. Daire | [2020/5090](4-daire/2023/E2020-5090_K2023-4743.md) | 2023/4743 | 06.07.2023 | Bozma | İdare | Oyçokluğu, Metinde kesin ibaresi yok |
| 4. Daire | [2020/1128](4-daire/2023/E2020-1128_K2023-4146.md) | 2023/4146 | 15.06.2023 | Onama | İdare | Oybirliği, Metinde kesin ibaresi yok |
| 4. Daire | [2020/3574](4-daire/2023/E2020-3574_K2023-3499.md) | 2023/3499 | 13.06.2023 | Onama (gerekçe değiştirilerek) | Mükellef | Oybirliği, Metinde kesin ibaresi yok |
| 9. Daire | [2025/4877](9-daire/2025/E2025-4877_K2025-4453.md) | 2025/4453 | 21.10.2025 | Onama (tarafların temyizleri reddi) | Kısmen | Oybirliği, Kesin |
| 3. Daire | [2025/2966](3-daire/2026/E2025-2966_K2026-427.md) | 2026/427 | 05.02.2026 | Bozma | Mükellef | Oybirliği, Kesin |
| 7. Daire | [2023/834](7-daire/2025/E2023-834_K2025-745.md) | 2025/745 | 20.02.2025 | Onama | İdare | Oyçokluğu, Kesin |

### Vergi Ziyaı, Ceza, Tahsilat ve Usul (7 karar)

| Daire | Esas | Karar | Tarih | Sonuç | Lehine | Oy / kesinlik |
|---|---|---|---|---|---|---|
| Vergi Dava Daireleri Kurulu | [2024/144](vddk/2026/E2024-144_K2026-21.md) | 2026/21 | 28.01.2026 | Davalı temyizi reddi – ısrar kararı kesinleşti | Mükellef | Oyçokluğu, Kesin |
| 7. Daire | [2025/1853](7-daire/2025/E2025-1853_K2025-4291.md) | 2025/4291 | 11.12.2025 | Bozma | Mükellef | Oyçokluğu, Kesin |
| 9. Daire | [2023/8232](9-daire/2025/E2023-8232_K2025-4529.md) | 2025/4529 | 30.10.2025 | Bozma | İdare | Oybirliği, Kesin |
| Vergi Dava Daireleri Kurulu | [2024/1081](vddk/2025/E2024-1081_K2025-1106.md) | 2025/1106 | 24.12.2025 | Israr kararı bozuldu | İdare | Oyçokluğu, Kesin |
| 3. Daire | [2025/833](3-daire/2026/E2025-833_K2026-1608.md) | 2026/1608 | 06.04.2026 | Bozma | Mükellef | Oybirliği, Kesin |
| 3. Daire | [2025/5286](3-daire/2026/E2025-5286_K2026-1564.md) | 2026/1564 | 02.04.2026 | Bozma | Mükellef | Oyçokluğu, Kesin |
| 7. Daire | [2023/2596](7-daire/2025/E2023-2596_K2025-4373.md) | 2025/4373 | 18.12.2025 | Bozma (davalı temyizi) | İdare | Oyçokluğu, Kesin |