#!/usr/bin/env python3
"""GİB 'KDV İade Taleplerine Ait Listeleri Gönderme Kılavuzu' (Mart 2022) içindeki
sayısal örneklerin yeniden hesaplanması. Değerler kılavuzun metninden ve resimlerinden
okunmuştur; her kontrolün yanında sayfa numarası yazar."""
from decimal import Decimal as D
sonuc = []
def kontrol(sayfa, ad, hesap, belgede, not_=""):
    ok = (hesap == belgede) if isinstance(hesap, bool) else D(str(hesap)) == D(str(belgede))
    sonuc.append((sayfa, ad, hesap, belgede, ok, not_))
def T(*x): return sum(D(str(v)) for v in x)

# --- Metindeki örnekler ---
kontrol(16, "(100x%8)+(200x%18)", D(100)*D("0.08")+D(200)*D("0.18"), 44)
kontrol(16, "100+200 KDV hariç tutar", 100+200, 300)
kontrol(25, "3.800 x %18", D(3800)*D("0.18"), 684)
kontrol(25, "4.200 x %18", D(4200)*D("0.18"), 756)
kontrol(25, "684+756 (tablo toplamı)", 684+756, 1440)
kontrol(36, "(1.000x%8)+(2.000x%18)", D(1000)*D("0.08")+D(2000)*D("0.18"), 440)
kontrol(36, "10.000 x %18", D(10000)*D("0.18"), 1800)
kontrol(36, "1.800 x 5/10 tevkifat", D(1800)*5/10, 900)
kontrol(36, "1.000 x %8 x 1/2 tevkifat", D(1000)*D("0.08")/2, 40)
kontrol(37, "2.000 x %18 x 2/3 tevkifat", D(2000)*D("0.18")*2/3, 240)
kontrol(37, "40+240 toplam tevkifat", 40+240, 280)
kontrol(48, "100.000 x %18 azami iade", D(100000)*D("0.18"), 18000)
kontrol(49, "60.000 x %18", D(60000)*D("0.18"), 10800)
kontrol(49, "20.000 x %18", D(20000)*D("0.18"), 3600)
kontrol(49, "40.000 x %18", D(40000)*D("0.18"), 7200)
kontrol(49, "10.800+3.600", 10800+3600, 14400)
kontrol(49, "18.000-14.400 ATİK payı üst sınırı", 18000-14400, 3600)
kontrol(49, "10.800+3.600+3.600", 10800+3600+3600, 18000)

# --- Resimlerdeki tablolar ---
kontrol(12, "İndirilecek KDV (sistem ekranı) matrah toplamı", T(1000, 5000, 25750, 15000, 10000, 1250, 45000), 103000)
kontrol(12, "İndirilecek KDV (sistem ekranı) KDV toplamı", T(180, 500, 4635, 1500, 800, 150, 450), 8215)
m13 = [3000, "32380.91", 7738, 1190, 10000, 3500, 16, 96, 180, 10000, 14000, 4200, 1200]
k13 = [540, "5828.60", "1392.80", "214.20", 1800, 630, "1.30", "7.70", "32.40", 1800, 1120, 362, 216]
kontrol(13, "İndirilecek KDV Listesi matrah toplamı", T(*m13), "87500.91")
kontrol(13, "İndirilecek KDV Listesi KDV toplamı", T(*k13), "13945.00")
kontrol(13, "Muhasebe fişi KDV'si (362) <= toplam KDV'nin %5'i", D(362) <= T(*k13)*D("0.05"), True,
        f"%5 sınırı = {T(*k13)*D('0.05')}")
kontrol(17, "406 örneği matrah toplamı", T(10000, 25000, 5000, 2000, 5000, 500), 47500)
kontrol(17, "406 örneği KDV toplamı", T(1800, 2500, 500, 200, 900, 50), 5950)
m19 = [10000,25000,5000,2000,5000,500,3100,2500,6500,40000,250000,150000,150,300000,60000,17500,98500,10000,6550,74500,650000,300000,50,10000]
k19 = [1800,2500,500,200,900,50,450,300,325,4000,30000,15000,10,36000,6500,1750,10000,900,650,7500,65000,3000,5,1000]
kontrol(19, "439 yıllık örnek matrah toplamı (24 satır)", T(*m19), "2026850.00")
kontrol(19, "439 yıllık örnek KDV toplamı (24 satır)", T(*k19), "188340.00")
kontrol(20, "Yüklenilen KDV (sistem ekranı) bünyeye giren toplam", T(2500, 500, 2000, 80, 1000), 6080)
kontrol(20, "Yüklenilen KDV (sistem ekranı) KDV toplamı", T(4500, 1800, 2500, 120, 4500), 13420)
kontrol(20, "Yüklenilen KDV (sistem ekranı) matrah toplamı", T(45000, 10000, 25000, 1200, 45000), 126200)
kontrol(21, "Yüklenilen KDV (Excel) bünyeye giren toplam", T(2500, 500, 2000, 80, 500), 5580)
kontrol(34, "Tevkifatlı satış matrah toplamı", T(10000, 15000, 20000, 100000, 30000), 175000)
kontrol(34, "Tevkifatlı satış KDV toplamı", T(1800, 2250, 3600, 18000, 5400), 31050)
kontrol(34, "Tevkifatlı satış tevkif edilen KDV toplamı", T(900, 1125, 1800, 16200, 3780), 23805)
kontrol(39, "İhraç kayıtlı matrah toplamı", T(10000, 25000, 250000, 50000, 50000, 4000, 65000), 454000)
kontrol(39, "İhraç kayıtlı KDV toplamı", T(1800, 1000, 20000, 9000, 9000, 450, 6000), 47250)
kontrol(44, "318/320/321 listesi toplamı", T("2208.68", "7775.33", "3535.31", 9500), "23019.32")
kontrol(46, "318+321 tablo toplamı", T(1530000, 322000), 1852000)
for i, (a, b, c, t) in enumerate([(10000, 1000, 500, 11500), (1000, 100, 250, 1350), (50000, 5000, 0, 55000)], 1):
    kontrol(47, f"Hesaplama tablosu (sistem) satır {i}", T(a, b, c), t)
kontrol(47, "Hesaplama tablosu (sistem) Toplam Yüklenilen KDV", T(11500, 1350, 55000), 67850)
for i, (a, b, c, t) in enumerate([(10800, 3600, 3600, 18000), (35000, 5000, 0, 40000), (100000, 50000, 10000, 160000)], 1):
    kontrol(48, f"Hesaplama tablosu (Excel) satır {i}", T(a, b, c), t)
kontrol(48, "Hesaplama tablosu (Excel) TOPLAM", T(18000, 40000, 160000), 218000)
kontrol(48, "406 satırı azami iade = 1.000.000 x (%18-%1)", D(1000000)*D("0.17"), 170000)
kontrol(54, "İndirimli oran satış (sistem) matrah toplamı", T(1000, 100, 1000, 100, 10000), 12200)
kontrol(55, "İndirimli oran satış (Excel) matrah toplamı", T(100, 10000, 1000), 11100)
kontrol(55, "İndirimli oran satış (Excel) KDV toplamı", T(1, 800, 10), 811)
kontrol(60, "Yatırım teşvik (sistem) toplam", T(100000, 10000000, 45000), 10145000)
kontrol(61, "Yatırım teşvik (Excel) toplam", T(100000, 50000, 800000, 100000), 1050000)
kontrol(64, "Uluslararası anlaşmalar toplam", T(50000, 250000, 100000), 400000)
kontrol(67, "13. madde (sistem) toplam", T(1500, 1500, 1500, 1500, 1500), 7500)
kontrol(68, "13. madde (Excel) TOPLAM", T(1000, 100000, 50000), 16000, "Satırların toplamı 151.000,00; tabloda 16.000,00 yazıyor")
kontrol(74, "Araç hasılat (sistem) toplam [düşük çözünürlük]", T(100000, 250000, 5000, 50000), 405000)
kontrol(78, "Bavul ticareti (sistem) TL toplam", T(310000, 310000, 310000, 310000), 1240000)
kontrol(78, "Bavul ticareti (sistem) döviz toplam", T(100000, 100000, 100000, 100000), 400000)
kontrol(81, "302-317 listesi (sistem) TL toplam", T("85711.60", 100000, 500000, 150000), "835711.60")
kontrol(81, "302-317 listesi (sistem) döviz toplam", T(0, 90000, 250000, 55000), 395000)
kontrol(85, "Serbest bölge fason (sistem) TL toplam", T("85711.60", 100000, 1000000, 10000), "1195711.60")
kontrol(85, "Serbest bölge fason (sistem) döviz toplam", T(0, 15000, 150000, 0), 165000)
kontrol(89, "Geçici 17 matrah toplamı", T(100, 100000, 55000, 15000000, 500000), 15655100)
kontrol(89, "Geçici 17 KDV toplamı", T(18, 10000, 5000, 1200000, 50000), 1265018)
kontrol(93, "FATİH (sistem) toplam", T(100000, 50000, 65000), 215000)
kontrol(97, "Geçici 39 (sistem) toplam", T(120000, 50000, 1000000), 1170000)
kontrol(100, "UEFA (sistem) toplam", T(150000, 50000, 45000), 245000)

# --- İndirimli Oran Hesaplama Tablosu (s.51), 439 işlem türü, 2018 ---
aylar = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
#        bedel, hesaplanan, yüklenilen, fark, önceki, iadeye esas, iade edilebilir, devreden, mahsup
tablo = [(1000000,100000,150000,50000,0,50000,38600,65000,0),
         (150000,15000,25000,10000,50000,60000,48600,113600,0),
         (500000,50000,75000,25000,60000,85000,73600,187200,0),
         (0,0,0,0,85000,85000,73600,187200,0),
         (300000,30000,45000,15000,85000,100000,88600,275800,0),
         (100000,10000,8000,-2000,100000,98000,88600,364400,0),
         (450000,4500,10000,5500,98000,103500,92100,456500,0),
         (200000,2000,1000,-1000,103500,102500,91100,500000,0),
         (10000000,100000,300000,200000,102500,302500,291100,791100,150000),
         (0,0,0,0,302500,302500,141100,950000,0),
         (500000,5000,65000,60000,302500,362500,201100,1100000,0),
         (400000,4000,24000,20000,362500,382500,221100,1163300,0)]
SINIR = 11400  # tablodan türetildi: Ocak 50.000 - 38.600
mahsup = 0; onceki_esas = 0; onceki_dev = None
for ay, (bedel, hes, yuk, fark, onc, esas, edil, dev, mah) in zip(aylar, tablo):
    kontrol(51, f"{ay}: Fark = Yüklenilen - Hesaplanan", yuk-hes, fark)
    bek_onc = onceki_esas if onceki_dev is None else min(onceki_esas, onceki_dev)
    kontrol(51, f"{ay}: Önceki dönem sonu iade edilebilir", bek_onc, onc)
    kontrol(51, f"{ay}: İadeye esas = Fark + Önceki", fark+onc, esas)
    bek = max(0, min(esas - SINIR - mahsup, dev))
    kontrol(51, f"{ay}: İade edilebilir = İadeye esas - sınır({SINIR}) - önceki mahsuplar({mahsup})", bek, edil)
    mahsup += mah; onceki_esas = esas; onceki_dev = dev
kontrol(51, "Yıl içinde mahsubu gerçekleşen toplam", mahsup, 150000)

hata = [s for s in sonuc if not s[4]]
print(f"Toplam kontrol: {len(sonuc)}  Tutan: {len(sonuc)-len(hata)}  Tutmayan: {len(hata)}")
for s in hata: print("TUTMUYOR  s.%s  %s  | hesaplanan=%s  belgede=%s  %s" % (s[0], s[1], s[2], s[3], s[5]))
if __name__ == "__main__":
    import sys
    if "-v" in sys.argv:
        for s in sonuc: print(("OK   " if s[4] else "HATA ")+"s.%s  %s = %s (belgede %s) %s" % (s[0], s[1], s[2], s[3], s[5]))
