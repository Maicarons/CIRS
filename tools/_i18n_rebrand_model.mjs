#!/usr/bin/env node
/* Rebrand polish: retranslate stale sentences that still describe the OLD FIRS product.
 * Uses the free bilibili Index-Translate API. Validates placeholder parity + brand fidelity. */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.cwd();
const URL = 'https://index-translate.bilibili.com/v1/chat/completions';
const MODEL = 'Index-Translate-9B', BATCH = 10, CONC = 8, TIMEOUT = 60000, RETRIES = 4;
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
  romanian:'罗马尼亚语（Română）', russian:'俄语（Русский）', serbian:'塞尔维亚语（Srpski，请使用拉丁字母）',
  simplified_chinese:'简体中文', slovak:'斯洛伐克语（Slovenčina）', spanish:'西班牙语（Español）',
  spanish_MX:'墨西哥西班牙语（Español de México）', swedish:'瑞典语（Svenska）',
  tamil:'泰米尔语（தமிழ்）', traditional_chinese:'繁体中文', turkish:'土耳其语（Türkçe）', welsh:'威尔士语（Cymraeg）',
};
const sleep = ms => new Promise(r => setTimeout(r, ms));
const phList = s => (String(s).match(PH_RE) || []).sort().join(',');
function hardIssues(en, tr) {
  const h = [];
  if (tr == null || typeof tr !== 'string' || !tr.trim()) { h.push('empty'); return h; }
  if (phList(en) !== phList(tr)) h.push('ph');
  if (/\uFFFD/.test(tr)) h.push('replacement');
  if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(tr)) h.push('ctrl');
  for (const m of tr.matchAll(PH_RE)) if (/[^\x00-\x7F]/.test(m[1])) { h.push('phtranslated'); break; }
  return h;
}
function brandIssues(x, tr) {
  const b = [];
  const ef = (x.en.match(/FIRS/g) || []).length, tf = (tr.match(/FIRS/g) || []).length;
  const ec = (x.en.match(/CIRS/g) || []).length, tc = (tr.match(/CIRS/g) || []).length;
  if (tf > ef) b.push('stray_firs');
  if (tc < ec) b.push('missing_cirs');
  if (/【|】|只输出|^>|^#|^(译文|翻译|注意|说明)[:：]/m.test(tr)) b.push('meta');
  return b;
}
function makePrompt(items, tgt) {
  const obj = {};
  for (const [i, x] of items.entries()) obj[String(i)] = { en:x.en, cur:x.tr };
  const notes = items.map((x,i) => String(i) + ': ' + (x.note || '') + (x.name_hint ? '（该语言的模组名已定为：' + x.name_hint + '）' : '')).filter(s => !/^\d+: *（/.test(s) || s.length > 8).join('\n');
  return '你是' + tgt + '本地化审校员。下面 JSON 的 key 是编号，value.en 是【英语原文】，value.cur 是【当前译文】。当前译文是旧版 FIRS 模组的遗留文案，与新的英语原文不符（品牌名、句子内容已更新为 CIRS 社区分支）。请依据英语原文重新给出地道、准确的' + tgt + '译文。\n' +
    '【硬性要求】所有花括号占位符（{TINYFONT}、{BLACK}、{SILVER}、{ORANGE}、{YELLOW}、{WHITE}、{SIGNED_WORD}、{count}、{STRING}、{P 0 "" s}、{}）必须逐字原样保留，不得增删或改写；CIRS、FIRS、OpenTTD、FRAX、GPL、NewGRF、git、readme 等专有名词保持原样不译；塞尔维亚语一律使用拉丁字母；不要输出 JSON 之外的任何内容。\n' +
    (notes ? '【逐条要点】\n' + notes + '\n' : '') +
    '\n【待修订】\n' + JSON.stringify(obj) + '\n\n请以相同 key（编号）输出 JSON，value 为修订后的译文字符串。只输出 JSON。';
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
  let s = raw.trim(); s = s.replace(/^<think>[\s\S]*?<\/think>/,'').trim();
  const tryIt = t => { try { const j = JSON.parse(t); for (const k of Object.keys(j)) if (typeof j[k] === 'string') j[k] = j[k].replace(/^[\r\n]+|[\r\n]+$/g,''); return j; } catch(e) { return null; } };
  let j = tryIt(s); if (j) return j;
  const a = s.indexOf('{'), b = s.lastIndexOf('}');
  if (a >= 0 && b > a) { j = tryIt(s.slice(a,b+1)); if (j) return j; }
  throw new Error('no JSON');
}
async function wave(items, tgt) {
  for (let a = 0; a < RETRIES; a++) {
    try {
      const j = parseJSON(await call(makePrompt(items, tgt), 8192));
      const out = [];
      for (const [i, x] of items.entries()) {
        const v = j[String(i)];
        if (typeof v !== 'string') continue;
        const h = hardIssues(x.en, v), b = brandIssues(x, v);
        if (!h.length && !b.length && v !== x.tr) out.push({ ...x, tr:v });
      }
      return out;
    } catch (e) { if (a === RETRIES-1) console.log('  waveFail', String(e).slice(0,90)); }
    await sleep(700*(a+1));
  }
  return [];
}
async function main() {
  const T = JSON.parse(fs.readFileSync('tools/_i18n_rebrand_model_tasks.json','utf8'));
  const byLang = {};
  for (const x of T.retranslate) (byLang[x.lang] = byLang[x.lang] || []).push(x);
  const results = [];
  const langs = Object.keys(byLang).sort();
  for (let li = 0; li < langs.length; li += CONC) {
    const group = langs.slice(li, li+CONC);
    const jobs = [];
    for (const l of group) {
      const arr = byLang[l];
      for (let s = 0; s < arr.length; s += BATCH) jobs.push({ l, items:arr.slice(s,s+BATCH) });
    }
    const got = await Promise.all(jobs.map(async j => ({ l:j.l, out:await wave(j.items, NAMES[j.l] || j.l) })));
    for (const g of got) { results.push(...g.out); console.log('  ' + g.l.padEnd(20) + ' +' + g.out.length + '/' + (byLang[g.l]||[]).length); }
  }
  fs.writeFileSync('tools/_i18n_rebrand_model_out.json', JSON.stringify(results, null, 1), 'utf8');
  console.log('REBRAND MODEL changed=' + results.length + ' of ' + T.retranslate.length);
}
main().catch(e => { console.error('FATAL', e); process.exit(1); });
