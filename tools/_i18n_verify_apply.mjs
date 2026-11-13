#!/usr/bin/env node
/* Read-only pre-apply verification: for each (file,key) ref in a work list, confirm the
 * target TOML currently holds the exact English value, so _i18n_pipeline.py apply will patch it. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd();
const WORK = path.join(ROOT, 'tools', '_i18n_work');
const SECTION = /^\s*\[([^\]]+)\]\s*(?:#.*)?$/;
const ASSIGN = /^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$/;
function unescape(s) {
  const mp = { n: '\n', t: '\t', r: '\r', '\\': '\\', '"': '"', b: '\b', f: '\f' };
  let out = '';
  for (let i = 0; i < s.length; i++) {
    if (s[i] === '\\' && i + 1 < s.length && mp[s[i+1]] !== undefined) { out += mp[s[i+1]]; i++; } else out += s[i];
  }
  return out;
}
function values(file) {
  const lines = fs.readFileSync(file, 'utf-8').split('\n');
  const m = new Map(); let section = '';
  for (const line of lines) {
    const ms = SECTION.exec(line); if (ms) { section = ms[1]; continue; }
    const a = ASSIGN.exec(line); if (!a) continue;
    const key = section ? section + '.' + a[2] : a[2];
    m.set(key, unescape(a[4].slice(1, -1)));
  }
  return m;
}
const args = process.argv.slice(2);
const langs = args.length ? args : fs.readdirSync(WORK).filter(f => f.endsWith('.json') && !f.startsWith('_')).map(f => f.slice(0, -5)).sort();
let grand = { refs: 0, ok: 0, mismatch: 0, absent: 0 };
for (const l of langs) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, l + '.json'), 'utf-8'));
  const cache = new Map();
  let refs = 0, ok = 0, mismatch = 0, absent = 0; const examples = [];
  for (const e of w.entries) {
    for (const [file, key] of e.refs) {
      refs++;
      if (!cache.has(file)) cache.set(file, values(path.join(ROOT, file)));
      const v = cache.get(file).get(key);
      if (v === undefined) { absent++; if (examples.length < 3) examples.push('ABSENT ' + file + ' ' + key); }
      else if (v !== e.en) { mismatch++; if (examples.length < 3) examples.push('DIFF ' + file + ' ' + key + ' | en=' + JSON.stringify(e.en).slice(0,60) + ' cur=' + JSON.stringify(v).slice(0,60)); }
      else ok++;
    }
  }
  grand.refs += refs; grand.ok += ok; grand.mismatch += mismatch; grand.absent += absent;
  console.log(l.padEnd(24) + 'refs=' + String(refs).padStart(5) + ' ok=' + String(ok).padStart(5) + ' mismatch=' + mismatch + ' absent=' + absent + (mismatch + absent ? '  e.g. ' + examples.join(' ; ') : ''));
}
console.log('GRAND ' + JSON.stringify(grand));
