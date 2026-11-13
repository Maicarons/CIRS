import fs from 'node:fs';
import path from 'node:path';
const WORK='tools/_i18n_work', OUT='tools/_i18n_out';
const targets=['CIRS Community Industry Replacement Set','Total Town Replacement Set'];
function out(lang){const m=new Map();const f=path.join(OUT,lang+'.jsonl');if(fs.existsSync(f))for(const l of fs.readFileSync(f,'utf8').split('\n')){if(!l.trim())continue;try{const o=JSON.parse(l);if(Number.isInteger(o.i)&&typeof o.tr==='string')m.set(o.i,o.tr);}catch(e){}}return m;}
for(const lang of fs.readdirSync(WORK).filter(f=>f.endsWith('.json')&&!f.startsWith('_')).map(f=>f.slice(0,-5)).sort()){
  const w=JSON.parse(fs.readFileSync(path.join(WORK,lang+'.json'),'utf8'));if(!w.entries)continue;const m=out(lang);
  for(let i=0;i<w.entries.length;i++){const en=w.entries[i].en; if(!targets.some(t=>en.includes(t)))continue; const tr=m.get(i);
    if(tr===undefined)continue; const same=tr===en;
    console.log((same?'SAME ':'DIFF ')+lang.padEnd(20)+' | '+tr.slice(0,110));
  }
}
