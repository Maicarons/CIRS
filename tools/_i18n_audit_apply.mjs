#!/usr/bin/env node
/* Post-apply audit: for every (file,key) ref in the work lists, read the PATCHED TOML and
 * confirm the value is no longer the English source, preserves placeholders, and is clean. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd();
const WORK = path.join(ROOT, 'tools', '_i18n_work');
const SECTION = /^\s*\[([^\]]+)\]\s*(?:#.*)?$/;
const ASSIGN = /^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$/;
const PH_RE = /\{([A-Za-z_0-9]*)\}/g;
const REPLACEMENT = String.fromCharCode(0xFFFD);
const phList = s => (String(s).match(PH_RE) || []).sort().join(',');
function unescape(s) {
  const mp = { n: '\n', t: '\t', r: '\r', '\\': '\\', '"': '"', b: '\b', f: '\f' };
  let out = '';
  for (let i = 0; i < s.length; i++) {
    if (s[i] === '\\' && i + 1 < s.length && mp[s[i+1]] !== undefined) { out += mp[s[i+1]]; i++; } else out += s[i];
  }
  return out;
}
function values(file) {
  const m = new Map(); let section = '';
  for (const line of fs.readFileSync(file, 'utf-8').split('\n')) {
    const ms = SECTION.exec(line); if (ms) { section = ms[1]; continue; }
    const a = ASSIGN.exec(line); if (!a) continue;
    m.set(section ? section + '.' + a[2] : a[2], unescape(a[4].slice(1, -1)));
  }
  return m;
}
const langs = process.argv.slice(2).length ? process.argv.slice(2)
  : fs.readdirSync(WORK).filter(f => f.endsWith('.json') && !f.startsWith('_')).map(f => f.slice(0, -5)).sort();
const grand = {}; const inc = k => { grand[k] = (grand[k] || 0) + 1; };
for (const l of langs) {
  const w = JSON.parse(fs.readFileSync(path.join(WORK, l + '.json'), 'utf-8'));
  const cache = new Map(); const c = {}; const bump = k => { c[k] = (c[k] || 0) + 1; inc(k); };
  for (const e of w.entries) {
    for (const [file, key] of e.refs) {
      if (!cache.has(file)) cache.set(file, values(path.join(ROOT, file)));
      const v = cache.get(file).get(key);
      if (v === undefined) { bump('absent'); continue; }
      if (v === e.en) { bump('untranslated'); continue; }
      if (phList(v) !== phList(e.en)) bump('ph_mismatch');
      if (v.includes(REPLACEMENT)) bump('replacement_char');
      if (!v.trim()) bump('empty');
      bump('ok');
    }
  }
  const flags = Object.entries(c).filter(([k]) => k !== 'ok').map(([k,v]) => k + '=' + v).join(' ');
  console.log(l.padEnd(24) + 'ok=' + String(c.ok || 0).padStart(5) + '  ' + (flags || 'ALL TRANSLATED'));
}
console.log('GRAND ' + JSON.stringify(grand));
