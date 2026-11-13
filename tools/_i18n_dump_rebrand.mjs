import fs from 'node:fs';
const d=JSON.parse(fs.readFileSync('tools/_i18n_rebrand.json','utf8'));
const L=['STALE '+d.stale.length+' CASE_ONLY '+d.case_only.length+' GRF_DESC '+d.grf_desc.length+''];
L.push('===== CASE-ONLY ENGLISH =====');
for(const s of d.case_only) L.push('  '+s.lang+' | '+s.file+' | '+s.key+'\n     EN: '+s.en+'\n     TR: '+s.tr);
L.push('===== STALE REBRAND (full) =====');
const by={}; for(const s of d.stale){(by[s.lang]=by[s.lang]||[]).push(s)}
for(const [l,arr] of Object.entries(by)){
  L.push('--- '+l+' count='+arr.length);
  for(const s of arr) L.push('  ['+s.reasons.join(',')+'] ef='+s.efirs+' tf='+s.tfirs+' ec='+s.ecirs+' tc='+s.tcirs+' | '+s.file+' | '+s.key+'\n     EN: '+s.en+'\n     TR: '+s.tr);
}
fs.writeFileSync('tools/_i18n_rebrand_view.txt',L.join('\n')+'\n','utf8');
console.log('wrote lines',L.length);
