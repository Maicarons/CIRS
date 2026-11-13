#!/usr/bin/env node
/* Post-translation identity polish: find translations identical to English that are
 * real words/short phrases (not brand names, cargo codes, punctuation), and ask the
 * model to confirm or produce a proper target-language translation. Appends to out JSONL. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd(), WORK = path.join(ROOT, 'tools', '_i18n_work'), OUT = path.join(ROOT, 'tools', '_i18n_out');
const URL = 'https://index-translate.bilibili.com/v1/chat/completions';
const MODEL = 'Index-Translate-9B', BATCH = 12, CONC = 8, TIMEOUT = 60000, RETRIES = 4;
const PH = /\{([A-Za-z_0-9]*)\}/g;
const NAMES = {
  afrikaans:'南非荷兰语', arabic:'阿拉伯语', belarusian:'白俄罗斯语', catalan:'加泰罗尼亚语',
  croatian:'克罗地亚语', czech:'捷克语', danish:'丹麦语', dutch:'荷兰语', esperanto:'世界语',
  estonian:'爱沙尼亚语', finnish:'芬兰语', french:'法语', gaelic:'苏格兰盖尔语', galician:'加利西亚语',
  german:'德语', hungarian:'匈牙利语', indonesian:'印度尼西亚语', italian:'意大利语', japanese:'日语',
  korean:'韩语', latin:'拉丁语', luxembourgish:'卢森堡语', norwegian_bokmal:'书面挪威语', polish:'波兰语',
  portuguese:'葡萄牙语', portuguese_BR:'巴西葡萄牙语', romanian:'罗马尼亚语', russian:'俄语',
  serbian:'塞尔维亚语', simplified_chinese:'简体中文', slovak:'斯洛伐克语', spanish:'西班牙语',
  spanish_MX:'墨西哥西班牙语', swedish:'瑞典语', tamil:'泰米尔语', traditional_chinese:'繁体中文',
  turkish:'土耳其语', welsh:'威尔士语',
};
const BRAND = /^(FIRS|CIRS|OpenTTD|FRAX|NewGRF|GRFID|Python|makefile|GitHub|Issue|pull request|GPL|TOML|fork|git|JSON|NML|Gung-ho|Xcode|Windows|macOS|Linux|Unix|OpenGFX|Total Town Replacement Set|STSW|E\d+|CABBAGE|ID|LAND|Mild Mild West|OpenTTD|BaNaNas|SVN|URL|HTML|CSS|XML|API|CLI|UTF|RGB|AI|PDF|ZIP|RAR|EXE|DLL|INI|CFG|LOG|TXT|MD|PNG|JPG|GIF|SVG|MP3|WAV|OGG|TTF|OTF)/i;
const CODE = /^\{[A-Za-z_0-9]*\}[A-Z0-9]{1,5}$/;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const phList = s => (String(s).match(PH) || []).sort().join(',');
function loadOut(lang) {
  const f = path.join(OUT, lang + '.jsonl'), m = new Map();
  if (fs.existsSync(f)) for (const l of fs.readFileSync(f, 'utf-8').split('\n')) {
    if (!l.trim()) continue;
    try { const o = JSON.parse(l); if (Number.isInteger(o.i) && typeof o.tr === 'string') m.set(o.i, o.tr); } catch (e) {}
  }
  return m;
}
function appendOut(lang, pairs) {
  fs.appendFileSync(path.join(OUT, lang + '.jsonl'), pairs.map(p => JSON.stringify({ i:p[0], tr:p[1] }) + '\n').join(''), 'utf-8');
}
function isCandidate(en) {
  const s = en.trim();
  if (s.length < 4) return false;
  if (!/[A-Za-z]{3,}/.test(s)) return false;
  if (CODE.test(s)) return false;
  if (BRAND.test(s)) return false;
  const stripped = s.replace(PH, ' ').trim();
  if (stripped.length < 3 || !/[A-Za-z]{3,}/.test(stripped)) return false;
  if (/^(E\d+|v?\d+(\.\d+)*\+?|[A-Z]{1,4})$/i.test(stripped)) return false;
  return true;
}
function prompt(obj, tgt) {
  return '你是' + tgt + '本地化审校员。下面 JSON 的 value 与英语原文完全相同。请逐条判断：如果该词/短语在' + tgt + '中本来就同形（专有名词、国际通用词、技术代号、货物代码），保持原样；否则给出地道、简洁的' + tgt + '译文。\n' +
    '【硬性要求】所有花括号占位符（如 {TINYFONT}、{BLACK}、{count}、{STRING}、{}）必须逐字原样保留，不得增删或改写。\n' +
    '保留 FIRS、CIRS、OpenTTD、FRAX 等专有名词不译。不要输出 JSON 之外的任何内容。\n\n' +
    '【待审校文本】\n' + JSON.stringify(obj) + '\n\n请以相同 key 输出 JSON，value 为确认或修正后的译文。只输出 JSON。';
}
async function call(text, maxTokens) {
  const ctrl = new AbortController(), t = setTimeout(() => ctrl.abort(), TIMEOUT);
  try {
    const r = await fetch(URL, { method:'POST', signal:ctrl.signal,
      headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},
      body: JSON.stringify({ model:MODEL, messages:[{role:'user',content:text}], temperature:0.0,
        max_tokens:maxTokens || 8192, stream:false, chat_template_kwargs:{enable_thinking:false} }) });
    const s = await r.text();
    if (!r.ok) throw new Error('HTTP ' + r.status + ' ' + s.slice(0,80));
    const j = JSON.parse(s); return (j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || '';
  } finally { clearTimeout(t); }
}
function parseJSON(raw) {
  let s = raw.trim(); try { return JSON.parse(s); } catch (e) {}
  const a = s.indexOf('{'), b = s.lastIndexOf('}');
  if (a >= 0 && b > a) return JSON.parse(s.slice(a, b+1));
  throw new Error('no JSON');
}
function hardBad(en, tr) {
  if (tr == null || typeof tr !== 'string' || !tr.trim()) return true;
  if (phList(en) !== phList(tr)) return true;
  if (/\uFFFD/.test(tr) || /[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(tr)) return true;
  for (const m of tr.matchAll(/\{([A-Za-z_0-9]*)\}/g)) if (/[^\x00-\x7F]/.test(m[1])) return true;
  return false;
}
async function runLang(lang) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8'));
  const m = loadOut(lang), tgt = NAMES[lang] || lang;
  const cand = [];
  for (let i = 0; i < w.entries.length; i++) {
    const tr = m.get(i); if (tr === undefined || tr !== w.entries[i].en) continue;
    if (isCandidate(w.entries[i].en)) cand.push(i);
  }
  if (!cand.length) { console.log(lang.padEnd(24) + 'identity=0'); return 0; }
  let changed = 0;
  for (let s = 0; s < cand.length; s += BATCH * CONC) {
    const wave = [];
    for (let a = s; a < Math.min(s + BATCH * CONC, cand.length); a += BATCH) wave.push(cand.slice(a, a + BATCH));
    const res = await Promise.all(wave.map(async idxs => {
      const obj = {}; idxs.forEach(i => obj[String(i)] = w.entries[i].en);
      for (let k = 0; k < RETRIES; k++) {
        try {
          const j = parseJSON(await call(prompt(obj, tgt), 8192));
          const got = [];
          for (const i of idxs) {
            const v = j[String(i)];
            if (typeof v === 'string' && !hardBad(w.entries[i].en, v) && v !== w.entries[i].en) got.push([i, v]);
          }
          return got;
        } catch (e) { if (k === RETRIES-1) return []; await sleep(700*(k+1)); }
      }
      return [];
    }));
    const pairs = res.flat();
    if (pairs.length) { appendOut(lang, pairs); changed += pairs.length; }
  }
  console.log(lang.padEnd(24) + 'identity=' + cand.length + ' improved=' + changed);
  return changed;
}
const args = process.argv.slice(2);
const langs = args.length ? args : fs.readdirSync(WORK).filter(f => f.endsWith('.json') && !f.startsWith('_')).map(f => f.slice(0,-5)).sort();
let total = 0;
for (const l of langs) { try { total += await runLang(l); } catch (e) { console.log(l + ' FATAL ' + String(e.stack||e).slice(0,300)); } }
console.log('IDENTITY POLISH TOTAL improved=' + total);
