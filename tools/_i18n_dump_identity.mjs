#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd(), WORK = path.join(ROOT, 'tools', '_i18n_work'), OUT = path.join(ROOT, 'tools', '_i18n_out');
for (const lang of process.argv.slice(2)) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, lang + '.json'), 'utf-8'));
  const m = new Map();
  for (const l of fs.readFileSync(path.join(OUT, lang + '.jsonl'), 'utf-8').split('\n')) {
    if (!l.trim()) continue; const o = JSON.parse(l); m.set(o.i, o.tr);
  }
  const ids = [];
  for (let i = 0; i < w.entries.length; i++) if (m.get(i) === w.entries[i].en) ids.push(w.entries[i].en);
  console.log('=== ' + lang + ' identity ' + ids.length + '/' + w.count + ' ===');
  console.log(JSON.stringify(ids, null, 0).slice(0, 4000));
}
