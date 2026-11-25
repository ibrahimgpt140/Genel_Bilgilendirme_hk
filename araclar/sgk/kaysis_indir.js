// KAYSİS (kms.kaysis.gov.tr) SGK kurum sayfasında, depoda henüz olmayan kayıtları indirir.
// Kullanım: yerleşik tarayıcıda https://kms.kaysis.gov.tr/Home/Kurum/22620739 açıkken javascript_tool ile çalıştırılır.
// BILINEN yer tutucusu yerine depodaki sgk/kaysis/dizin.csv'den üretilen {"kategori": [id, ...], ...} nesnesi konur
// (python3 araclar/sgk/kaysis_bilinen.py çıktısı).
// Yeni kayıt varsa her biri base64 PDF olarak `kaysis-sgk-yeni-<tarih>-NN.json` paketlerine yazılıp İndirilenler'e indirilir;
// ilk pakette sayfadaki tam dizin de bulunur. window.__kaysis_ref = '<commit sha>' verilirse dizin o commit'ten okunur (GitHub önbelleğinden etkilenmez). Durum: window.__kdurum (bitti, yeni, paket, hata, dosyalar).
(async () => {
  let BILINEN;
  if (typeof __BILINEN__ !== 'undefined') {
    BILINEN = new Set(Object.entries(__BILINEN__).flatMap(([k, ids]) => ids.map(i => `${k}|${i}`)));
  } else {
    // yer tutucu doldurulmadıysa depodaki dizini GitHub'dan oku (depo herkese açık)
    const csv = await fetch(`https://raw.githubusercontent.com/ibrahimgpt140/Genel_Bilgilendirme_hk/${window.__kaysis_ref || 'main'}/sgk/kaysis/dizin.csv`, {cache: 'no-store'}).then(r => r.text());
    // tırnaklı alanları (satır sonu ve virgül içerebilir) doğru okuyan küçük CSV ayrıştırıcı
    const satirlar = []; let alan = '', satir = [], tirnak = false;
    for (let i = 0; i < csv.length; i++) {
      const c = csv[i];
      if (tirnak) { if (c === '"' && csv[i + 1] === '"') { alan += '"'; i++; } else if (c === '"') tirnak = false; else alan += c; }
      else if (c === '"') tirnak = true;
      else if (c === ',') { satir.push(alan); alan = ''; }
      else if (c === '\n') { satir.push(alan.replace(/\r$/, '')); satirlar.push(satir); satir = []; alan = ''; }
      else alan += c;
    }
    if (alan || satir.length) { satir.push(alan); satirlar.push(satir); }
    BILINEN = new Set(satirlar.slice(1).map(r => { const m = (r[5] || '').match(/Goster\/(\d+)/); return m ? `${r[0]}|${m[1]}` : null; }).filter(Boolean));
    if (BILINEN.size < 900) { window.__kdurum = {bitti: true, hata: [['dizin', 'depodaki dizin.csv okunamadı (' + BILINEN.size + ' kayıt)']]}; return; }
  }
  const idx = [];
  for (const p of document.querySelectorAll('.panel')) {
    const h = p.querySelector('h3.panel-title');
    if (!h || !h.querySelector('.badge')) continue;
    const kat = h.childNodes[0].textContent.trim();
    for (const row of p.querySelectorAll('.row')) {
      const a = row.querySelector(':scope > .col-md-8 a[href*="/Home/Goster/"]');
      if (!a) continue;
      const id = a.getAttribute('href').match(/Goster\/(\d+)/)[1];
      if (idx.find(x => x.id === id && x.kat === kat)) continue;
      const links = [...row.querySelectorAll(':scope > .col-md-8 a')];
      const sayi = (row.querySelector('.badge')?.textContent || '').trim();
      const baslik = (links.find(l => l.getAttribute('target') === '_blank' && /Goster/.test(l.href))?.textContent || '').replace(/\s+/g, ' ').trim();
      const rgA = links.find(l => /resmigazete/.test(l.href));
      idx.push({kat, id, sayi, baslik, rg: rgA ? rgA.textContent.replace(/\s+/g, ' ').trim() : '', rg_url: rgA ? rgA.href : '', ek: ''});
    }
  }
  const yeni = idx.filter(x => !BILINEN.has(`${x.kat}|${x.id}`));
  const tarih = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  window.__kdurum = {bitti: false, toplam_sayfa: idx.length, yeni: yeni.map(x => `${x.kat} | ${x.sayi} | ${x.baslik}`), paket: 0, hata: [], dosyalar: []};
  if (!yeni.length) { window.__kdurum.bitti = true; return; }
  const b64 = (buf) => { let s = ''; const u = new Uint8Array(buf); for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s); };
  const indir = (obj, ad) => { const u = URL.createObjectURL(new Blob([JSON.stringify(obj)], {type: 'application/json'})); const a = document.createElement('a'); a.href = u; a.download = ad; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(u), 60000); window.__kdurum.dosyalar.push(ad); };
  let docs = [], boy = 0;
  const bosalt = () => { window.__kdurum.paket++; const n = window.__kdurum.paket; indir({kaynak: 'https://kms.kaysis.gov.tr/Home/Kurum/22620739', alinma: new Date().toISOString(), paket: n, dizin: n === 1 ? idx : undefined, docs}, `kaysis-sgk-yeni-${tarih}-${String(n).padStart(2, '0')}.json`); docs = []; boy = 0; };
  for (const x of yeni) {
    for (let d = 0; d < 3; d++) {
      try {
        const r = await fetch(`https://kms.kaysis.gov.tr/Home/Goster/${x.id}`);
        if (!r.ok) throw new Error('HTTP ' + r.status);
        const ct = r.headers.get('content-type') || ''; const buf = await r.arrayBuffer(); const s = b64(buf);
        docs.push({id: x.id, kat: x.kat, ct, boyut: buf.byteLength, b64: s}); boy += s.length; break;
      } catch (e) { if (d === 2) window.__kdurum.hata.push([x.id, String(e)]); await new Promise(z => setTimeout(z, 2000)); }
    }
    if (boy > 40 * 1024 * 1024) { bosalt(); await new Promise(z => setTimeout(z, 1500)); }
  }
  if (docs.length || !window.__kdurum.paket) bosalt();
  window.__kdurum.bitti = true;
})();
