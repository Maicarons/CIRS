#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
const ROOT=process.cwd(), WORK=path.join(ROOT,'tools','_i18n_work'), OUT=path.join(ROOT,'tools','_i18n_out');
const URL='https://index-translate.bilibili.com/v1/chat/completions', MODEL='Index-Translate-9B', TIMEOUT=60000;
const PH=/\{([A-Za-z_0-9]*)\}/g; const phList=s=>(String(s).match(PH)||[]).sort().join(',');
const NAMES={belarusian:'白俄罗斯语（Беларуская）',danish:'丹麦语（Dansk）',dutch:'荷兰语（Nederlands）',german:'德语（Deutsch）',indonesian:'印度尼西亚语（Bahasa Indonesia）',italian:'意大利语（Italiano）',korean:'韩语（한국어）',latin:'拉丁语（Latina）',luxembourgish:'卢森堡语（Lëtzebuergesch）',norwegian_bokmal:'书面挪威语（Norsk bokmål）',swedish:'瑞典语（Svenska）',turkish:'土耳其语（Türkçe）'};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const NAME_EN='CIRS Community Industry Replacement Set';
function loadOut(lang){const m=new Map();const f=path.join(OUT,lang+'.jsonl');if(fs.existsSync(f))for(const l of fs.readFileSync(f,'utf8').split('\n')){if(!l.trim())continue;try{const o=JSON.parse(l);if(Number.isInteger(o.i)&&typeof o.tr==='string')m.set(o.i,o.tr);}catch(e){}}return m;}
function hardBad(en,tr){if(!tr||typeof tr!=='string'||!tr.trim())return true;if(phList(en)!==phList(tr))return true;if(/\uFFFD/.test(tr)||/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(tr))return true;return false;}
async function call(text){const ctrl=new AbortController(),t=setTimeout(()=>ctrl.abort(),TIMEOUT);
  try{const r=await fetch(URL,{method:'POST',signal:ctrl.signal,headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},body:JSON.stringify({model:MODEL,messages:[{role:'user',content:text}],temperature:0,max_tokens:512,stream:false,chat_template_kwargs:{enable_thinking:false}})});
    const s=await r.text();if(!r.ok)throw new Error('HTTP '+r.status);const j=JSON.parse(s);return (j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
  }finally{clearTimeout(t);}}
let changed=0;
for(const lang of Object.keys(NAMES)){
  const w=JSON.parse(fs.readFileSync(path.join(WORK,lang+'.json'),'utf8'));if(!w.entries)continue;const m=loadOut(lang);
  const idx=w.entries.findIndex(e=>e.en===NAME_EN);if(idx<0)continue;
  const cur=m.get(idx);if(cur===undefined)continue;
  const hasEnglish=/Community Industry|Replacement Set|Community Industry Replacement Set/i.test(cur);
  const wrongProject=/FIRS/.test(cur)&&!/CIRS/.test(cur);
  if(!hasEnglish&&!wrongProject&&cur!==NAME_EN){console.log('OK    '+lang.padEnd(18)+' | '+cur.slice(0,75));continue;}
  const tgt=NAMES[lang];
  const prompt='把下面这个 OpenTTD 模组名称翻译成'+tgt+'。\n' +
    '规则：① CIRS 是本项目名，必须原样保留（不要写成 FIRS）；② Community Industry Replacement Set 三个普通词必须全部译成'+tgt+'，意思是「社区工业替换套装」，不得残留任何英文普通词；③ 输出要简短，只输出译文本身，不要引号、解释或前后缀。\n' +
    '示例（德语，仅示意格式）：CIRS Community-Industrie-Ersatzpaket\n\n' +
    '【原文】'+NAME_EN+'\n\n【当前译文（不合格）】'+cur+'\n\n请给出合格译文：';
  let best=null;
  for(let k=0;k<5&&!best;k++){try{let tr=(await call(prompt)).trim().replace(/^["'「」]+|["'」」]+$/g,'');
    if(hardBad(NAME_EN,tr)||tr===NAME_EN)continue;
    if(!/CIRS/.test(tr)||/FIRS/.test(tr))continue;
    if(/Community Industry|Replacement Set/i.test(tr))continue;
    if(tr.length>90)continue;
    const letters=tr.replace(/CIRS/g,'').replace(/[^A-Za-zÀ-ɏ]/g,'');
    if(letters.length<4)continue;
    best=tr;
  }catch(e){await sleep(600*(k+1));}}
  if(best){fs.appendFileSync(path.join(OUT,lang+'.jsonl'),JSON.stringify({i:idx,tr:best})+'\n','utf8');
    console.log('FIXED '+lang.padEnd(18)+' | OLD='+cur.slice(0,60)+'\n                     | NEW='+best.slice(0,85));changed++;}
  else console.log('KEEP  '+lang.padEnd(18)+' | '+cur.slice(0,85));
}
console.log('NAMEFIX2 changed='+changed);
