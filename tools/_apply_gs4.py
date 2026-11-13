"""GS (GameScript) translations - Batch 4: japanese, simplified_chinese, traditional_chinese, afrikaans, esperanto.
Value-keyed. Placeholder-only GS strings intentionally omitted."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _translate as T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GS_EN = os.path.join(ROOT, "src", "gs", "lang", "english.toml")

W = "Hello {COMPANY}!{}{}You are playing a game with CIRS test GS{}{}Git version of this GS is {NUM}"
C = "{BLUE}Cabbage"
HAPPY = "happy"
UNHAPPY = "unhappy"
TOWN = "Town is {STRING}{}{}To find out more about this town (including growth and happiness requirements), open the Story Book, and find the page for {TOWN}"
GRIND = "{BLACK}Note that this won't refresh currently unless Grind is turned off and on in GS settings"
RND = "{BLACK}Random word (test): {WHITE}{RAW_STRING}"
GROWTH = "{BLACK}Current growth rate: {WHITE}{RAW_STRING}"
RQG = "{YELLOW}Required cargos for growth"
RQH = "{YELLOW}Required cargos for happiness"
SUP = "{BLACK}Supplied: {WHITE}{CARGO_LONG}"
TI = "{BLACK}--- Town industries --- {}"
ACCEPT = "{BLACK}Required cargo supplied last month"
PROD = "{BLACK}Cargo produced last month"
HIST = "{BLACK}Production (permanent) increase history (last 10 events)"
NEVER = "{WHITE}- this industry has never permanently increased production"
PRODLVL = "{BLACK}Current production level: {WHITE}{NUM}"
NAME = "{BLACK}Name: {WHITE}{RAW_STRING}"
TYPE = "{BLACK}Type: {WHITE}{RAW_STRING}"
HQ = "{BLACK}HQ town: {WHITE}{TOWN}"
VALID = "{BLACK}Valid towns: {WHITE}{RAW_STRING}"
OWNED = "{BLACK}Industries owned: {WHITE}{RAW_STRING}"
CLICK = "{BLACK}This is a GS text. {WHITE}Click me for the town story page. {BLACK}Here is some more text."
OWNER = "Owner: {RAW_STRING}"
DELIV = "{BLACK}Deliveries to this industry will contribute to town growth and/or happiness"
INCR = "{INDUSTRY} increases production!"

GS_JA = {
    W: "こんにちは {COMPANY} さん！{}{}あなたは CIRS テスト GS を使用するゲームをプレイ中です{}{}この GS の Git バージョンは {NUM} です",
    C: "{BLUE}キャベツ", HAPPY: "幸せ", UNHAPPY: "不幸",
    TOWN: "街は {STRING}{}{}この街についてもっと知るには（成長と幸福の要件を含む）、ストーリーブックを開き、{TOWN} のページを見つけてください",
    GRIND: "{BLACK}現在、GS の設定で Grind をオフにして再度オンにしない限り、これは更新されません",
    RND: "{BLACK}ランダムな単語（テスト）: {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}現在の成長率: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}成長に必要な積荷",
    RQH: "{YELLOW}幸福に必要な積荷",
    SUP: "{BLACK}供給済み: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- 街の産業 --- {}",
    ACCEPT: "{BLACK}前月に供給された必要積荷",
    PROD: "{BLACK}前月に生産された積荷",
    HIST: "{BLACK}生産（永続的）増加の履歴（直近 10 件）",
    NEVER: "{WHITE}- この産業はこれまで生産を永続的に増加させたことがありません",
    PRODLVL: "{BLACK}現在の生産レベル: {WHITE}{NUM}",
    NAME: "{BLACK}名前: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}種類: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}本社所在地の街: {WHITE}{TOWN}",
    VALID: "{BLACK}有効な街: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}所有する産業: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}これは GS のテキストです。{WHITE}街のストーリーページを表示するには私をクリックしてください。{BLACK}続きのテキストがあります。",
    OWNER: "所有者: {RAW_STRING}",
    DELIV: "{BLACK}この産業への配送は、街の成長および／または幸福に寄与します",
    INCR: "{INDUSTRY} は生産を増加させます！",
}
GS_ZH = {
    W: "你好 {COMPANY}！{}{}你正在使用 CIRS 测试 GS 进行游戏{}{}此 GS 的 Git 版本为 {NUM}",
    C: "{BLUE}卷心菜", HAPPY: "幸福", UNHAPPY: "不幸福",
    TOWN: "城镇：{STRING}{}{}要了解该城镇的更多信息（包括增长与幸福度要求），请打开故事书，找到 {TOWN} 的页面",
    GRIND: "{BLACK}请注意，当前不会刷新，除非在 GS 设置中关闭并重新开启 Grind",
    RND: "{BLACK}随机单词（测试）：{WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}当前增长率：{WHITE}{RAW_STRING}",
    RQG: "{YELLOW}增长所需的货物",
    RQH: "{YELLOW}幸福所需的货物",
    SUP: "{BLACK}已供应：{WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- 城镇产业 --- {}",
    ACCEPT: "{BLACK}上月供应的所需货物",
    PROD: "{BLACK}上月生产的货物",
    HIST: "{BLACK}生产（永久）增长历史（最近 10 个事件）",
    NEVER: "{WHITE}- 该产业从未永久提高过产量",
    PRODLVL: "{BLACK}当前生产等级：{WHITE}{NUM}",
    NAME: "{BLACK}名称：{WHITE}{RAW_STRING}",
    TYPE: "{BLACK}类型：{WHITE}{RAW_STRING}",
    HQ: "{BLACK}总部所在城镇：{WHITE}{TOWN}",
    VALID: "{BLACK}有效城镇：{WHITE}{RAW_STRING}",
    OWNED: "{BLACK}拥有的产业：{WHITE}{RAW_STRING}",
    CLICK: "{BLACK}这是一段 GS 文本。{WHITE}点击我打开城镇故事页面。{BLACK}这里是更多文本。",
    OWNER: "所有者：{RAW_STRING}",
    DELIV: "{BLACK}向该产业交付货物将促进城镇的增长和／或幸福度",
    INCR: "{INDUSTRY} 提高了产量！",
}
GS_ZHT = {
    W: "你好 {COMPANY}！{}{}你正在使用 CIRS 測試 GS 進行遊戲{}{}此 GS 的 Git 版本為 {NUM}",
    C: "{BLUE}捲心菜", HAPPY: "幸福", UNHAPPY: "不幸福",
    TOWN: "城鎮：{STRING}{}{}要了解該城鎮的更多資訊（包括成長與幸福度要求），請開啟故事書，找到 {TOWN} 的頁面",
    GRIND: "{BLACK}請注意，目前不會重新整理，除非在 GS 設定中關閉並重新開啟 Grind",
    RND: "{BLACK}隨機單字（測試）：{WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}目前成長率：{WHITE}{RAW_STRING}",
    RQG: "{YELLOW}成長所需的貨物",
    RQH: "{YELLOW}幸福所需的貨物",
    SUP: "{BLACK}已供應：{WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- 城鎮產業 --- {}",
    ACCEPT: "{BLACK}上月供應的所需貨物",
    PROD: "{BLACK}上月生產的貨物",
    HIST: "{BLACK}生產（永久）成長歷史（最近 10 個事件）",
    NEVER: "{WHITE}- 該產業從未永久提高過產量",
    PRODLVL: "{BLACK}目前生產等級：{WHITE}{NUM}",
    NAME: "{BLACK}名稱：{WHITE}{RAW_STRING}",
    TYPE: "{BLACK}類型：{WHITE}{RAW_STRING}",
    HQ: "{BLACK}總部所在城鎮：{WHITE}{TOWN}",
    VALID: "{BLACK}有效城鎮：{WHITE}{RAW_STRING}",
    OWNED: "{BLACK}擁有的產業：{WHITE}{RAW_STRING}",
    CLICK: "{BLACK}這是一段 GS 文字。{WHITE}點擊我開啟城鎮故事頁面。{BLACK}這裡是更多文字。",
    OWNER: "擁有者：{RAW_STRING}",
    DELIV: "{BLACK}向該產業交付貨物將促進城鎮的成長和／或幸福度",
    INCR: "{INDUSTRY} 提高了產量！",
}
GS_AF = {
    W: "Hallo {COMPANY}!{}{}Jy speel 'n spel met die CIRS-toets-GS{}{}Git-weergawe van hierdie GS is {NUM}",
    C: "{BLUE}Kool", HAPPY: "gelukkig", UNHAPPY: "ongelukkig",
    TOWN: "Dorp is {STRING}{}{}Om meer oor hierdie dorp uit te vind (insluitend groei- en gelukkigheidsvereistes), maak die Storieboek oop en kry die bladsy vir {TOWN}",
    GRIND: "{BLACK}Let daarop dat dit tans nie sal verfris nie, tensy Grind af- en weer aangeskakel word in die GS-instellings",
    RND: "{BLACK}Lukrake woord (toets): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Huidige groeitempo: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Vereiste vragte vir groei",
    RQH: "{YELLOW}Vereiste vragte vir geluk",
    SUP: "{BLACK}Voorsien: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Dorpse nywerheid --- {}",
    ACCEPT: "{BLACK}Vereiste vrag gelewer verlede maand",
    PROD: "{BLACK}Vrag geproduseer verlede maand",
    HIST: "{BLACK}Geskiedenis van (permanente) produksieverhogings (laaste 10 gebeure)",
    NEVER: "{WHITE}- hierdie nywerheid het nog nooit permanent produksie verhoog nie",
    PRODLVL: "{BLACK}Huidige produksievlak: {WHITE}{NUM}",
    NAME: "{BLACK}Naam: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tipe: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Hoofkwartierdorp: {WHITE}{TOWN}",
    VALID: "{BLACK}Geldige dorpe: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Eienaarsnywerhede: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Hierdie is 'n GS-teks. {WHITE}Klik op my vir die dorp se storiebladsy. {BLACK}Hier is meer teks.",
    OWNER: "Eienaar: {RAW_STRING}",
    DELIV: "{BLACK}Aflewerings aan hierdie nywerheid sal bydra tot die dorp se groei en/of geluk",
    INCR: "{INDUSTRY} verhoog produksie!",
}
GS_EO = {
    W: "Saluton {COMPANY}!{}{}Vi ludas ludon kun la testa GS de CIRS{}{}La Git-versio de cxi tiu GS estas {NUM}",
    C: "{BLUE}Brassiko", HAPPY: "feliĉa", UNHAPPY: "malfeliĉa",
    TOWN: "La urbo estas {STRING}{}{}Por scii pli pri cxi tiu urbo (inkluzive kreskaj kaj feliĉaj postuloj), malfermu la Rakontolibron kaj trovu la paĝon por {TOWN}",
    GRIND: "{BLACK}Rimarku ke cxi tio ne gxisdatigos aktuale krom se Grind estos malsxaltita kaj resxaltita en la GS-agordoj",
    RND: "{BLACK}Hazarda vorto (testo): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Nuna kreskrapido: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Postulataj varoj por kresko",
    RQH: "{YELLOW}Postulataj varoj por feliĉo",
    SUP: "{BLACK}Provizita: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Urbaj industrioj --- {}",
    ACCEPT: "{BLACK}Postulata varo liverita pasintmonate",
    PROD: "{BLACK}Varo produktita pasintmonate",
    HIST: "{BLACK}Historio de (permanentaj) produktaĵpliigoj (lastaj 10 eventoj)",
    NEVER: "{WHITE}- cxi tiu industrio neniam permanente pliigis produktadon",
    PRODLVL: "{BLACK}Nuna produktadanivelo: {WHITE}{NUM}",
    NAME: "{BLACK}Nomo: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tipo: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Cxefsideja urbo: {WHITE}{TOWN}",
    VALID: "{BLACK}Validaj urboj: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Posedataj industrioj: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Cxi tio estas GS-teksto. {WHITE}Klaku min por la urba rakontopagxo. {BLACK}Jen pli da teksto.",
    OWNER: "Posedanto: {RAW_STRING}",
    DELIV: "{BLACK}Liveroj al cxi tiu instalaĵo kontribuos al la kresko kaj/aŭ feliĉo de la urbo",
    INCR: "{INDUSTRY} pliigas produktadon!",
}


def main():
    for lang, mp in [("japanese", GS_JA), ("simplified_chinese", GS_ZH), ("traditional_chinese", GS_ZHT),
                     ("afrikaans", GS_AF), ("esperanto", GS_EO)]:
        n = T.translate_file(os.path.join(ROOT, "src", "gs", "lang", lang + ".toml"), mp, GS_EN)
        print(f"{lang}: {n}")


if __name__ == "__main__":
    main()
