// Tam metin çekme: node metin_cek.js idler.txt cikti_klasoru
const { chromium } = require('playwright'); const fs=require('fs');
const BASE='https://karararama.danistay.gov.tr/'; const [idF,out]=process.argv.slice(2);
const ids=fs.readFileSync(idF,'utf8').split('\n').filter(Boolean); fs.mkdirSync(out,{recursive:true});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{ const b=await chromium.launch(); let p=await b.newPage();
 await p.goto(BASE,{waitUntil:'networkidle',timeout:60000});
 let ok=0,err=0;
 for(const id of ids){ if(fs.existsSync(`${out}/${id}.html`)) continue;
   for(let t=0;t<3;t++){ try{
     const rp=p.waitForResponse(x=>x.url().includes('getDocContent'),{timeout:45000}); rp.catch(()=>{});
     await p.goto(`${BASE}karar/${id}?aranacakKelimeler=vergi`,{waitUntil:'domcontentloaded',timeout:60000});
     const j=await (await rp).json(); const h=Buffer.from(j.data.content,'base64').toString('utf8');
     fs.writeFileSync(`${out}/${id}.html`,h); ok++; break;
   }catch(e){ if(t==2){ err++; console.log('ERR',id,e.message.split('\n')[0]); } else { await sleep(4000*(t+1)); await p.close().catch(()=>{}); p=await b.newPage(); } } }
   if((ok+err)%100==0) console.log('ilerleme',ok,err); await sleep(400); }
 console.log('bitti',ok,err); await b.close(); })();
