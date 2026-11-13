#!/usr/bin/env node
/* Glossary-guided repair of steel-industry mistranslations (tickets/flowers trap). */
import fs from 'node:fs';
const URL='https://index-translate.bilibili.com/v1/chat/completions';
const MODEL='Index-Translate-9B', CONC=8, TIMEOUT=60000, RETRIES=4;
const PH_RE=/\{([A-Za-z_0-9]*)\}/g;
const NAMES = {
  afrikaans:'南非荷兰语（Afrikaans）', arabic:'阿拉伯语（العربية）', belarusian:'白俄罗斯语（Беларуская）',
  catalan:'加泰罗尼亚语（Català）', croatian:'克罗地亚语（Hrvatski）', czech:'捷克语（Čeština）',
  danish:'丹麦语（Dansk）', dutch:'荷兰语（Nederlands）', esperanto:'世界语（Esperanto）',
  estonian:'爱沙尼亚语（Eesti）', finnish:'芬兰语（Suomi）', french:'法语（Français）',
  gaelic:'苏格兰盖尔语（Gàidhlig）', galician:'加利西亚语（Galego）', german:'德语（Deutsch）',
  hungarian:'匈牙利语（Magyar）', indonesian:'印度尼西亚语（Bahasa Indonesia）', italian:'意大利语（Italiano）',
  japanese:'日语（日本語）', korean:'韩语（한국어）', latin:'拉丁语（Latina）',
  luxembourgish:'卢森堡语（Lëtzebuergesch）', norwegian_bokmal:'书面挪威语（Norsk bokmål）',
  polish:'波兰语（Polski）', portuguese:'葡萄牙语（Português）', portuguese_BR:'巴西葡萄牙语（Português do Brasil）',
  romanian:'罗马尼亚语（Română）', russian:'俄语（Русский）', serbian:'塞尔维亚语（Srpski，请使用拉丁字母）',
  simplified_chinese:'简体中文', slovak:'斯洛伐克语（Slovenčina）', spanish:'西班牙语（Español）',
  spanish_MX:'墨西哥西班牙语（Español de México）', swedish:'瑞典语（Svenska）',
  tamil:'泰米尔语（தமிழ்）', traditional_chinese:'繁体中文', turkish:'土耳其语（Türkçe）', welsh:'威尔士语（Cymraeg）',
};
// Known WRONG renderings observed in the corpus: tickets / flowers / nonsense.
const BAD = /\b(flors|billetes|bilhetes|biletes|bilety|blöme|цветы|билеты|květiny|kvety|flores|fleurs|blumen|blomster|kukat|blóm|tickets|flowers|banknotes)\b/i;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const phList=s=>(String(s).match(PH_RE)||[]).sort().join(',');
function hard(en,tr){
  if(!tr||!tr.trim()) return ['empty'];
  const h=[];
  if(phList(en)!==phList(tr)) h.push('ph');
  if(/\uFFFD/.test(tr)) h.push('replacement');
  if(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(tr)) h.push('ctrl');
  for(const m of tr.matchAll(PH_RE)) if(/[^\x00-\x7F]/.test(m[1])) {h.push('phtranslated');break;}
  if(/【|】|只输出|^(译文|翻译|注意|说明)[:：]/m.test(tr)) h.push('meta');
  return h;
}
function prompt(x,tgt){
  const egs = x.examples.map(e=>'  - '+e.lang+': '+e.tr).join('\n');
  return '你是'+tgt+'本地化审校员。下面是一句游戏内货物说明的英语原文和当前译文。当前译文把钢铁工业术语误译了或整句没译，请给出地道的'+tgt+'译文。\n' +
    '【词义（极其重要，不要搞错）】billets=方形钢坯（半成品钢材，不是"票/纸币"）；blooms=大型钢坯（半成品钢材，不是"花朵"）；ingots=铸锭/金属锭；slabs=板坯/厚钢板。绝对不要译成"票、纸币、钞票、花朵、鲜花"之类的词。若该语言没有对应的行业词，可直接保留英语技术词。\n' +
    '【硬性要求】所有花括号占位符（{WEIGHT}、{SIGNED_WORD}、{P 0 "" s}、{} 等）必须逐字原样保留；CIRS、FIRS、OpenTTD 等专有名词不译；不要输出译文之外的任何内容。\n' +
    '【同键的其他语言正确译法（供参考）】\n'+(egs||'  （无）')+'\n' +
    '【英语原文】\n'+x.en+'\n\n【当前译文（待修订）】\n'+x.tr+'\n\n只输出修订后的译文；若当前译文已经完全正确，就原样输出当前译文。';
}
async function call(text){
  const c=new AbortController(),t=setTimeout(()=>c.abort(),TIMEOUT);
  try{
    const r=await fetch(URL,{method:'POST',signal:c.signal,
      headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},
      body:JSON.stringify({model:MODEL,messages:[{role:'user',content:text}],temperature:0.0,
        max_tokens:2048,stream:false,chat_template_kwargs:{enable_thinking:false}})});
    const s=await r.text(); if(!r.ok) throw new Error('HTTP '+r.status);
    const j=JSON.parse(s);
    let v=(j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
    return v.replace(/^<think>[\s\S]*?<\/think>/,'').trim().replace(/^[\r\n]+|[\r\n]+$/g,'');
  } finally {clearTimeout(t);}
}
function validate(x,tr){
  const h=hard(x.en,tr); if(h.length) return h;
  if(tr===x.tr) return ['unchanged'];
  if(BAD.test(tr)) return ['known_bad_word'];
  // must remove at least one flagged English term
  const before=x.fix_terms.filter(t=>new RegExp('(?<![A-Za-z])'+t+'(?![A-Za-z])','i').test(x.tr)).length;
  const after=x.fix_terms.filter(t=>new RegExp('(?<![A-Za-z])'+t+'(?![A-Za-z])','i').test(tr)).length;
  if(after>=before) return ['no_term_removed'];
  return [];
}
async function main(){
  const T=JSON.parse(fs.readFileSync('tools/_i18n_residue_model_tasks.json','utf8'));
  const out=[], fails=[];
  for(let s=0;s<T.length;s+=CONC){
    const wave=T.slice(s,s+CONC);
    const res=await Promise.all(wave.map(async x=>{
      for(let a=0;a<RETRIES;a++){
        try{
          const tr=await call(prompt(x,NAMES[x.lang]||x.lang));
          const v=validate(x,tr);
          if(!v.length) return {...x,tr_new:tr};
          if(a===RETRIES-1) return {fail:x,why:v,sample:tr.slice(0,180)};
        }catch(e){if(a===RETRIES-1)return {fail:x,why:['http'],sample:String(e).slice(0,120)};}
        await sleep(700*(a+1));
      }
      return null;
    }));
    for(const y of res){if(!y)continue;if(y.fail)fails.push(y);else out.push(y);}
    console.log('  wave '+(s/CONC+1)+': +'+res.filter(y=>y&&!y.fail).length+'/'+wave.length);
  }
  fs.writeFileSync('tools/_i18n_residue_model_out.json',JSON.stringify(out,null,1),'utf8');
  fs.writeFileSync('tools/_i18n_residue_model_fails.json',JSON.stringify(fails,null,1),'utf8');
  console.log('RESIDUE MODEL changed='+out.length+' of '+T.length+' fails='+fails.length);
}
main().catch(e=>{console.error('FATAL',e);process.exit(1);});
