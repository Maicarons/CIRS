#!/usr/bin/env node
/* Independent QA audit of tools/_i18n_out/<lang>.jsonl against work lists. */
import fs from 'node:fs';
import path from 'node:path';
const WORK = path.join(process.cwd(), 'tools', '_i18n_work');
const OUT = path.join(process.cwd(), 'tools', '_i18n_out');
const PH_RE = /\{([A-Za-z_0-9]*)\}/g;
const REPLACEMENT = String.fromCharCode(0xFFFD);
const META = /【|】|\[硬性|\[注意|\[软性|^>|^#|^(翻译|译文|注意|说明|提示)[:：]|只输出|源文】|Do not translate|Ne pas traduire|翻訳しない|traduci|no traduzca|请勿翻译/i;
const LATIN_WORD = /[A-Za-z]{4,}/;
const BRANDS = /(FIRS|CIRS|OpenTTD|FRAX|GitHub|Issue|pull request|GPL|NewGRF|TOML|makefile|fork|git|GRFID|Python|Gung-ho|Windows|macOS|Linux|Unix|Xcode|NML|JSON|ports tree|OpenGFX|Total Town Replacement( Set)?|STSW|CB|ID)/i;
const CYRILLIC = /[Ѐ-ӿ]/;
const KANA = /[぀-ヿ]/;
const BENGALI = /[ঀ-৿]/;
const CTRL = new RegExp('[' + String.fromCharCode(0) + '-' + String.fromCharCode(8) + String.fromCharCode(11) + String.fromCharCode(12) + String.fromCharCode(14) + '-' + String.fromCharCode(31) + ']');
const phList = s => (String(s).match(PH_RE) || []).sort().join(',');
function loadOut(lang) {
  const f = path.join(OUT, lang + '.jsonl'); const m = new Map();
  if (!fs.existsSync(f)) return m;
  for (const line of fs.readFileSync(f, 'utf-8').split('\n')) {
    if (!line.trim()) continue;
    try { const o = JSON.parse(line); if (Number.isInteger(o.i) && typeof o.tr === 'string') m.set(o.i, o.tr); } catch (e) {}
  }
  return m;
}
function auditLang(lang) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8'));
  const m = loadOut(lang); const c = {};
  const add = k => { c[k] = (c[k] || 0) + 1; };
  for (let i = 0; i < w.count; i++) {
    const en = w.entries[i].en; const tr = m.get(i);
    if (tr === undefined) { add('missing'); continue; }
    if (!tr.trim()) add('empty');
    if (phList(en) !== phList(tr)) add('ph_mismatch');
    if (tr.includes(REPLACEMENT)) add('replacement_char');
    if (CTRL.test(tr)) add('control_char');
    if (META.test(tr)) add('meta_leak');
    const bodies = [...tr.matchAll(PH_RE)].map(x => x[1]);
    if (bodies.some(b => /[^\x00-\x7F]/.test(b))) add('placeholder_translated');
    if (lang === 'japanese' && CYRILLIC.test(tr)) add('wrong_script');
    if (lang === 'korean' && (KANA.test(tr) || CYRILLIC.test(tr))) add('wrong_script');
    if (lang === 'tamil' && BENGALI.test(tr)) add('wrong_script');
    const latinText = tr.replace(PH_RE, ' ');
    // Serbian uses Latin script in this project.
    if (['arabic','russian','belarusian','tamil'].includes(lang) && LATIN_WORD.test(latinText) && !BRANDS.test(latinText)) add('latin_residue');
    if (tr === en && en.trim().split(/\s+/).length >= 4) add('identity');
    if (['japanese','korean','tamil','arabic','russian','belarusian','traditional_chinese','simplified_chinese'].includes(lang) &&
        en.trim().split(/\s+/).length >= 5 && !/[^\x00-\x7F]/.test(tr)) add('no_script');
    add('checked');
  }
  return { lang: lang, total: w.count, have: m.size, counts: c };
}
const args = process.argv.slice(2);
const langs = args.length ? args : fs.readdirSync(WORK).filter(f => f.endsWith('.json') && !f.startsWith('_')).map(f => f.slice(0, -5)).sort();
let grand = {};
for (const l of langs) {
  const a = auditLang(l);
  const flags = Object.entries(a.counts).filter(([k]) => k !== 'checked').map(([k,v]) => k + '=' + v).join(' ');
  console.log(a.lang.padEnd(24) + String(a.have).padStart(5) + '/' + a.total + '  ' + (flags || 'OK'));
  for (const [k,v] of Object.entries(a.counts)) grand[k] = (grand[k] || 0) + v;
}
console.log('GRAND: ' + JSON.stringify(grand));
