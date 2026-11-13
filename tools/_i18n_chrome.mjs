// Translate VitePress default-theme chrome labels for the 31 locales that
// currently have no themeConfig (and therefore no sidebar). Fallback = English.
const fs = await import('node:fs');
const API = 'https://index-translate.bilibili.com/v1/chat/completions';
const MODEL = 'Index-Translate-9B';

const EN = {
  guide: 'Guide',
  get_started: 'Get started',
  reference: 'Reference',
  on_this_page: 'On this page',
  prev: 'Previous',
  next: 'Next',
  appearance: 'Appearance',
  switch_light: 'Switch to light theme',
  switch_dark: 'Switch to dark theme',
  menu: 'Menu',
  return_to_top: 'Return to top',
  change_language: 'Change language'
};

// code -> (lang id, Chinese target name)
const LANGS = {
  af: ['afrikaans', '南非荷兰语'],
  be: ['belarusian', '白俄罗斯语'],
  ca: ['catalan', '加泰罗尼亚语'],
  cs: ['czech', '捷克语'],
  cy: ['welsh', '威尔士语'],
  da: ['danish', '丹麦语'],
  eo: ['esperanto', '世界语'],
  'es-mx': ['spanish_MX', '墨西哥西班牙语'],
  et: ['estonian', '爱沙尼亚语'],
  fi: ['finnish', '芬兰语'],
  gd: ['gaelic', '苏格兰盖尔语'],
  gl: ['galician', '加利西亚语'],
  hr: ['croatian', '克罗地亚语'],
  hu: ['hungarian', '匈牙利语'],
  id: ['indonesian', '印度尼西亚语'],
  it: ['italian', '意大利语'],
  ja: ['japanese', '日语'],
  la: ['latin', '拉丁语'],
  lb: ['luxembourgish', '卢森堡语'],
  nb: ['norwegian_bokmal', '书面挪威语'],
  nl: ['dutch', '荷兰语'],
  pl: ['polish', '波兰语'],
  'pt-br': ['portuguese_BR', '巴西葡萄牙语'],
  ro: ['romanian', '罗马尼亚语'],
  ru: ['russian', '俄语'],
  sk: ['slovak', '斯洛伐克语'],
  sr: ['serbian', '塞尔维亚语（请用拉丁字母）'],
  sv: ['swedish', '瑞典语'],
  ta: ['tamil', '泰米尔语'],
  tr: ['turkish', '土耳其语'],
  'zh-hant': ['traditional_chinese', '繁体中文']
};

function prompt(tgt, obj) {
  return '请将以下英语网站界面文案翻译成' + tgt + '，并且严格遵循所有约束要求。\n\n' +
    '【源文】\n' + JSON.stringify(obj) + '\n\n' +
    '【约束要求】\n' +
    '1. 【硬性要求】只翻译 JSON 的 value，key 必须保持不变，不得增删 key。\n' +
    '2. 【硬性要求】这些是网站导航栏、侧边栏、按钮上的短标签，请用简洁、地道、常见的说法，不要加标点、不要加任何说明。\n' +
    '3. 【注意】品牌名 CIRS、FIRS、OpenTTD、GitHub 保持原样。\n\n' +
    '请以相同的 JSON 格式输出翻译结果，key 保持不变，value 为对应译文。只输出 JSON，不要有任何额外说明。';
}

async function callAPI(tgt) {
  const body = {
    model: MODEL,
    messages: [{ role: 'user', content: prompt(tgt, EN) }],
    temperature: 0.0,
    max_tokens: 2048,
    stream: false,
    chat_template_kwargs: { enable_thinking: false }
  };
  const r = await fetch(API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'User-Agent': 'Index-Translate-Client/1.0' },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(60000)
  });
  if (!r.ok) throw new Error('HTTP ' + r.status + ' ' + (await r.text()).slice(0, 100));
  const j = await r.json();
  let c = (j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || '';
  c = c.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
  const s = c.indexOf('{'), e = c.lastIndexOf('}');
  if (s < 0 || e <= s) throw new Error('no JSON: ' + c.slice(0, 120));
  const o = JSON.parse(c.slice(s, e + 1));
  for (const k of Object.keys(EN)) {
    if (typeof o[k] !== 'string') throw new Error('missing key ' + k);
    o[k] = o[k].replace(/^[\r\n]+|[\r\n]+$/g, '').trim();
    if (!o[k]) throw new Error('empty ' + k);
    if (o[k].length > 200) throw new Error('too long ' + k);
    if (/[\uFFFD\u0000-\u001F]/u.test(o[k])) throw new Error('bad char ' + k);
    if (/【|源文|约束|译文[:：]|Here is|Note:/.test(o[k])) throw new Error('meta ' + k + ': ' + o[k].slice(0, 60));
  }
  return o;
}

async function one(code, id, tgt) {
  for (let a = 0; a < 4; a++) {
    try { return { code, val: await callAPI(tgt), ok: true, attempts: a + 1 }; }
    catch (e) { if (a === 3) return { code, val: EN, ok: false, err: String(e.message || e).slice(0, 120), attempts: 4 }; await new Promise(r => setTimeout(r, 700 + a * 400)); }
  }
}

const codes = Object.keys(LANGS);
const out = { english: EN };
const notes = [];
for (let i = 0; i < codes.length; i += 8) {
  const batch = codes.slice(i, i + 8);
  const rs = await Promise.all(batch.map(c => one(c, LANGS[c][0], LANGS[c][1])));
  for (const r of rs) {
    out[r.code] = r.val;
    notes.push(r.code + ' ' + (r.ok ? 'OK(' + r.attempts + ')' : 'FALLBACK ' + r.err) + ' guide=' + r.val.guide);
  }
}
fs.writeFileSync('tools/_i18n_chrome.json', JSON.stringify(out, null, 2), 'utf8');
console.log('WROTE tools/_i18n_chrome.json langs=' + (Object.keys(out).length - 1) + ' fallbacks=' + notes.filter(n => n.includes('FALLBACK')).length);
console.log(notes.join('\n'));
