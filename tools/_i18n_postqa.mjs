#!/usr/bin/env node
/* Post-job QA + repair for all 38 languages.
 * 1) single-string recovery for any missing index (resume-safe).
 * 2) QA flags: latin_residue (ar/ru/be/sr/ta), no_script (non-Latin langs),
 *    identity (>=4-word unchanged), meta leaks, wrong script.
 * 3) repair flagged entries via a targeted polish prompt; accept only results
 *    that reduce soft-flag count and pass all hard checks.
 * Usage: node tools/_i18n_postqa.mjs [lang ...]  (default: all)
 */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd(), WORK = path.join(ROOT, 'tools', '_i18n_work'), OUT = path.join(ROOT, 'tools', '_i18n_out');
const URL = 'https://index-translate.bilibili.com/v1/chat/completions';
const MODEL = 'Index-Translate-9B', BATCH = 12, CONC = 8, TIMEOUT = 60000, RETRIES = 4;
const PH_RE = /\{([A-Za-z_0-9]*)\}/g;
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
  romanian:'罗马尼亚语（Română）', russian:'俄语（Русский）', serbian:'塞尔维亚语（Srpski，请使用拉丁字母，与项目既有塞尔维亚语料一致）',
  simplified_chinese:'简体中文', slovak:'斯洛伐克语（Slovenčina）', spanish:'西班牙语（Español）',
  spanish_MX:'墨西哥西班牙语（Español de México）', swedish:'瑞典语（Svenska）',
  tamil:'泰米尔语（தமிழ்）', traditional_chinese:'繁体中文', turkish:'土耳其语（Türkçe）', welsh:'威尔士语（Cymraeg）',
};
const BRANDS = /(FIRS|CIRS|OpenTTD|FRAX|GitHub|Issue|pull request|GPL|NewGRF|TOML|makefile|fork|git|GRFID|Python|Gung-ho|Windows|macOS|Linux|Unix|Xcode|NML|JSON|ports tree|OpenGFX|Total Town Replacement Set|STSW|CB|ID|LAND|CABBAGE)/i;
const CYRILLIC = /[\u0400-\u04FF]/, KANA = /[\u3040-\u30FF]/;
const NONLATIN = /[^\x00-\x7F]/;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const phList = s => (String(s).match(PH_RE) || []).sort().join(',');
function loadOut(lang) {
  const f = path.join(OUT, lang + '.jsonl'), m = new Map();
  if (fs.existsSync(f)) for (const l of fs.readFileSync(f, 'utf-8').split('\n')) {
    if (!l.trim()) continue;
    try { const o = JSON.parse(l); if (Number.isInteger(o.i) && typeof o.tr === 'string') m.set(o.i, o.tr); } catch (e) {}
  }
  return m;
}
function appendOut(lang, pairs) { fs.appendFileSync(path.join(OUT, lang + '.jsonl'), pairs.map(p => JSON.stringify({ i:p[0], tr:p[1] }) + '\n').join(''), 'utf-8'); }
function hardIssues(en, tr) {
  const h = [];
  if (tr == null || typeof tr !== 'string' || !tr.trim()) { h.push('empty'); return h; }
  if (phList(en) !== phList(tr)) h.push('ph');
  if (/\uFFFD/.test(tr)) h.push('replacement');
  if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(tr)) h.push('ctrl');
  for (const m of tr.matchAll(PH_RE)) if (/[^\x00-\x7F]/.test(m[1])) { h.push('phtranslated'); break; }
  return h;
}
function softIssues(en, tr, lang) {
  const s = [];
  if (/【|】|\[硬性|\[注意|\[软性|^>|^#|^(翻译|译文|注意|说明|提示)[:：]|只输出|源文】|Do not translate|Ne pas traduire|翻訳しない|traduci|no traduzca|请勿翻译/i.test(tr)) s.push('meta');
  if (lang === 'japanese' && CYRILLIC.test(tr)) s.push('wrongscript');
  if (lang === 'korean' && (KANA.test(tr) || CYRILLIC.test(tr))) s.push('wrongscript');
  const latinText = tr.replace(PH_RE, ' ');
  // Serbian uses Latin script in this project (FIRS 4.x serbian.lng is all Latin).
  if (['arabic','russian','belarusian','tamil'].includes(lang) && /[A-Za-z]{4,}/.test(latinText) && !BRANDS.test(latinText)) s.push('latin');
  if (tr === en && en.trim().split(/\s+/).length >= 4) s.push('identity');
  if (['japanese','korean','tamil','arabic','russian','belarusian','traditional_chinese','simplified_chinese'].includes(lang) &&
      en.trim().split(/\s+/).length >= 5 && !NONLATIN.test(tr)) s.push('no_script');
  return s;
}
function singlePrompt(en, tgt) {
  return '请将下面这句英语游戏/网站文本翻译成' + tgt + '。\n' +
    '【硬性要求】所有花括号占位符（如 {TINYFONT}、{BLACK}、{count}、{STRING}、{}）必须逐字原样保留，不得增删或改写；保留 FIRS、CIRS、OpenTTD、FRAX 等专有名词不译。\n' +
    '只输出译文，不要任何解释或前后缀。\n\n【源文】\n' + en;
}
function repairPrompt(obj, tgt) {
  return '你是' + tgt + '本地化审校员。下面 JSON 的 key 对应【英语原文】与【当前译文】。当前译文存在下列问题之一：混入未翻译的英文词、整句未译、与原文完全相同、或输出了错误的文字体系。请给出地道、准确的' + tgt + '译文。\n' +
    '【硬性要求】所有花括号占位符（如 {TINYFONT}、{BLACK}、{count}、{STRING}、{}）必须逐字原样保留，不得增删或改写；保留 FIRS、CIRS、OpenTTD、FRAX 等专有名词不译；塞尔维亚语一律使用拉丁字母；不要输出 JSON 之外的任何内容。\n\n' +
    '【待修订】\n' + JSON.stringify(obj) + '\n\n请以相同 key 输出 JSON，value 为修订后的译文。只输出 JSON。';
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
async function runLang(lang) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8'));
  const tgt = NAMES[lang] || lang;
  let map = loadOut(lang);
  // Phase 1: recover missing.
  const miss = [];
  for (let i = 0; i < w.count; i++) if (!map.has(i)) miss.push(i);
  let recovered = 0;
  for (let s = 0; s < miss.length; s += CONC) {
    const res = await Promise.all(miss.slice(s, s + CONC).map(async i => {
      for (let a = 0; a < RETRIES; a++) {
        try { const tr = (await call(singlePrompt(w.entries[i].en, tgt), 1024)).trim(); if (tr && !hardIssues(w.entries[i].en, tr).length) return [i, tr]; }
        catch (e) {} await sleep(600*(a+1));
      }
      return null;
    }));
    const pairs = res.filter(Boolean); if (pairs.length) { appendOut(lang, pairs); recovered += pairs.length; }
  }
  // Phase 2: repair soft issues.
  map = loadOut(lang);
  const flagged = [];
  for (let i = 0; i < w.count; i++) { const tr = map.get(i); if (tr === undefined) continue; if (softIssues(w.entries[i].en, tr, lang).length) flagged.push(i); }
  let improved = 0;
  for (let s = 0; s < flagged.length; s += BATCH * CONC) {
    const waves = [];
    for (let a = s; a < Math.min(s + BATCH * CONC, flagged.length); a += BATCH) waves.push(flagged.slice(a, a + BATCH));
    const res = await Promise.all(waves.map(async idxs => {
      const obj = {}; idxs.forEach(i => obj[String(i)] = { en: w.entries[i].en, cur: map.get(i) });
      for (let a = 0; a < RETRIES; a++) {
        try {
          const j = parseJSON(await call(repairPrompt(obj, tgt), 8192));
          const got = [];
          for (const i of idxs) {
            const v = j[String(i)]; if (typeof v !== 'string' || !v.trim()) continue;
            const en = w.entries[i].en, orig = map.get(i);
            if (hardIssues(en, v).length) continue;
            if (softIssues(en, v, lang).length < softIssues(en, orig, lang).length) got.push([i, v]);
          }
          return got;
        } catch (e) { if (a === RETRIES-1) return []; await sleep(700*(a+1)); }
      }
      return [];
    }));
    const pairs = res.flat(); if (pairs.length) { appendOut(lang, pairs); improved += pairs.length; }
  }
  map = loadOut(lang);
  let still = 0; for (let i = 0; i < w.count; i++) { const tr = map.get(i); if (tr === undefined || softIssues(w.entries[i].en, tr, lang).length) still++; }
  console.log(lang.padEnd(24) + ' have=' + map.size + '/' + w.count + ' recovered=' + recovered + ' improved=' + improved + ' remaining_soft=' + still);
  return { recovered, improved, still };
}
const args = process.argv.slice(2);
const langs = args.length ? args : fs.readdirSync(WORK).filter(f => f.endsWith('.json') && !f.startsWith('_')).map(f => f.slice(0,-5)).sort();
const g = { recovered:0, improved:0, still:0 };
for (const l of langs) { try { const r = await runLang(l); g.recovered += r.recovered; g.improved += r.improved; g.still += r.still; } catch (e) { console.log(l + ' FATAL ' + String(e.stack||e).slice(0,300)); } }
console.log('POSTQA TOTAL ' + JSON.stringify(g));
