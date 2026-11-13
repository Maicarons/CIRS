import fs from 'node:fs';
const URL='https://index-translate.bilibili.com/v1/chat/completions', MODEL='Index-Translate-9B';
const obj={301:'Bitumen',302:'Cassava',303:'Barytes & Fluorspar',304:'Nitrogen',305:'Peat',306:'Slag',307:'Billets & Blooms',308:'Tin',309:'Barns',310:'Colliery',311:'Estate',312:'Silo'};
const tgt='威尔士语（Cymraeg）';
const prompt='你是'+tgt+'本地化审校员。下面 JSON 的 key 是条目号，value 是翻译文件中仍与英文原文完全相同的游戏/网站短文本。\n' +
  '请逐条给出地道、准确的'+tgt+'译文；只有当该词在'+tgt+'中本来就同形（国际通用借词、专有名词、品牌、货物两字母代码、缩写代号）时，才保持原样。\n' +
  '【硬性要求】所有花括号内容必须逐字原样保留；FIRS、CIRS、OpenTTD、FRAX 等专有名词不译；不要输出 JSON 之外的任何内容。\n\n' +
  '【待审校】\n'+JSON.stringify(obj)+'\n\n请以相同 key 输出 JSON，value 为确认或修正后的译文。只输出 JSON。';
for (const model of [MODEL]) {
  const r=await fetch(URL,{method:'POST',headers:{'Content-Type':'application/json','User-Agent':'Index-Translate-Client/1.0'},body:JSON.stringify({model,messages:[{role:'user',content:prompt}],temperature:0,max_tokens:8192,stream:false,chat_template_kwargs:{enable_thinking:false}})});
  const s=await r.text();console.log('status',r.status);
  try{const j=JSON.parse(s);const c=(j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
    console.log('RAW:',JSON.stringify(c.slice(0,1500)));
    let t=c.trim();try{const p=JSON.parse(t);console.log('PARSED keys',Object.keys(p).length);for(const [k,v] of Object.entries(p))console.log(' ',k,JSON.stringify(v));}catch(e){console.log('JSON parse failed:',e.message.slice(0,120));}
  }catch(e){console.log('resp parse failed',s.slice(0,300));}
}
