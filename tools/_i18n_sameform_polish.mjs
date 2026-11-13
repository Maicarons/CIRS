#!/usr/bin/env node
/* Final same-form review: for short strings still identical to English, ask the model
 * to translate into the target language (keeping genuine loanwords/proper nouns/codes).
 * Appends only hard-clean, changed results to out JSONL for idempotent re-apply. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT=process.cwd(), WORK=path.join(ROOT,'tools','_i18n_work'), OUT=path.join(ROOT,'tools','_i18n_out');
const URL='https://index-translate.bilibili.com/v1/chat/completions', MODEL='Index-Translate-9B', TIMEOUT=60000, BATCH=12, CONC=8, RETRIES=3;
const PH_LOOSE=/\{[^}]*\}/g;
const PH_STRICT=/\{([A-Za-z_0-9]*)\}/g;
const phLoose=s=>(String(s).match(PH_LOOSE)||[]).sort().join('|');
const phStrict=s=>(String(s).match(PH_STRICT)||[]).sort().join(',');
const NAMES={
  afrikaans:'南非荷兰语（Afrikaans）', arabic:'阿拉伯语（العربية）', belarusian:'白俄罗斯语（Беларуская）',
  catalan:'加泰罗尼亚语（Català）', croatian:'克罗地亚语（Hrvatski）', czech:'捷克语（Čeština）',
  danish:'丹麦语（Dansk）', dutch:'荷兰语（Nederlands）', esperanto:'世界语（Esperanto）',
  estonian:'爱沙尼亚语（Eesti）', finnish:'芬兰语（Suomi）', french:'法语（Français）',
  gaelic:'苏格兰盖尔语（Gàidhlig）', galician:'加利西亚语（Galego）', german:'德语（Deutsch）',
  hungarian:'匈牙利语（Magyar）', indonesian:'印度尼西亚语（Bahasa Indonesia）', italian:'意大利语（Italiano）',
  japanese:'日语（日本語）', korean:'韩语（한국어）', latin:'拉丁语（Latina）',
  luxembourgish:'卢森堡语（Lëtzebuergesch）', norwegian_bokmal:'书面挪威语（Norsk bokmål）', polish:'波兰语（Polski）',
  portuguese:'葡萄牙语（Português）', portuguese_BR:'巴西葡萄牙语（Português do Brasil）', romanian:'罗马尼亚语（Română）',
  russian:'俄语（Русский）', serbian:'塞尔维亚语（Srpski，拉丁字母）', simplified_chinese:'简体中文',
  slovak:'斯洛伐克语（Slovenčina）', spanish:'西班牙语（Español）', spanish_MX:'墨西哥西班牙语（Español de México）',
  swedish:'瑞典语（Svenska）', tamil:'泰米尔语（தமிழ்）', traditional_chinese:'繁体中文',
  turkish:'土耳其语（Türkçe）', welsh:'威尔士语（Cymraeg）',
};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function loadOut(lang){const m=new Map();const f=path.join(OUT,lang+'.jsonl');if(fs.existsSync(f))for(const l of fs.readFileSync(f,'utf8').split('\n')){if(!l.trim())continue;try{const o=JSON.parse(l);if(Number.isInteger(o.i)&&typeof o.tr==='string')m.set(o.i,o.tr);}catch(e){}}return m;}
function hardBad(en,tr){
  if(!tr||typeof tr!=='string'||!tr.trim())return 'empty';
  if(phLoose(en)!==phLoose(tr))return 'ph';
  if(phStrict(en)!==phStrict(tr))return 'ph2';
  if(/\uFFFD/.test(tr))return 'replacement';
  if(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\r\n]/.test(tr))return 'ctrl';
  for(const m of tr.matchAll(PH_STRICT))if(/[^\x00-\x7F]/.test(m[1]))return 'phtranslated';
  if(/【|】|译文[:：]|翻译[:：]|只输出|^>|^#/.test(tr))return 'meta';
  if(tr.length>en.length*3+60)return 'toolong';
  return null;
}
function isTarget(en){
  const residue=en.replace(PH_LOOSE,'').trim();
  if(!/[A-Za-z]{3,}/.test(residue))return false;          // pure placeholder template
  if(/^[A-Z0-9]{1,5}[.]?$/.test(en.trim()))return false;   // badge / short code e.g. SEA
  return true;
}
async function call(text){const ctrl=new AbortController(),t=setTimeout(()=>ctrl.abort(),TIMEOUT);
  try{const r=await fetch(URL,{method:'POST',signal:ctrl.signal,headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},body:JSON.stringify({model:MODEL,messages:[{role:'user',content:text}],temperature:0,max_tokens:8192,stream:false,chat_template_kwargs:{enable_thinking:false}})});
    const s=await r.text();if(!r.ok)throw new Error('HTTP '+r.status);const j=JSON.parse(s);return (j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
  }finally{clearTimeout(t);}}
function parseJSON(raw){let s=String(raw).trim();try{return JSON.parse(s);}catch(e){}const a=s.indexOf('{'),b=s.lastIndexOf('}');if(a>=0&&b>a)return JSON.parse(s.slice(a,b+1));throw new Error('no JSON');}
function prompt(obj,tgt){
  return '你是'+tgt+'本地化审校员。下面 JSON 的 key 是条目号，value 是翻译文件中仍与英文原文完全相同的游戏/网站短文本。\n' +
    '请逐条给出地道、准确的'+tgt+'译文；只有当该词在'+tgt+'中本来就同形（国际通用借词、专有名词、品牌、货物两字母代码、缩写代号）时，才保持原样。\n' +
    '【硬性要求】所有花括号内容（{TINYFONT}、{BLACK}、{count}、{P 0 "" s}、{} 等）必须逐字原样保留，不得增删或改写；FIRS、CIRS、OpenTTD、FRAX 等专有名词不译；塞尔维亚语用拉丁字母；不要输出 JSON 之外的任何内容。\n\n' +
    '【待审校】\n'+JSON.stringify(obj)+'\n\n请以相同 key 输出 JSON，value 为确认或修正后的译文。只输出 JSON。';
}
const raw=fs.readFileSync('tools/_i18n_same_real_files.txt','utf8').trim().split('\n');
const byLang=new Map(); let unmapped=[];
for(const line of raw){if(!line.trim())continue;const [lang,file,key,en]=line.split('|'); if(!isTarget(en))continue;
  if(!byLang.has(lang))byLang.set(lang,[]); byLang.get(lang).push({file,key,en}); }
let changed=0, skipped=0;
for(const lang of [...byLang.keys()].sort()){
  const w=JSON.parse(fs.readFileSync(path.join(WORK,lang+'.json'),'utf8'));
  const refmap=new Map();
  for(let i=0;i<w.entries.length;i++)for(const [f,k] of w.entries[i].refs)refmap.set(f+'::'+k,i);
  const items=[];
  for(const x of byLang.get(lang)){const i=refmap.get(x.file+'::'+x.key);if(i===undefined){unmapped.push(lang+'|'+x.file+'|'+x.key+'|'+x.en);continue;}items.push({i,en:x.en});}
  if(!items.length)continue;
  const out=loadOut(lang), pairs=[];
  for(let s=0;s<items.length;s+=BATCH*CONC){
    const waves=[];for(let a=s;a<Math.min(s+BATCH*CONC,items.length);a+=BATCH)waves.push(items.slice(a,a+BATCH));
    const res=await Promise.all(waves.map(async grp=>{
      const obj={};grp.forEach(x=>obj[String(x.i)]=x.en);
      for(let k=0;k<RETRIES;k++){try{const j=parseJSON(await call(prompt(obj,NAMES[lang]||lang),8192));
        const got=[];for(const x of grp){const v=j[String(x.i)];if(typeof v!=='string')continue;if(v===x.en)continue;if(hardBad(x.en,v))continue;got.push([x.i,v]);}return got;
      }catch(e){if(k===RETRIES-1)return [];await sleep(700*(k+1));}}return [];}));
    pairs.push(...res.flat());
  }
  for(const [i,tr] of pairs){if(out.get(i)===tr)continue;}
  const fresh=pairs.filter(([i,tr])=>out.get(i)!==tr);
  if(fresh.length){fs.appendFileSync(path.join(OUT,lang+'.jsonl'),fresh.map(([i,tr])=>JSON.stringify({i,tr})+'\n').join(''),'utf8');changed+=fresh.length;}
  skipped+=items.length-fresh.length;
  console.log(lang.padEnd(22)+' reviewed='+String(items.length).padStart(3)+' improved='+fresh.length);
  if(fresh.length)for(const [i,tr] of fresh.slice(0,3))console.log('      '+tr.slice(0,95));
}
console.log('SAMEFORM POLISH changed='+changed+' kept='+skipped+' unmapped='+unmapped.length);
if(unmapped.length)fs.writeFileSync('tools/_i18n_unmapped.txt',unmapped.join('\n')+'\n','utf8');
