// Danıştay Karar Arama – sitenin kendi arayüzünden arama; filtreler arayüzde bulunan alanlarla (daire, karar no yıl/sıra, karar tarihi) sınırlıdır.
const { chromium } = require('playwright');
const BASE='https://karararama.danistay.gov.tr/';
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function open(b){
  const p=await b.newPage({viewport:{width:1280,height:1400}});
  let birimler=null;
  p.on('response',async r=>{ if(r.url().includes('getBirimler')) { try{birimler=(await r.json()).data;}catch(e){} } });
  await p.goto(BASE,{waitUntil:'networkidle',timeout:60000});
  await p.getByText('Tamam',{exact:true}).click({timeout:3000}).catch(()=>{});
  await p.getByText('Detaylı Arama').click(); await p.waitForTimeout(800);
  p._birimler=()=>birimler;
  return p;
}
// q: {kw:[], daire:[], kararNoYil, siraStart, siraEnd, tarihStart, tarihEnd, sort:'DESC'}
async function search(p,q){
  if(p._used){ await p.goto(BASE,{waitUntil:'domcontentloaded',timeout:60000}); await p.getByText('Detaylı Arama').waitFor({timeout:30000}); await p.getByText('Tamam',{exact:true}).click({timeout:1500}).catch(()=>{}); await p.getByText('Detaylı Arama').click(); await p.waitForTimeout(500); }
  p._used=true;
  await p.unroute('**/getEmsalKarar').catch(()=>{});
  await p.route('**/getEmsalKarar', async route=>{
    const body=JSON.parse(route.request().postData()); const d=body.data;
    d.andKelimeler=q.kw||[]; d.birimAdiList=q.daire||[];
    d.kararNoYil=q.kararNoYil?String(q.kararNoYil):''; d.kararNoSiraStart=q.siraStart?String(q.siraStart):''; d.kararNoSiraEnd=q.siraEnd?String(q.siraEnd):'';
    d.kararTarihiStart=q.tarihStart||null; d.kararTarihiEnd=q.tarihEnd||null; if(q.sort) d.sortDirection=q.sort;
    await route.continue({postData:JSON.stringify(body)});
  });
  const inp=p.locator("input[placeholder=\"Kelime yazıp Enter'a basın...\"]:visible").first();
  if(!(await p.locator('.dx-tag:visible').count())){ await inp.click(); await inp.fill('x'); await inp.press('Enter'); }
  const rp=p.waitForResponse(r=>r.url().includes('getEmsalKarar'),{timeout:45000});
  await p.locator('.dx-button[aria-label="Sorgula"]').last().evaluate(el=>{el.scrollIntoView();});
  await p.locator('.dx-button[aria-label="Sorgula"]').last().click({force:true}).catch(async()=>{});
  const j=await (await rp).json();
  if(!j.data) return {err:JSON.stringify(j).slice(0,300)};
  return {total:j.data.total, list:(j.data.emsalKararList||[]).map(x=>({id:x.documentId,daire:x.birimAdi,esas:x.esasNo,karar:x.kararNo,tarih:x.kararTarihiStr,kyil:x.kararNoYil,ksira:x.kararNoSira,turu:x.kararTuru}))};
}
module.exports={open,search,sleep,chromium};
