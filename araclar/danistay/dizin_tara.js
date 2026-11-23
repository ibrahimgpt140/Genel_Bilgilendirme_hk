// Karar no (yıl + sıra aralığı) pencereleriyle bir dairenin bir yıldaki tüm kararlarının künyesini toplar.
// Kullanım: node dizin_tara.js sayim.json cikti.jsonl [daire filtresi virgüllü]
const {open,search,sleep,chromium}=require('./dan.js'); const fs=require('fs');
const [sayimF,outF,filt]=process.argv.slice(2);
const hedef=JSON.parse(fs.readFileSync(sayimF)).filter(x=>typeof x.total==='number'&&x.total>0&&(!filt||filt.split(',').includes(x.daire)));
const seen=new Set(); const done=new Set();
if(fs.existsSync(outF)) for(const l of fs.readFileSync(outF,'utf8').split('\n')){ if(!l) continue; const o=JSON.parse(l); if(o.id) seen.add(o.id); if(o._done) done.add(o._done); }
const w=o=>fs.appendFileSync(outF,JSON.stringify(o)+'\n');
(async()=>{ const b=await chromium.launch(); let p=await open(b);
 async function ara(q){ for(let t=0;t<4;t++){ try{ const r=await search(p,q); if(r.err) throw new Error(r.err); return r; }catch(e){ console.log('  tekrar',JSON.stringify(q),e.message.slice(0,120)); await p.close().catch(()=>{}); await sleep(5000*(t+1)); p=await open(b);} } throw new Error('başarısız '+JSON.stringify(q)); }
 for(const h of hedef){ const key=h.daire+'|'+h.yil; if(done.has(key)) continue;
   let got=0, bos=0, s=1; const t0=Date.now();
   while(true){
     const pencere=async(a,z)=>{ const r=await ara({daire:[h.daire],kararNoYil:h.yil,siraStart:a,siraEnd:z});
       if(r.total>r.list.length && z>a){ const m=Math.floor((a+z)/2); return (await pencere(a,m))+(await pencere(m+1,z)); }
       let n=0; for(const x of r.list){ if(x.kyil!==h.yil) continue; n++; if(!seen.has(x.id)){ seen.add(x.id); w(x);} } await sleep(800); return n; };
     const n=await pencere(s,s+99); got+=n; bos = n? 0 : bos+1; s+=100;
     if(got>=h.total || bos>=8) break;
   }
   w({_done:key,total:h.total,got}); console.log(key,'toplam',h.total,'alınan',got,Math.round((Date.now()-t0)/1000)+'s');
 }
 await b.close(); })();
