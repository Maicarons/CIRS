import fs from 'node:fs';
const c=JSON.parse(fs.readFileSync('tools/_i18n_rebrand_candidates.json','utf8'));
const L=['CANDIDATES '+c.length];
const byk={}; for(const x of c){(byk[x.key]=byk[x.key]||[]).push(x)}
for(const [k,arr] of Object.entries(byk)){
  L.push('=== KEY '+k+' count='+arr.length+' ===');
  for(const x of arr) L.push('  '+x.lang.padEnd(20)+' inwork='+x.in_work+' idx='+x.work_index+' ['+x.reasons.join(',')+']\n     EN: '+x.en+'\n     TR: '+x.tr);
}
fs.writeFileSync('tools/_i18n_rebrand_candidates.txt',L.join('\n')+'\n','utf8');
console.log('wrote lines',L.length);
