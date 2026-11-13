#!/usr/bin/env node
/* Fix intra-language inconsistencies: same English value is translated in some keys but kept English in others. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT=process.cwd(), WORK=path.join(ROOT,'tools','_i18n_work'), OUT=path.join(ROOT,'tools','_i18n_out');
const PH=o=>Object.entries((String(o).match(/\{[^}]*\}/g)||[]).reduce((a,x)=>(a[x]=(a[x]||0)+1,a),{})).sort().map(([k,v])=>k+':'+v).join('|');
const data=JSON.parse(fs.readFileSync('tools/_i18n_consensus.json','utf8'));
let applied=0, skipped=0;
for(const inc of data.inconsistency){
  const f=path.join(WORK,inc.lang+'.json');
  if(!fs.existsSync(f)){skipped++;continue;}
  const w=JSON.parse(fs.readFileSync(f,'utf8'));
  let idx=-1;
  for(let i=0;i<w.entries.length;i++)if(w.entries[i].refs.some(([rf,rk])=>rf===inc.file&&rk===inc.key)){idx=i;break;}
  if(idx<0){skipped++;continue;}
  if(PH(inc.en)!==PH(inc.tr)){console.log('SKIP ph mismatch',inc.lang,inc.key);skipped++;continue;}
  fs.appendFileSync(path.join(OUT,inc.lang+'.jsonl'),JSON.stringify({i:idx,tr:inc.tr})+'\n','utf8');
  console.log('FIX',inc.lang,inc.key,JSON.stringify(inc.en),'->',JSON.stringify(inc.tr),'index',idx);
  applied++;
}
console.log('INCONSISTENCY_FIX applied='+applied+' skipped='+skipped);
