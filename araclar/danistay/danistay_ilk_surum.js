// Danıştay Karar Arama – site arayüzü üzerinden arama ve tam metin çekme
// Kullanım:
//   node danistay.js search '<json>' out.json   json: {"kw":["\"sahte belge\"","\"karşıt inceleme\""],"daire":"9. Daire"}
//   node danistay.js fetch id1,id2,... outdir   (her karar için <id>.html ve <id>.txt)
const { chromium } = require('playwright'); const fs = require('fs');
const BASE='https://karararama.danistay.gov.tr/';
async function search(b, q){
  const p=await b.newPage({viewport:{width:1280,height:1400}});
  await p.goto(BASE,{waitUntil:'networkidle',timeout:60000});
  await p.getByText('Tamam',{exact:true}).click({timeout:3000}).catch(()=>{});
  await p.getByText('Detaylı Arama').click(); await p.waitForTimeout(800);
  const inp=p.locator("input[placeholder=\"Kelime yazıp Enter'a basın...\"]:visible").first();
  for (const k of q.kw){ await inp.click(); await inp.fill(k); await inp.press('Enter'); await p.waitForTimeout(200); }
  if (q.not) { const ni=p.locator("input[placeholder=\"Kelime yazıp Enter'a basın...\"]:visible").nth(1); for (const k of q.not){ await ni.click(); await ni.fill(k); await ni.press('Enter'); } }
  if (q.daire){ await p.locator('input[placeholder="Daire Seçiniz"]:visible').click(); await p.waitForTimeout(1000);
    await p.locator('.dx-list-item:visible',{hasText:new RegExp('^'+q.daire.replace(/[.()]/g,'\\$&')+'$')}).first().click(); }
  const rp=p.waitForResponse(r=>r.url().includes('getEmsalKarar'),{timeout:90000});
  await p.locator('button:visible, .dx-button:visible',{hasText:'Sorgula'}).last().click();
  const j=await (await rp).json(); await p.close();
  return {query:q,total:j.data.total,results:j.data.emsalKararList.map(x=>({id:x.documentId,daire:x.birimAdi,esas:x.esasNo,karar:x.kararNo,tarih:x.kararTarihiStr,url:BASE+'karar/'+x.documentId}))};
}
async function fetchDocs(b, ids, out){
  fs.mkdirSync(out,{recursive:true}); const p=await b.newPage();
  await p.goto(BASE,{waitUntil:'networkidle',timeout:60000});
  for (const id of ids){ if (fs.existsSync(`${out}/${id}.txt`)) continue;
    try{ const rp=p.waitForResponse(x=>x.url().includes('getDocContent'),{timeout:45000});
      await p.goto(`${BASE}karar/${id}?aranacakKelimeler=vergi`,{timeout:60000});
      const h=Buffer.from((await (await rp).json()).data.content,'base64').toString('utf8');
      fs.writeFileSync(`${out}/${id}.html`,h);
      let t=h.replace(/<br\s*\/?>/gi,'\n').replace(/<[^>]+>/g,'').replace(/&nbsp;/g,' ').replace(/[ \t ]+/g,' ').replace(/\n\s*\n+/g,'\n');
      fs.writeFileSync(`${out}/${id}.txt`,t); console.log('ok',id);
    }catch(e){ console.log('ERR',id,e.message.split('\n')[0]); } }
}
(async()=>{ const [cmd,a,b2]=process.argv.slice(2); const br=await chromium.launch();
  try{ if(cmd==='search'){ const r=await search(br,JSON.parse(a)); fs.writeFileSync(b2,JSON.stringify(r,null,1)); console.log('total',r.total,'got',r.results.length); }
       else if(cmd==='fetch'){ await fetchDocs(br,a.split(','),b2); } }
  finally{ await br.close(); } })();
