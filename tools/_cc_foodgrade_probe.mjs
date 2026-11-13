#!/usr/bin/env node
/* Probe the Bilibili Index-Translate API for the FRAX food-grade sense of
 * "Potable" / "Non-Potable" cargo classes, in every project language.
 * The FRAX spec defines CC_POTABLE as "edible / food-grade" cargo, NOT "drinkable".
 */
const URL = "https://index-translate.bilibili.com/v1/chat/completions";
const MODEL = "Index-Translate-9B";
const OUT = "tools/_cc_foodgrade_probe.json";

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

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function prompt(langName) {
  return [
    "这是 OpenTTD 游戏模组 CIRS 的 FRAX 货物类别标签，请翻译成" + langName + "。",
    "",
    "【语义说明】FRAX 标准里，Potable 这一类指【食品级】货物：可食用、适合人类食用、需要卫生运输条件的货物，",
    "例如牛奶、谷物、面粉、鱼、豆类、食品。它并不是指「可以喝的液体」。",
    "Non-Potable 则是指【非食品级】货物：不可食用、不适合人类食用，例如牲畜、煤炭、水泥、石油、化肥、化工品。",
    "",
    "【要求】请使用该语言中表示「食品级／食用级」这一概念的术语（而不是「可饮用／能喝」），",
    "翻译下面两个类别标签。输出 JSON，key 保持不变，只输出 JSON，不要任何解释。",
    "",
    '{"Potable":"Potable","Non-Potable":"Non-Potable"}',
  ].join("\n");
}

async function call(p) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 60000);
  try {
    const r = await fetch(URL, {
      method: "POST", signal: ctrl.signal,
      headers: { "Content-Type": "application/json", "User-Agent": "Index-Translate-Client/1.0" },
      body: JSON.stringify({
        model: MODEL, messages: [{ role: "user", content: p }],
        temperature: 0.0, max_tokens: 400, stream: false,
        chat_template_kwargs: { enable_thinking: false },
      }),
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const j = await r.json();
    return (j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || "";
  } finally { clearTimeout(t); }
}

function parse(raw) {
  let s = String(raw).trim();
  try { return JSON.parse(s); } catch (e) {}
  const a = s.indexOf("{"), b = s.lastIndexOf("}");
  if (a >= 0 && b > a) return JSON.parse(s.slice(a, b + 1));
  throw new Error("no JSON: " + s.slice(0, 120));
}

(async () => {
  const result = {};
  const langs = Object.keys(NAMES);
  for (let i = 0; i < langs.length; i += 4) {
    const batch = langs.slice(i, i + 4);
    const outs = await Promise.all(batch.map(async (l) => {
      for (let a = 0; a < 3; a++) {
        try {
          const raw = await call(prompt(NAMES[l]));
          const obj = parse(raw);
          if (obj && obj.Potable && obj["Non-Potable"]) {
            return [l, { Potable: String(obj.Potable), "Non-Potable": String(obj["Non-Potable"]) }];
          }
        } catch (e) { /* retry */ }
        await sleep(800);
      }
      return [l, { error: "failed" }];
    }));
    for (const [l, v] of outs) { result[l] = v; console.log(l, JSON.stringify(v)); }
    await sleep(400);
  }
  require("fs").writeFileSync(OUT, JSON.stringify(result, null, 1), "utf-8");
  console.log("wrote", OUT);
})();
