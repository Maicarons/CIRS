import fs from 'node:fs';
const w = JSON.parse(fs.readFileSync('tools/_i18n_work/portuguese_BR.json','utf-8'));
const e = w.entries[604];
const tgt = '巴西葡萄牙语（Português do Brasil）';
const prompt = '请将下面这句英语游戏/网站文本翻译成' + tgt + '。\n' +
  '【硬性要求】所有花括号占位符（如 {TINYFONT}、{BLACK}、{count}、{STRING}、{}）必须逐字原样保留，不得增删或改写；保留 FIRS、CIRS、OpenTTD、FRAX 等专有名词不译。\n' +
  '只输出译文，不要任何解释或前后缀。\n\n【源文】\n' + e.en;
for (let k=0;k<3;k++){
  const r = await fetch('https://index-translate.bilibili.com/v1/chat/completions',{method:'POST',headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},body:JSON.stringify({model:'Index-Translate-9B',messages:[{role:'user',content:prompt}],temperature:0,max_tokens:1024,stream:false,chat_template_kwargs:{enable_thinking:false}})});
  const s = await r.text(); console.log('status',r.status);
  try { const j=JSON.parse(s); const c=(j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
    console.log('content',JSON.stringify(c));
    const phl = x => (String(x).match(/\{([A-Za-z_0-9]*)\}/g)||[]).sort().join(',');
    console.log('en_ph',phl(e.en),'tr_ph',phl(c),'match',phl(e.en)===phl(c));
  } catch(err){ console.log('parse err',s.slice(0,200)); }
}
