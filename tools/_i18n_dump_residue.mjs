import fs from 'node:fs';
const d=JSON.parse(fs.readFileSync('tools/_i18n_residue_all.json','utf8'));
const L=[];
L.push('FLAGS '+d.flags.length+' TARGETED '+d.targeted.length);
L.push('===== TARGETED BY PATTERN =====');
const byp={};
for(const t of d.targeted){(byp[t.pattern]=byp[t.pattern]||[]).push(t)}
for(const [pat,arr] of Object.entries(byp)){
  L.push('--- '+pat+' count='+arr.length);
  for(const t of arr) L.push('  '+t.lang.padEnd(20)+' | '+t.file+' | '+t.key+'\n     EN: '+t.en+'\n     TR: '+t.tr);
}
L.push('===== ALL FLAGS =====');
const bylang={};
for(const f of d.flags){(bylang[f.lang]=bylang[f.lang]||[]).push(f)}
for(const [l,arr] of Object.entries(bylang)){
  L.push('--- '+l+' count='+arr.length);
  for(const f of arr) L.push('  ['+f.flags.join(',')+'] r='+f.ratio+' ov='+f.overlap+' stops='+JSON.stringify(f.stops)+' | '+f.file+' | '+f.key+'\n     EN: '+f.en+'\n     TR: '+f.tr);
}
fs.writeFileSync('tools/_i18n_residue_all.txt',L.join('\n')+'\n','utf8');
console.log('wrote lines',L.length);
