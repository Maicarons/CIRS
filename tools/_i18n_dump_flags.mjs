#!/usr/bin/env node
/* Dump translations that independent QA flags, for manual judgement. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd(), WORK = path.join(ROOT, 'tools', '_i18n_work'), OUT = path.join(ROOT, 'tools', '_i18n_out');
const PH_RE = /\{([A-Za-z_0-9]*)\}/g;
const BRANDS = /(FIRS|CIRS|OpenTTD|FRAX|GitHub|Issue|pull request|GPL|NewGRF|TOML|makefile|fork|git|GRFID|Python|Gung-ho|Windows|macOS|Linux|Unix|Xcode|NML|JSON|ports tree|OpenGFX|Total Town Replacement Set|STSW|CB|ID)/i;
const NONLATIN = /[^\x00-\x7F]/;
function loadOut(lang) {
  const f = path.join(OUT, lang + '.jsonl'), m = new Map();
  if (fs.existsSync(f)) for (const l of fs.readFileSync(f, 'utf-8').split('\n')) {
    if (!l.trim()) continue;
    try { const o = JSON.parse(l); if (Number.isInteger(o.i) && typeof o.tr === 'string') m.set(o.i, o.tr); } catch (e) {}
  }
  return m;
}
for (const lang of process.argv.slice(2)) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8'));
  const m = loadOut(lang);
  console.log('===== ' + lang + ' =====');
  for (let i = 0; i < w.count; i++) {
    const en = w.entries[i].en, tr = m.get(i);
    if (tr === undefined) { console.log('MISSING ' + i + ' | EN=' + en); continue; }
    const latinText = tr.replace(PH_RE, ' ');
    const latin = ['arabic','russian','belarusian','serbian','tamil'].includes(lang) && /[A-Za-z]{4,}/.test(latinText) && !BRANDS.test(latinText);
    const noScript = ['japanese','korean','tamil','arabic','russian','belarusian','serbian','traditional_chinese','simplified_chinese'].includes(lang) && en.trim().split(/\s+/).length >= 5 && !NONLATIN.test(tr);
    const identity = tr === en && en.trim().split(/\s+/).length >= 4;
    if (latin || noScript || identity) {
      console.log((latin?'L':'') + (noScript?'N':'') + (identity?'I':'') + ' ' + i + ' | EN=' + en.slice(0,110) + ' | TR=' + tr.slice(0,140));
    }
  }
}
