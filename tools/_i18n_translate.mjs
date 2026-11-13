#!/usr/bin/env node
/* CIRS i18n completion driver -- Bilibili Index-Translate free public API.
 * Usage: node tools/_i18n_translate.mjs [lang ...]   (default: all 38)
 *        node tools/_i18n_translate.mjs stats
 * Phase 1: batch translate via JSON instTrans prompt; only placeholder-safe results are kept.
 * Phase 2: QA/polish (meta-leak, wrong script, identity) + single-string recovery for gaps.
 */
import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const WORK = path.join(ROOT, "tools", "_i18n_work");
const OUT = path.join(ROOT, "tools", "_i18n_out");
const URL = "https://index-translate.bilibili.com/v1/chat/completions";
const MODEL = "Index-Translate-9B";
const BATCH = 12;
const CONC = 8;
const TIMEOUT = 60000;
const RETRIES = 4;
const PH = /\{([A-Za-z_0-9]*)\}/g;

const HARD = "【硬性要求】所有花括号占位符（例如 {STRING}、{BLACK}、{WHITE}、{TINYFONT}、{ORANGE}、{}）必须逐字原样保留，不得翻译、增删、改写或调整顺序。";
const SOFT = "【注意】这是 OpenTTD 游戏模组（NewGRF）与文档的界面文本；译文需地道、简洁，保留专有名词 FIRS、CIRS、OpenTTD、FRAX 不译；单字符标点或纯代码字符串保持原样。";

const NAMES = {
  afrikaans: "南非荷兰语", arabic: "阿拉伯语", belarusian: "白俄罗斯语", catalan: "加泰罗尼亚语",
  croatian: "克罗地亚语", czech: "捷克语", danish: "丹麦语", dutch: "荷兰语", esperanto: "世界语",
  estonian: "爱沙尼亚语", finnish: "芬兰语", french: "法语", gaelic: "苏格兰盖尔语", galician: "加利西亚语",
  german: "德语", hungarian: "匈牙利语", indonesian: "印度尼西亚语", italian: "意大利语", japanese: "日语",
  korean: "韩语", latin: "拉丁语", luxembourgish: "卢森堡语", norwegian_bokmal: "书面挪威语", polish: "波兰语",
  portuguese: "葡萄牙语", portuguese_BR: "巴西葡萄牙语", romanian: "罗马尼亚语", russian: "俄语",
  serbian: "塞尔维亚语（拉丁字母）", simplified_chinese: "简体中文", slovak: "斯洛伐克语", spanish: "西班牙语",
  spanish_MX: "墨西哥西班牙语", swedish: "瑞典语", tamil: "泰米尔语", traditional_chinese: "繁体中文",
  turkish: "土耳其语", welsh: "威尔士语",
};

const sleep = ms => new Promise(r => setTimeout(r, ms));
const phList = s => (String(s).match(PH) || []).sort().join(",");

function batchPrompt(obj, tgt) {
  return "请将以下英语文本翻译成" + tgt + "，并且严格遵循所有约束要求。\n\n【源文】\n" + JSON.stringify(obj) +
    "\n\n【约束要求】\n1. 【硬性要求】严格保留合法 JSON 语法格式，仅翻译 value 文本，key 保持不变；不要输出 JSON 之外的任何内容。\n2. " + HARD +
    "\n3. " + SOFT + "\n\n请以相同的 JSON 格式输出翻译结果，key 保持不变，value 为对应译文。只输出 JSON，不要有任何额外说明。";
}
function polishPrompt(enObj, trObj, langName) {
  return "你是" + langName + "翻译质量审校员。以下是英语源文 JSON 与对应的" + langName + "译文 JSON。请逐条检查并润色：\n" +
    "- 必须逐字保留所有花括号占位符（如 {BLACK}、{ORANGE}、{STRING}、{}），数量与顺序与源文完全一致；缺失的补回，多余的删除。\n" +
    "- 删除任何残留的指令、注释、解释、方括号提示、元文本或翻译腔；只保留地道译文。\n" +
    "- 保留 FIRS、CIRS、OpenTTD、FRAX 等专有名词不译。\n" +
    "- 译文简洁、符合游戏界面用语；单字符标点保持原样。\n" +
    "- 输出相同 key 的 JSON，value 为修正后的译文；只输出 JSON，不要有任何额外说明。\n\n" +
    "【源文】\n" + JSON.stringify(enObj) + "\n\n【待润色译文】\n" + JSON.stringify(trObj);
}
function singlePrompt(text, tgt) {
  return "请将以下英语文本翻译成" + tgt + "，并且严格遵循所有约束要求。\n\n【源文】\n" + text +
    "\n\n【约束要求】\n1. " + HARD + "\n2. " + SOFT + "\n\n只输出译文，不要有任何额外说明。";
}

async function call(prompt, maxTokens) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), TIMEOUT);
  try {
    const r = await fetch(URL, { method: "POST", signal: ctrl.signal,
      headers: { "Content-Type": "application/json", "User-Agent": "Index-Translate-Client/1.0" },
      body: JSON.stringify({ model: MODEL, messages: [{ role: "user", content: prompt }],
        temperature: 0.0, max_tokens: maxTokens || 8192, stream: false,
        chat_template_kwargs: { enable_thinking: false } }) });
    const txt = await r.text();
    if (!r.ok) throw new Error("HTTP " + r.status + " " + txt.slice(0, 80).replace(/\s+/g, " "));
    const j = JSON.parse(txt);
    return (j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || "";
  } finally { clearTimeout(t); }
}
function parseJSON(raw) {
  let s = raw.trim();
  try { return JSON.parse(s); } catch (e) {}
  const a = s.indexOf("{"), b = s.lastIndexOf("}");
  if (a >= 0 && b > a) return JSON.parse(s.slice(a, b + 1));
  throw new Error("no JSON object in response");
}

// Hard issues = must never be written (would break check_translations.py or corrupt file).
// Soft issues = quality problems fixed by the polish pass.
function issues(en, tr, lang) {
  const hard = [], soft = [];
  if (tr == null || tr === "") { hard.push("empty"); return { hard, soft }; }
  const s = String(tr);
  if (phList(en) !== phList(s)) hard.push("ph");
  if (/\uFFFD/.test(s)) hard.push("replacement");
  if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(s)) hard.push("ctrl");
  const bodies = [...s.matchAll(/\{([A-Za-z_0-9]*)\}/g)].map(m => m[1]);
  for (const b of bodies) if (/[^\x00-\x7F]/.test(b)) { hard.push("phtranslated"); break; }
  if (/【|】|\[硬性|\[注意|\[软性|^>|^#|^(翻译|译文|注意|说明|提示)[:：]|只输出|源文】|Do not translate|Ne pas traduire|翻訳しない|traduci|no traduzca|请勿翻译/i.test(s)) soft.push("meta");
  if (lang === "japanese" && /[Ѐ-ӿ]/.test(s)) soft.push("wrongscript");
  if (lang === "korean" && /[぀-ヿ]/.test(s)) soft.push("wrongscript");
  const latinText = s.replace(/\{[A-Za-z_0-9]*\}/g, " ");
  // Serbian in this project uses Latin script (FIRS 4.x corpus), so it is NOT flagged here.
  if ((lang === "arabic" || lang === "russian" || lang === "belarusian" || lang === "tamil") &&
      /[A-Za-z]{4,}/.test(latinText) && !/(FIRS|CIRS|OpenTTD|FRAX|GitHub|Issue|pull request|GPL|NewGRF|TOML|makefile|fork|git|GRFID|Python|Gung-ho|Windows|macOS|Linux|Unix|Xcode|NML|JSON|ports tree|OpenGFX|CB|ID)/i.test(latinText)) soft.push("latin");
  if (s === en && en.trim().split(/\s+/).length >= 4) soft.push("identity");
  return { hard, soft };
}

function loadOut(lang) {
  const f = path.join(OUT, lang + ".jsonl");
  const map = new Map();
  if (fs.existsSync(f)) {
    for (const line of fs.readFileSync(f, "utf-8").split("\n")) {
      if (!line.trim()) continue;
      try { const o = JSON.parse(line); if (Number.isInteger(o.i) && typeof o.tr === "string") map.set(o.i, o.tr); } catch (e) {}
    }
  }
  return map;
}
function appendOut(lang, pairs) {
  const f = path.join(OUT, lang + ".jsonl");
  const text = pairs.map(p => JSON.stringify({ i: p[0], tr: p[1] }) + "\n").join("");
  fs.appendFileSync(f, text, "utf-8");
}

async function translateLang(lang) {
  const work = JSON.parse(fs.readFileSync(path.join(WORK, lang + ".json"), "utf-8"));
  const tgt = NAMES[lang] || lang;
  const entries = work.entries;
  const out = loadOut(lang);
  const todo = [];
  for (let i = 0; i < entries.length; i++) if (!out.has(i)) todo.push(i);

  if (todo.length) {
    const batches = [];
    for (let s = 0; s < todo.length; s += BATCH) batches.push(todo.slice(s, s + BATCH));
    let done = 0, failed = 0;
    const t0 = Date.now();
    for (let s = 0; s < batches.length; s += CONC) {
      const wave = batches.slice(s, s + CONC);
      const res = await Promise.all(wave.map(async idxs => {
        const obj = {}; idxs.forEach(i => obj[String(i)] = entries[i].en);
        for (let a = 0; a < RETRIES; a++) {
          try {
            const j = parseJSON(await call(batchPrompt(obj, tgt), 8192));
            const got = [];
            for (const i of idxs) {
              const k = String(i);
              if (Object.prototype.hasOwnProperty.call(j, k) && typeof j[k] === "string") {
                if (!issues(entries[i].en, j[k], lang).hard.length) got.push([i, j[k]]);
              }
            }
            return got;
          } catch (e) { if (a === RETRIES - 1) return null; await sleep(700 * (a + 1)); }
        }
        return null;
      }));
      for (const got of res) {
        if (got === null) { failed += 1; continue; }
        if (got.length) { appendOut(lang, got); done += got.length; }
      }
      process.stdout.write("  [" + lang + "] phase1 " + Math.min(s + CONC, batches.length) + "/" + batches.length + " waves, +" + done + ", failed=" + failed + "\n");
    }
    console.log("[" + lang + "] phase1: +" + done + " kept, " + failed + " failed waves, " + ((Date.now() - t0) / 1000).toFixed(1) + "s");
  } else console.log("[" + lang + "] phase1: 0 pending");

  // Recovery for missing/hard-rejected entries, one string per request.
  let map = loadOut(lang);
  const miss = [];
  for (let i = 0; i < entries.length; i++) if (!map.has(i)) miss.push(i);
  if (miss.length) {
    let got = 0;
    for (let s = 0; s < miss.length; s += CONC) {
      const res = await Promise.all(miss.slice(s, s + CONC).map(async i => {
        for (let a = 0; a < RETRIES; a++) {
          try {
            const tr = (await call(singlePrompt(entries[i].en, tgt), 1024)).trim();
            if (tr && !issues(entries[i].en, tr, lang).hard.length) return [i, tr];
          } catch (e) { await sleep(600 * (a + 1)); }
        }
        return null;
      }));
      const pairs = res.filter(Boolean);
      if (pairs.length) { appendOut(lang, pairs); got += pairs.length; }
    }
    console.log("[" + lang + "] recovery: " + miss.length + " pending, " + got + " recovered");
  }

  // QA + polish for soft issues.
  map = loadOut(lang);
  const flagged = [], qa = {};
  for (let i = 0; i < entries.length; i++) {
    const tr = map.get(i);
    if (tr === undefined) continue;
    const soft = issues(entries[i].en, tr, lang).soft;
    if (soft.length) { flagged.push(i); for (const x of soft) qa[x] = (qa[x] || 0) + 1; }
  }
  console.log("[" + lang + "] QA: have=" + map.size + "/" + entries.length + " flagged_soft=" + flagged.length + " " + JSON.stringify(qa));
  if (flagged.length) {
    let fixed = 0;
    for (let s = 0; s < flagged.length; s += BATCH) {
      const idxs = flagged.slice(s, s + BATCH);
      const enObj = {}, trObj = {};
      idxs.forEach(i => { enObj[String(i)] = entries[i].en; trObj[String(i)] = map.get(i); });
      for (let a = 0; a < RETRIES; a++) {
        try {
          const j = parseJSON(await call(polishPrompt(enObj, trObj, tgt), 8192));
          const pairs = [];
          for (const i of idxs) {
            const k = String(i);
            if (Object.prototype.hasOwnProperty.call(j, k) && typeof j[k] === "string" && j[k].trim()) {
              const iss = issues(entries[i].en, j[k], lang);
              const orig = issues(entries[i].en, map.get(i), lang);
              if (!iss.hard.length && iss.soft.length < orig.soft.length) pairs.push([i, j[k]]);
            }
          }
          if (pairs.length) { appendOut(lang, pairs); fixed += pairs.length; }
          break;
        } catch (e) { if (a === RETRIES - 1) console.log("  [" + lang + "] polish wave " + s + " failed"); await sleep(700 * (a + 1)); }
      }
      await sleep(60);
    }
    console.log("[" + lang + "] polish: " + flagged.length + " flagged, " + fixed + " improved");
  }
  map = loadOut(lang);
  console.log("[" + lang + "] FINAL " + map.size + "/" + entries.length);
}

async function stats() {
  const langs = fs.readdirSync(WORK).filter(f => f.endsWith(".json") && !f.startsWith("_")).map(f => f.slice(0, -5)).sort();
  let tot = 0, have = 0;
  for (const l of langs) {
    const w = JSON.parse(fs.readFileSync(path.join(WORK, l + ".json"), "utf-8"));
    const m = loadOut(l);
    const n = Math.min(m.size, w.count);
    tot += w.count; have += n;
    console.log("  " + l.padEnd(24) + String(n).padStart(5) + "/" + w.count);
  }
  console.log("TOTAL " + have + "/" + tot);
}

const args = process.argv.slice(2);
if (args[0] === "stats") { await stats(); process.exit(0); }
fs.mkdirSync(OUT, { recursive: true });
const langs = args.length ? args : fs.readdirSync(WORK).filter(f => f.endsWith(".json") && !f.startsWith("_")).map(f => f.slice(0, -5)).sort();
console.log("Driver start: " + langs.length + " languages, MODEL=" + MODEL + ", BATCH=" + BATCH + ", CONC=" + CONC);
for (const l of langs) {
  try { await translateLang(l); }
  catch (e) { console.log("[" + l + "] FATAL " + String(e.stack || e).slice(0, 500)); }
}
console.log("Driver done.");
