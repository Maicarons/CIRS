#!/usr/bin/env node
import fs from 'node:fs';
const URL = 'https://index-translate.bilibili.com/v1/chat/completions', MODEL = 'Index-Translate-9B';
const T = JSON.parse(fs.readFileSync('tools/_i18n_rebrand_model_tasks.json','utf8'));
const pick = T.retranslate.filter(x => x.key === 'STR_GRF_DESC.base').slice(0, 3);
const obj = {}; for (const [i,x] of pick.entries()) obj[String(i)] = {en:x.en, cur:x.tr};
const notes = pick.map((x,i)=>String(i)+': '+x.note+(x.name_hint?'（模组名：'+x.name_hint+'）':'')).join('\n');
const prompt = '你是本地化审校员。下面 JSON 的 key 是编号，value.en 是【英语原文】，value.cur 是【当前译文】。当前译文是旧版 FIRS 模组的遗留文案，与新的英语原文不符（品牌名、句子内容已更新为 CIRS 社区分支）。请依据英语原文重新给出地道、准确的译文。\n' +
  '【硬性要求】所有花括号占位符必须逐字原样保留；CIRS、FIRS、OpenTTD、FRAX、GPL、NewGRF、git 等专有名词保持原样不译；不要输出 JSON 之外的任何内容。\n' +
  '【逐条要点】\n'+notes+'\n\n【待修订】\n'+JSON.stringify(obj)+'\n\n请以相同 key 输出 JSON，value 为修订后的译文字符串。只输出 JSON。';
const r = await fetch(URL, {method:'POST', headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},
  body: JSON.stringify({model:MODEL, messages:[{role:'user',content:prompt}], temperature:0.0, max_tokens:8192, stream:false, chat_template_kwargs:{enable_thinking:false}})});
const s = await r.text();
let j = {}; try { j = JSON.parse(s); } catch(e) { console.log('OUTER PARSE FAIL', s.slice(0,300)); process.exit(0); }
const raw = (j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || '';
console.log('=== RAW (len '+raw.length+') ===');
console.log(raw.slice(0, 4000));
console.log('=== EN (first) ===', pick[0].en);
console.log('=== CUR (first) ===', pick[0].tr);
const PH_RE = /\{([A-Za-z_0-9]*)\}/g;
const phList = s2 => (String(s2).match(PH_RE)||[]).sort().join(',');
let clean = raw.trim().replace(/^<think>[\s\S]*?<\/think>/,'').trim();
let parsed; try { parsed = JSON.parse(clean); } catch(e) { const a=clean.indexOf('{'), b=clean.lastIndexOf('}'); try { parsed=JSON.parse(clean.slice(a,b+1)); } catch(e2){ console.log('no JSON'); process.exit(0); } }
for (const [i,x] of pick.entries()) {
  let v = parsed[String(i)];
  if (typeof v==='string') v = v.replace(/^[\r\n]+|[\r\n]+$/g,'');
  const ef=(x.en.match(/FIRS/g)||[]).length, tf=((v||'').match(/FIRS/g)||[]).length;
  const ec=(x.en.match(/CIRS/g)||[]).length, tc=((v||'').match(/CIRS/g)||[]).length;
  console.log('--- item',i,'ph',phList(x.en)===phList(v||''),'ef',ef,'tf',tf,'ec',ec,'tc',tc,'v!==cur',v!==x.tr,'len',(v||'').length);
  console.log('    V:', JSON.stringify(String(v).slice(0,400)));
}
