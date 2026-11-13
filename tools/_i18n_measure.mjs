#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd(), WORK = path.join(ROOT, 'tools', '_i18n_work'), OUT = path.join(ROOT, 'tools', '_i18n_out');
function loadOut(lang) { const f = path.join(OUT, lang + '.jsonl'), m = new Map(); if (fs.existsSync(f)) for (const l of fs.readFileSync(f, 'utf-8').split('\n')) { if (!l.trim()) continue; try { const o = JSON.parse(l); if (Number.isInteger(o.i) && typeof o.tr === 'string') m.set(o.i, o.tr); } catch(e){} } return m; }
const CYR = /[\u0400-\u04FF]/, LAT = /[A-Za-z]/;
for (const lang of ['serbian','belarusian','russian']) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8')), m = loadOut(lang);
  let cyr=0, lat=0, both=0, none=0;
  for (let i=0;i<w.count;i++){ const tr=m.get(i); if(tr===undefined) continue; const c=CYR.test(tr), l=LAT.test(tr); if(c&&l) both++; else if(c) cyr++; else if(l) lat++; else none++; }
  console.log(lang.padEnd(14) + ' cyr=' + cyr + ' latin=' + lat + ' mixed=' + both + ' neither=' + none + ' have=' + m.size);
}
for (const lang of ['simplified_chinese','traditional_chinese']) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8')), m = loadOut(lang);
  console.log('\n=== ' + lang + ' samples (' + m.size + '/' + w.count + ') ===');
  let n = 0;
  for (let i=0;i<w.count && n<12;i++){ const tr=m.get(i); if(tr===undefined) continue; const en=w.entries[i].en; if(en.length<12) continue; console.log('EN: ' + en.slice(0,100)); console.log('TR: ' + tr.slice(0,140)); n++; }
}
