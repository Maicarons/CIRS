#!/usr/bin/env node
/* Final polish: GRF display name. Keep the proper noun CIRS verbatim, translate the
 * descriptive part; also fix languages where the model wrote FIRS instead of CIRS. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT=process.cwd(), WORK=path.join(ROOT,'tools','_i18n_work'), OUT=path.join(ROOT,'tools','_i18n_out');
const URL='https://index-translate.bilibili.com/v1/chat/completions', MODEL='Index-Translate-9B', TIMEOUT=60000;
const PH=/\{([A-Za-z_0-9]*)\}/g;
const phList=s=>(String(s).match(PH)||[]).sort().join(',');
const NAMES={belarusian:'白俄罗斯语',danish:'丹麦语',dutch:'荷兰语',german:'德语',indonesian:'印度尼西亚语',italian:'意大利语',korean:'韩语',latin:'拉丁语',luxembourgish:'卢森堡语',norwegian_bokmal:'书面挪威语',swedish:'瑞典语',turkish:'土耳其语'};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const NAME_EN='CIRS Community Industry Replacement Set';
function loadOut(lang){const m=new Map();const f=path.join(OUT,lang+'.jsonl');if(fs.existsSync(f))for(const l of fs.readFileSync(f,'utf8').split('\n')){if(!l.trim())continue;try{const o=JSON.parse(l);if(Number.isInteger(o.i)&&typeof o.tr==='string')m.set(o.i,o.tr);}catch(e){}}return m;}
function hardBad(en,tr){if(!tr||typeof tr!=='string'||!tr.trim())return true;if(phList(en)!==phList(tr))return true;if(/\uFFFD/.test(tr)||/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(tr))return true;for(const m of tr.matchAll(PH))if(/[^\x00-\x7F]/.test(m[1]))return true;return false;}
async function call(text){const ctrl=new AbortController(),t=setTimeout(()=>ctrl.abort(),TIMEOUT);
  try{const r=await fetch(URL,{method:'POST',signal:ctrl.signal,headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},body:JSON.stringify({model:MODEL,messages:[{role:'user',content:text}],temperature:0,max_tokens:1024,stream:false,chat_template_kwargs:{enable_thinking:false}})});
    const s=await r.text();if(!r.ok)throw new Error('HTTP '+r.status);const j=JSON.parse(s);return (j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
  }finally{clearTimeout(t);}}
let changed=0, skipped=0;
for(const lang of Object.keys(NAMES)){
  const w=JSON.parse(fs.readFileSync(path.join(WORK,lang+'.json'),'utf8'));if(!w.entries)continue;const m=loadOut(lang);
  const idx=w.entries.findIndex(e=>e.en===NAME_EN);
  if(idx<0){console.log('SKIP '+lang+' (no exact name entry)');skipped++;continue;}
  const en=w.entries[idx].en, cur=m.get(idx);
  if(cur===undefined){console.log('SKIP '+lang+' (missing)');skipped++;continue;}
  const needs= cur===en || (/FIRS/.test(cur)&&!/CIRS/.test(cur));
  if(!needs){console.log('OK   '+lang+' (already) '+cur.slice(0,70));continue;}
  const tgt=NAMES[lang];
  const prompt='你是'+tgt+'本地化审校员。请翻译下面这个 OpenTTD NewGRF 模组的显示名称。\n' +
    '【硬性要求】CIRS 是本项目专有名词，必须原样保留（绝对不要改成 FIRS，也不要删掉）；FIRS 是它的上游项目名，不能混用。\n' +
    '把 Community Industry Replacement Set 这三个普通词准确译成'+tgt+'（意为「社区工业替换套装/合集」），不要保留英文，不要整句照抄原文。\n' +
    '只输出译文，不要任何解释、引号或前后缀。\n\n【原文】\n'+en+'\n\n【当前译文（需要修正）】\n'+cur;
  let best=null;
  for(let k=0;k<3&&!best;k++){try{const tr=(await call(prompt)).trim();
    if(hardBad(en,tr)||tr===en||!/CIRS/.test(tr)||/FIRS/.test(tr)&&!/CIRS/.test(tr))continue;
    if(tr.replace(/CIRS/g,'').replace(/[^A-Za-z]/g,'').length===0)continue;
    best=tr;
  }catch(e){await sleep(600*(k+1));}}
  if(best){fs.appendFileSync(path.join(OUT,lang+'.jsonl'),JSON.stringify({i:idx,tr:best})+'\n','utf8');
    console.log('FIXED '+lang.padEnd(18)+' | OLD='+cur.slice(0,70)+'\n                     | NEW='+best.slice(0,90));changed++;}
  else {console.log('KEEP  '+lang+' (no clean result) cur='+cur.slice(0,80));skipped++;}
}
console.log('NAMEFIX changed='+changed+' skipped='+skipped);
