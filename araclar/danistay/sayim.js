// Daire × yıl karar sayıları. Kullanım: node sayim.js cikti.json "2025,2026" ["Vergi Dava Daireleri Kurulu,3. Daire"]
const {open,search,sleep,chromium}=require('./dan.js'); const fs=require('fs');
const [outF,yillar,filt]=process.argv.slice(2);
(async()=>{ const b=await chromium.launch(); let p=await open(b); await sleep(1500);
 let daireler=p._birimler().map(x=>x.daire); if(filt) daireler=daireler.filter(d=>filt.split(',').includes(d));
 const out=[];
 for (const d of daireler) for (const y of yillar.split(',').map(Number)) {
   let r; for (let t=0;t<3;t++){ try{ r=await search(p,{daire:[d],kararNoYil:y}); if(!r.err) break; }catch(e){ await p.close().catch(()=>{}); await sleep(5000); p=await open(b); } }
   out.push({daire:d,yil:y,total:r&&(r.total??r.err)}); console.log(d,y,r&&(r.total??r.err)); await sleep(1200); }
 fs.writeFileSync(outF,JSON.stringify(out,null,1)); await b.close(); })();
