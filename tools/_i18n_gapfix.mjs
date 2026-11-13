#!/usr/bin/env node
/* Targeted gap fixer: recover the last missing entry and re-translate strings with
 * genuine leftover English words. Appends last-wins lines to out JSONL. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd(), WORK = path.join(ROOT, 'tools', '_i18n_work'), OUT = path.join(ROOT, 'tools', '_i18n_out');
const URL = 'https://index-translate.bilibili.com/v1/chat/completions', MODEL = 'Index-Translate-9B', TIMEOUT = 60000;
const PH = /\{([A-Za-z_0-9]*)\}/g;
const phList = s => (String(s).match(PH) || []).sort().join(',');
const NAMES = { portuguese_BR:'巴西葡萄牙语（Português do Brasil）', russian:'俄语（Русский）', tamil:'泰米尔语（தமிழ்）' };
const sleep = ms => new Promise(r => setTimeout(r, ms));
function loadOut(lang) {
  const f = path.join(OUT, lang + '.jsonl'), m = new Map();
  if (fs.existsSync(f)) for (const l of fs.readFileSync(f, 'utf-8').split('\n')) {
    if (!l.trim()) continue; try { const o = JSON.parse(l); if (Number.isInteger(o.i) && typeof o.tr === 'string') m.set(o.i, o.tr); } catch (e) {}
  }
  return m;
}
function append(lang, pairs) { fs.appendFileSync(path.join(OUT, lang + '.jsonl'), pairs.map(p => JSON.stringify({i:p[0],tr:p[1]})+'\n').join(''), 'utf-8'); }
function hardBad(en, tr) {
  if (!tr || typeof tr !== 'string' || !tr.trim()) return true;
  if (phList(en) !== phList(tr)) return true;
  if (/\uFFFD/.test(tr) || /[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(tr)) return true;
  for (const m of tr.matchAll(PH)) if (/[^\x00-\x7F]/.test(m[1])) return true;
  return false;
}
/* The 9B model sometimes drops the closing brace of the LAST placeholder, e.g.
 * '{YELLOW}Só...' becomes '{YELLOW>Só...'. Restore '{NAME>' -> '{NAME}'. */
function fixBrokenBrace(en, tr) {
  const names = [...String(en).matchAll(PH)].map(m => m[1]);
  let s = tr;
  for (const n of names) s = s.split('{' + n + '>').join('{' + n + '}');
  return s;
}
async function call(text, maxTokens) {
  const ctrl = new AbortController(), t = setTimeout(() => ctrl.abort(), TIMEOUT);
  try {
    const r = await fetch(URL, { method:'POST', signal:ctrl.signal,
      headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},
      body: JSON.stringify({ model:MODEL, messages:[{role:'user',content:text}], temperature:0.0,
        max_tokens:maxTokens||1024, stream:false, chat_template_kwargs:{enable_thinking:false} }) });
    const s = await r.text();
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const j = JSON.parse(s); return (j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || '';
  } finally { clearTimeout(t); }
}
function prompts(en, tgt) {
  const common = '【硬性要求】所有花括号占位符（如 {TINYFONT}、{BLACK}、{YELLOW}、{count}、{STRING}、{}）必须逐字原样保留，一个字符都不能改；保留 FIRS、CIRS、OpenTTD、FRAX 等专有名词不译。\n';
  return [
    '请将下面这句英语游戏文本翻译成' + tgt + '。\n' + common + '只输出译文，不要任何解释或前后缀。\n\n【源文】\n' + en,
    '请把以下 JSON 中 key "0" 的英语文本翻译成' + tgt + '。\n' + common + '请以相同 JSON 格式输出，key 不变，value 为译文。只输出 JSON，不要任何额外说明。\n\n' + JSON.stringify({0:en}),
    'Translate the following English game text into ' + tgt + '. Preserve every curly-brace placeholder exactly (e.g. {YELLOW}, {BLACK}, {}), including its closing brace. Output only the translation.\n\n' + en,
  ];
}
function extract(raw, jsonMode) {
  let s = String(raw).trim();
  if (jsonMode) { try { const j = JSON.parse(s); return String(j['0'] ?? j[0] ?? ''); } catch(e) { const a=s.indexOf('{'), b=s.lastIndexOf('}'); if(a>=0&&b>a) try { return String(JSON.parse(s.slice(a,b+1))['0'] ?? ''); } catch(e2){ return ''; } } return ''; }
  return s;
}
async function fixEntry(lang, i, en) {
  const tgt = NAMES[lang] || lang;
  const ps = prompts(en, tgt);
  for (let k = 0; k < ps.length; k++) {
    for (let a = 0; a < 2; a++) {
      try {
        const raw = await call(ps[k], 1024);
        let tr = extract(raw, k === 1);
        if (!tr) continue;
        tr = fixBrokenBrace(en, tr);
        if (!hardBad(en, tr)) return { tr, variant: k, broken: tr !== extract(raw, k===1) };
      } catch (e) { await sleep(500*(a+1)); }
    }
  }
  return null;
}
const FIX = [
  ['portuguese_BR', 604],
  ['russian', 31], ['russian', 32], ['russian', 290],
  ['tamil', 189], ['tamil', 195], ['tamil', 463],
];
let done = 0, fail = 0;
for (const [lang, i] of FIX) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8'));
  const en = w.entries[i].en;
  const cur = loadOut(lang).get(i);
  const r = await fixEntry(lang, i, en);
  if (r) { append(lang, [[i, r.tr]]); console.log('FIX ' + lang + ' ' + i + ' v=' + r.variant + (r.broken?' [brace-repaired]':'') + ' | EN=' + en.slice(0,60) + ' | OLD=' + String(cur===undefined?'(missing)':cur).slice(0,70) + ' | NEW=' + r.tr.slice(0,90)); done++; }
  else { console.log('FAIL ' + lang + ' ' + i + ' | EN=' + en.slice(0,80)); fail++; }
}
console.log('GAPFIX done=' + done + ' fail=' + fail);
