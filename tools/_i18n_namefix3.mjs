#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
const ROOT=process.cwd(), WORK=path.join(ROOT,'tools','_i18n_work'), OUT=path.join(ROOT,'tools','_i18n_out');
const URL='https://index-translate.bilibili.com/v1/chat/completions', MODEL='Index-Translate-9B', TIMEOUT=60000;
const PH=/\{([A-Za-z_0-9]*)\}/g; const phList=s=>(String(s).match(PH)||[]).sort().join(',');
const NAME_EN='CIRS Community Industry Replacement Set';
const T={ belarusian:'白俄罗斯语（Беларуская мова）', korean:'韩语（한국어）' };
const HINT={ belarusian:'Набор CIRS для замены аб’ектаў прамысловасці супольнасці', korean:'CIRS 커뮤니티 산업 교체 세트' };
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function loadOut(lang){const m=new Map();const f=path.join(OUT,lang+'.jsonl');if(fs.existsSync(f))for(const l of fs.readFileSync(f,'utf8').split('\n')){if(!l.trim())continue;try{const o=JSON.parse(l);if(Number.isInteger(o.i)&&typeof o.tr==='string')m.set(o.i,o.tr);}catch(e){}}return m;}
async function call(text){const ctrl=new AbortController(),t=setTimeout(()=>ctrl.abort(),TIMEOUT);
  try{const r=await fetch(URL,{method:'POST',signal:ctrl.signal,headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},body:JSON.stringify({model:MODEL,messages:[{role:'user',content:text}],temperature:0,max_tokens:512,stream:false,chat_template_kwargs:{enable_thinking:false}})});
    const s=await r.text();if(!r.ok)throw new Error('HTTP '+r.status);const j=JSON.parse(s);return (j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
  }finally{clearTimeout(t);}}
for(const lang of Object.keys(T)){
  const w=JSON.parse(fs.readFileSync(path.join(WORK,lang+'.json'),'utf8'));const m=loadOut(lang);
  const idx=w.entries.findIndex(e=>e.en===NAME_EN); const cur=m.get(idx);
  const prompt='把下列 OpenTTD 模组名称翻译成'+T[lang]+'。\n' +
    'CIRS 是项目名，必须原样写成 CIRS（不要写成 FIRS）；其余三个英文普通词要译成'+T[lang]+'，意为「社区工业替换套装」，不得残留英文。\n' +
    '参考译法（请照此格式输出，不要解释）：'+HINT[lang]+'\n\n' +
    '【原文】'+NAME_EN+'\n\n【当前错误译文】'+cur+'\n\n只输出正确译文：';
  let best=null;
  for(let k=0;k<4&&!best;k++){try{let tr=(await call(prompt)).trim().replace(/^["'「」]+|["'」」]+$/g,'');
    if(phList(NAME_EN)!==phList(tr)||tr===NAME_EN||!/CIRS/.test(tr)||/FIRS/.test(tr))continue;
    if(/Community Industry|Replacement Set/i.test(tr))continue;
    if(/\uFFFD/.test(tr))continue;
    if(tr.length>90)continue;
    best=tr;
  }catch(e){await sleep(600*(k+1));}}
  if(best){fs.appendFileSync(path.join(OUT,lang+'.jsonl'),JSON.stringify({i:idx,tr:best})+'\n','utf8');console.log('FIXED '+lang+' | OLD='+cur+'\n       NEW='+best);}
  else console.log('KEEP  '+lang+' | '+cur);
}
