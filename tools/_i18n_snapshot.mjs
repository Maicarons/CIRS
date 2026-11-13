#!/usr/bin/env node
/* Snapshot / diff last-wins maps of tools/_i18n_out/*.jsonl.
 * Usage: node tools/_i18n_snapshot.mjs snapshot <file>
 *        node tools/_i18n_snapshot.mjs diff <file>
 */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd(), WORK = path.join(ROOT, 'tools', '_i18n_work'), OUT = path.join(ROOT, 'tools', '_i18n_out');
function maps() {
  const out = {};
  for (const f of fs.readdirSync(OUT).filter(f => f.endsWith('.jsonl')).sort()) {
    const lang = f.slice(0, -6), m = {};
    for (const l of fs.readFileSync(path.join(OUT, f), 'utf-8').split('\n')) {
      if (!l.trim()) continue; try { const o = JSON.parse(l); if (Number.isInteger(o.i) && typeof o.tr === 'string') m[o.i] = o.tr; } catch (e) {}
    }
    out[lang] = m;
  }
  return out;
}
const [cmd, file] = process.argv.slice(2);
if (cmd === 'snapshot') { fs.writeFileSync(file, JSON.stringify(maps()), 'utf-8'); console.log('snapshot -> ' + file); }
else if (cmd === 'diff') {
  const before = JSON.parse(fs.readFileSync(file, 'utf-8')), after = maps();
  let n = 0;
  for (const lang of Object.keys(after).sort()) {
    const b = before[lang] || {}, a = after[lang] || {};
    const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8'));
    for (const k of Object.keys(a)) {
      if (b[k] === undefined) { console.log('NEW   ' + lang + ' ' + k + ' | EN=' + (w.entries[+k]||{}).en + ' | TR=' + a[k]); n++; continue; }
      if (b[k] !== a[k]) { console.log('CHG   ' + lang + ' ' + k + ' | EN=' + (w.entries[+k]||{}).en + ' | OLD=' + b[k] + ' | NEW=' + a[k]); n++; }
    }
  }
  console.log('DIFF changes=' + n);
} else console.log('usage: snapshot|diff <file>');
