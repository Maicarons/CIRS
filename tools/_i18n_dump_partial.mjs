import fs from 'node:fs';
const d=JSON.parse(fs.readFileSync('tools/_i18n_partial_en.json','utf8'));
const L=[];
L.push('TOTAL '+JSON.stringify(d.total));
for(const o of d.languages){
  L.push('=== '+o.lang+' '+JSON.stringify(o.counts));
  for(const s of o.samples) L.push('  ['+s.flag+'] r='+s.ratio+' ov='+s.overlap+' stops='+JSON.stringify(s.stops)+'\n     EN: '+s.en+'\n     TR: '+s.tr);
}
fs.writeFileSync('tools/_i18n_partial_en_view.txt',L.join('\n')+'\n','utf8');
// also dump ALL flagged pairs, not just the 6 samples, for genuine-fix detection
const out=[];
for(const o of d.languages)for(const s of o.samples)out.push(o.lang+'|'+s.flag+'|'+s.file+'|'+s.key+'|'+s.en+'|'+s.tr);
fs.writeFileSync('tools/_i18n_partial_en_samples.txt',out.join('\n')+'\n','utf8');
console.log('wrote view lines',L.length,'sample pairs',out.length);
