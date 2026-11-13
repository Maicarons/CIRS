#!/usr/bin/env node
import fs from 'node:fs';
const ok = JSON.parse(fs.readFileSync('tools/_i18n_residue_model_out.json','utf8'));
const bad = JSON.parse(fs.readFileSync('tools/_i18n_residue_model_fails.json','utf8'));
let s='=== SUCCESSES ('+ok.length+') ===\n';
for(const x of ok){s+=x.lang+' | '+x.key+'\n  EN: '+x.en+'\n  OLD: '+x.tr+'\n  NEW: '+x.tr_new+'\n';}
s+='\n=== FAILS ('+bad.length+') ===\n';
for(const f of bad){s+=f.fail.lang+' | '+f.fail.key+' | '+JSON.stringify(f.why)+'\n  OLD: '+f.fail.tr.slice(0,160)+'\n  GOT: '+f.sample+'\n';}
fs.writeFileSync('tools/_i18n_residue_review.txt',s,'utf8');
console.log('wrote',s.length);
