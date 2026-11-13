#!/usr/bin/env node
import fs from 'node:fs';
const T = JSON.parse(fs.readFileSync('tools/_i18n_rebrand_model_tasks.json','utf8'));
const mo = JSON.parse(fs.readFileSync('tools/_i18n_rebrand_model_out.json','utf8'));
const fails = JSON.parse(fs.readFileSync('tools/_i18n_rebrand_rest_fails.json','utf8'));
let s = '=== SUCCESSES (non-desc) ===\n';
for (const x of mo.filter(y=>y.key!=='STR_GRF_DESC.base')) {
  s += x.lang+' '+x.key+'\n  EN: '+x.en+'\n  OLD: '+x.tr_before+'\n  NEW: '+x.tr+'\n';
}
s += '\n=== FAILS ===\n';
for (const f of fails) s += f.fail.lang+' '+f.fail.key+' '+JSON.stringify(f.why)+'\n  '+f.sample+'\n';
fs.writeFileSync('tools/_i18n_rebrand_rest_view.txt', s, 'utf8');
console.log('wrote', s.length);
