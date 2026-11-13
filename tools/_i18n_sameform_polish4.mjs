#!/usr/bin/env node
/* v4 same-form review: give cross-language majority hints, ask for definitive keep/translate. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT=process.cwd(), WORK=path.join(ROOT,'tools','_i18n_work'), OUT=path.join(ROOT,'tools','_i18n_out');
const URL='https://index-translate.bilibili.com/v1/chat/completions', MODEL='Index-Translate-9B', TIMEOUT=60000, BATCH=12, CONC=8, RETRIES=4;
const PH_LOOSE=/\{[^}]*\}/g, PH_STRICT=/\{([A-Za-z_0-9]*)\}/g;
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
async function call(text){const ctrl=new AbortController(),t=setTimeout(()=>ctrl.abort(),TIMEOUT);
  try{const r=await fetch(URL,{method:'POST',signal:ctrl.signal,headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},body:JSON.stringify({model:MODEL,messages:[{role:'user',content:text}],temperature:0,max_tokens:4096,stream:false,chat_template_kwargs:{enable_thinking:false}})});
    const s=await r.text();if(!r.ok)throw new Error('HTTP '+r.status+' '+s.slice(0,80));const j=JSON.parse(s);return (j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
  }finally{clearTimeout(t);}}
function parseJSON(raw){let s=String(raw).trim();try{const j=JSON.parse(s);for(const k of Object.keys(j))if(typeof j[k]==='string')j[k]=j[k].replace(/^[\r\n]+|[\r\n]+$/g,'');return j;}catch(e){}const a=s.indexOf('{'),b=s.lastIndexOf('}');if(a>=0&&b>a){const j=JSON.parse(s.slice(a,b+1));for(const k of Object.keys(j))if(typeof j[k]==='string')j[k]=j[k].replace(/^[\r\n]+|[\r\n]+$/g,'');return j;}throw new Error('no JSON');}
function hintText(c){
  if(!c.hints||!c.hints.length)return '';
  return '\n同项目其他语言对这条的译法参考：'+c.hints.map(h=>h.lang+'='+h.tr).join('；')+'。多数语言译成了不同于英语的形式，请据此判断目标语言是否也不应保留英语原词。';
}
function prompt(obj,tgt,cands){
  return '你是'+tgt+'游戏本地化终审。下面 JSON 的 value 目前与英语原文完全相同，需要你最终裁定：\n'+
    '对每条：若该词在'+tgt+'里确实有通用译法（哪怕是单字、短词、行业术语），必须给出'+tgt+'译文，不要照抄英文；仅当它是国际通用化学名/专有名词/品牌/代号，或'+tgt+'确实惯用同形借词时，才允许原样保留英语。\n'+
    '【硬性要求】所有花括号内容（{TINYFONT}、{BLACK}、{count}、{P 0 "" s}、{} 等）逐字原样保留；FIRS/CIRS/OpenTTD/FRAX 不译；塞尔维亚语用拉丁字母；不要输出 JSON 之外的任何内容。\n'+
    '以相同 key 输出 JSON，value 为最终译文（保留原词就输出原词）。只输出 JSON，不要解释。\n\n'+
    cands.map(c=>'#"'+c.i+'": '+JSON.stringify(c.en)+hintText(c)).join('\n')+'\n\n'+JSON.stringify(obj);
}
const ONLY=new Set(process.argv.slice(2));
const cands=JSON.parse(fs.readFileSync('tools/_i18n_sameform_v4_candidates.json','utf8'));
const byLang=new Map();for(const c of cands){if(!byLang.has(c.lang))byLang.set(c.lang,[]);byLang.get(c.lang).push(c);}
let changed=0, kept=0, unmapped=0, waveFail=0;
for(const lang of [...byLang.keys()].sort()){
  if(ONLY.size&&!ONLY.has(lang))continue;
  const w=JSON.parse(fs.readFileSync(path.join(WORK,lang+'.json'),'utf8'));
  const refmap=new Map();for(let i=0;i<w.entries.length;i++)for(const [f,k] of w.entries[i].refs)refmap.set(f+'::'+k,i);
  const items=[];for(const c of byLang.get(lang)){const idxs=[];for(const r of c.refs){const i=refmap.get(r.file+'::'+r.key);if(i!==undefined)idxs.push(i);else unmapped++;}if(idxs.length)items.push({c,idxs:[...new Set(idxs)]});}
  if(!items.length)continue;
  const out=loadOut(lang), pairs=[];
  for(let s=0;s<items.length;s+=BATCH*CONC){
    const waves=[];for(let a=s;a<Math.min(s+BATCH*CONC,items.length);a+=BATCH)waves.push(items.slice(a,a+BATCH));
    const res=await Promise.all(waves.map(async grp=>{
      const obj={};for(const x of grp)for(const i of x.idxs)obj[String(i)]=x.c.en;
      const cinfo=grp.map(x=>({i:String(x.idxs[0]),en:x.c.en,hints:x.c.hints}));
      for(let k=0;k<RETRIES;k++){
        try{const resp=await call(prompt(obj,NAMES[lang]||lang,cinfo));
          const j=parseJSON(resp);const got=[];
          for(const x of grp){const v=j[String(x.idxs[0])];if(typeof v!=='string')continue;const bad=hardBad(x.c.en,v);if(bad)continue;if(v===x.c.en)continue;for(const i of x.idxs)got.push([i,v]);}
          return got;
        }catch(e){if(k===RETRIES-1){waveFail++;console.log('  WAVEFAIL '+lang+' :: '+String(e.message||e).slice(0,120));return [];}await sleep(700*(k+1));}
      } return [];
    }));
    pairs.push(...res.flat());
  }
  const fresh=pairs.filter(([i,tr])=>out.get(i)!==tr);
  if(fresh.length){fs.appendFileSync(path.join(OUT,lang+'.jsonl'),fresh.map(([i,tr])=>JSON.stringify({i,tr})+'\n').join(''),'utf8');changed+=fresh.length;}
  kept+=items.length-fresh.length;
  console.log(lang.padEnd(22)+' reviewed='+String(items.length).padStart(3)+' improved='+String(fresh.length).padStart(3)+' waveFail='+waveFail);
  for(const [i,tr] of fresh.slice(0,4))console.log('      '+tr.slice(0,100));
}
console.log('SAMEFORM4 changed='+changed+' kept='+kept+' unmapped='+unmapped+' waveFail='+waveFail);
