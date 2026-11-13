#!/usr/bin/env node
/* Classify post-apply identity (still-English) refs to find any that should have been translated. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd();
const WORK = path.join(ROOT, 'tools', '_i18n_work');
const SECTION = /^\s*\[([^\]]+)\]\s*(?:#.*)?$/;
const ASSIGN = /^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$/;
function unesc(s) {
  const mp = { n: '\n', t: '\t', r: '\r', '\\': '\\', '"': '"', b: '\b', f: '\f' };
  let o = '';
  for (let i = 0; i < s.length; i++) {
    if (s[i] === '\\' && i + 1 < s.length && mp[s[i+1]] !== undefined) { o += mp[s[i+1]]; i++; } else o += s[i];
  }
  return o;
}
function vals(f) {
  const m = new Map(); let sec = '';
  for (const l of fs.readFileSync(f, 'utf-8').split('\n')) {
    const s = SECTION.exec(l); if (s) { sec = s[1]; continue; }
    const a = ASSIGN.exec(l); if (!a) continue;
    m.set(sec ? sec + '.' + a[2] : a[2], unesc(a[4].slice(1, -1)));
  }
  return m;
}
const BRAND = /^(FIRS|CIRS|OpenTTD|FRAX|NewGRF|GRFID|Python|makefile|GitHub|Issue|pull request|GPL|TOML|fork|git|JSON|NML|Gung-ho|Xcode|Windows|macOS|Linux|Unix|OpenGFX|Total Town Replacement Set|STSW|E\d+|CABBAGE)/i;
const cats = { punct:0, brand:0, shortcode:0, number:0, word:0, sentence:0, other:0 };
let shown = 0;
for (const lang of ['french','afrikaans','arabic']) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8'));
  const cache = new Map();
  for (const e of w.entries) {
    for (const [f, k] of e.refs) {
      if (!cache.has(f)) cache.set(f, vals(path.join(ROOT, f)));
      const v = cache.get(f).get(k);
      if (v !== e.en) continue;
      const s = e.en.trim();
      let c = 'other';
      if (/^[\W_]+$/.test(s) || s.length <= 2) c = 'punct';
      else if (BRAND.test(s)) c = 'brand';
      else if (/^[A-Z0-9_\/-]{2,12}$/.test(s)) c = 'shortcode';
      else if (/^[\d.,%+\-]+$/.test(s)) c = 'number';
      else if (s.split(/\s+/).length >= 4) c = 'sentence';
      else if (/^[A-Za-z][A-Za-z .,'&()\/-]{1,30}$/.test(s)) c = 'word';
      cats[c]++;
      if (shown < 30) { console.log(lang + ' [' + c + '] ' + k + ' = ' + JSON.stringify(e.en).slice(0, 110)); shown++; }
    }
  }
}
console.log('CATEGORIES ' + JSON.stringify(cats));
