#!/usr/bin/env node
/* Glossary-assisted repair for a handful of domain terms the plain prompt mistranslated. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd(), WORK = path.join(ROOT, 'tools', '_i18n_work'), OUT = path.join(ROOT, 'tools', '_i18n_out');
const URL = 'https://index-translate.bilibili.com/v1/chat/completions', MODEL = 'Index-Translate-9B', TIMEOUT = 60000;
const PH = /\{([A-Za-z_0-9]*)\}/g;
const phList = s => (String(s).match(PH) || []).sort().join(',');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const GLOSS = {
  'russian:31': '这是钢铁工业术语：billet = 方坯/钢坯（俄语 заготовка），bloom = 初轧方坯/大钢坯（俄语 блюм）。请译成“Заготовки и блюмы”这类钢铁术语，绝对不要译成 билет（票）或 цветы（花）。',
  'russian:32': '这是钢铁工业术语：billets = заготовки, blooms = блюмы, ingots = слитки, slabs = слябы。整句都要译成俄语钢铁术语，不得残留任何英文单词，也不要译成 билет/цветы。',
  'russian:290': 'roadstone = 道路碎石/筑路石料（俄语 щебень）。Roadstone Plant 指生产筑路碎石的工厂，请译成纯俄语（如 Завод щебня），不得残留英文 Roadstone。',
  'tamil:189': 'Lye = கார நீர் / சோடியம் ஹைட்ராக்சைடு கரைசல், Caustic Soda = காஸ்டிக் சோடா / சோடியம் ஹைட்ராக்சைடு。请把这两个英文词也译成泰米尔语，不要残留拉丁字母（专有化学名可意译）。',
  'tamil:195': 'Kaolin = காவ்லின் / கயோலின்（高岭土）。请把这个英文词也译成泰米尔语，不要残留拉丁字母。',
  'tamil:463': 'wool = கம்பளி（羊毛）, bale = மூட்டை / கட்டு（捆）。请把英文词 bale 和 wool 都译成泰米尔语，花括号占位符 {SIGNED_WORD} 与 {P 0 "" s} 必须原样保留。',
};
const TGT = { russian:'俄语（Русский）', tamil:'泰米尔语（தமிழ்）' };
function loadOut(lang) { const m=new Map(); const f=path.join(OUT,lang+'.jsonl');
  if (fs.existsSync(f)) for (const l of fs.readFileSync(f,'utf-8').split('\n')) { if(!l.trim())continue; try{const o=JSON.parse(l); if(Number.isInteger(o.i)&&typeof o.tr==='string')m.set(o.i,o.tr);}catch(e){} } return m; }
function hardBad(en,tr){ if(!tr||typeof tr!=='string'||!tr.trim())return true; if(phList(en)!==phList(tr))return true; if(/\uFFFD/.test(tr)||/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(tr))return true; for(const m of tr.matchAll(PH))if(/[^\x00-\x7F]/.test(m[1]))return true; return false; }
function latinResidue(lang,tr){ const s=tr.replace(PH,' '); return /[A-Za-z]{4,}/.test(s); }
async function call(text){ const ctrl=new AbortController(),t=setTimeout(()=>ctrl.abort(),TIMEOUT);
  try{ const r=await fetch(URL,{method:'POST',signal:ctrl.signal,headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},body:JSON.stringify({model:MODEL,messages:[{role:'user',content:text}],temperature:0,max_tokens:1024,stream:false,chat_template_kwargs:{enable_thinking:false}})});
    const s=await r.text(); if(!r.ok)throw new Error('HTTP '+r.status); const j=JSON.parse(s); return (j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
  } finally { clearTimeout(t); } }
let done=0;
for (const key of Object.keys(GLOSS)) {
  const [lang,si]=key.split(':'), i=+si;
  const w=JSON.parse(fs.readFileSync(path.join(WORK,lang+'.json'),'utf-8'));
  const en=w.entries[i].en, cur=loadOut(lang).get(i);
  const prompt='你是'+TGT[lang]+'本地化审校员，正在修订一条游戏内货物名称/描述。\n' +
    '【术语表】'+GLOSS[key]+'\n' +
    '【硬性要求】所有花括号占位符（如 {TINYFONT}、{BLACK}、{YELLOW}、{count}、{STRING}、{SIGNED_WORD}、{P 0 "" s}、{}）必须逐字原样保留，包括右花括号；FIRS、CIRS、OpenTTD、FRAX 等专有名词不译；全句不得残留任何未翻译的英文普通词；只输出译文，不要任何解释或前后缀。\n\n' +
    '【英语原文】\n'+en+'\n\n【当前译文（可能错误）】\n'+String(cur||'')+'\n\n请给出正确译文：';
  let best=null;
  for(let k=0;k<3 && !best;k++){ try{ let tr=(await call(prompt)).trim();
      // repair the model's habit of dropping the last closing brace
      for(const n of [...String(en).matchAll(PH)].map(m=>m[1])) tr=tr.split('{'+n+'>').join('{'+n+'}');
      if(hardBad(en,tr)) continue;
      if(latinResidue(lang,tr)) continue;
      if(tr===en) continue;
      best=tr;
    }catch(e){ await sleep(600*(k+1)); } }
  if(best){ fs.appendFileSync(path.join(OUT,lang+'.jsonl'), JSON.stringify({i,tr:best})+'\n','utf-8');
    console.log('OK   '+lang+' '+i+' | EN='+en.slice(0,55)+'\n     OLD='+String(cur||'(missing)').slice(0,90)+'\n     NEW='+best.slice(0,120)); done++; }
  else console.log('KEEP '+lang+' '+i+' (no soft-clean result) cur='+String(cur||'').slice(0,100));
}
console.log('GLOSSFIX changed='+done);
