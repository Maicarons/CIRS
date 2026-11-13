"""GS (GameScript) translations - Batch 5 (final): latin, luxembourgish, gaelic, welsh, tamil.
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

GS_LA = {
    W: "Salve {COMPANY}!{}{}Ludis ludum cum CIRS probationis GS{}{}Versio Git huius GS est {NUM}",
    C: "{BLUE}Brassica", HAPPY: "laetus", UNHAPPY: "tristis",
    TOWN: "Oppidum est {STRING}{}{}Ut plura de hoc oppido scias (inclusis incrementi et felicitatis postulatis), aperi Librum Fabularum et paginam pro {TOWN} inveni",
    GRIND: "{BLACK}Nota hoc nunc non renovari nisi Grind in GS praeferentiis exstinguatur et rursus accendatur",
    RND: "{BLACK}Ver fortuitum (probatio): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Praesens incrementi ratio: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Merces requisitae ad incrementum",
    RQH: "{YELLOW}Merces requisitae ad felicitatem",
    SUP: "{BLACK}Praebitum: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Oppidi industriae --- {}",
    ACCEPT: "{BLACK}Merx requisita mense praeterito praebita",
    PROD: "{BLACK}Merx mense praeterito producta",
    HIST: "{BLACK}Historia augmentorum (permanentium) productionis (proxima 10 eventa)",
    NEVER: "{WHITE}- haec industria numquam productionem permanentur auxit",
    PRODLVL: "{BLACK}Praesens productionis gradus: {WHITE}{NUM}",
    NAME: "{BLACK}Nomen: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Genus: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Oppidum principale: {WHITE}{TOWN}",
    VALID: "{BLACK}Oppida valida: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Industriae possessae: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Hic textus GS est. {WHITE}Me preme pro pagina fabulae oppidi. {BLACK}Hic plus textus est.",
    OWNER: "Dominus: {RAW_STRING}",
    DELIV: "{BLACK}Traditiones huic industriae conferent ad incrementum oppidi et/vel felicitatem",
    INCR: "{INDUSTRY} productionem auget!",
}
GS_LB = {
    W: "Moien {COMPANY}!{}{}Du spillst e Spill mat dem CIRS Test-GS{}{}D'Git-Versioun vun dësem GS ass {NUM}",
    C: "{BLUE}Kappes", HAPPY: "glécklech", UNHAPPY: "onglécklech",
    TOWN: "D'Stad ass {STRING}{}{}Fir méi iwwer dës Stad erauszefannen (inklusiv Wuesstem- a Glécksufuerderungen), maach de Geschichtbuch op a fann d'Säit fir {TOWN}",
    GRIND: "{BLACK}Bemierk datt dat elo net frëscht gemaach gëtt, ausser Grind gëtt an de GS-Astellungen aus- an nees ungeschalt",
    RND: "{BLACK}Zoufällegt Wuert (Test): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Aktuell Wuesstem-Taux: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Ufuerderungen am Wuesstem",
    RQH: "{YELLOW}Ufuerderungen am Gléck",
    SUP: "{BLACK}Geliwwert: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Stad Industrien --- {}",
    ACCEPT: "{BLACK}Ufuerdert Luedung déi leschte Mount geliwwert gouf",
    PROD: "{BLACK}Luedung déi leschte Mount produzéiert gouf",
    HIST: "{BLACK}Historie vun (permanente) Produktiounserhéijungen (lescht 10 Evenementer)",
    NEVER: "{WHITE}- dës Industrie huet d'Produktioun niemols permanent eropgesat",
    PRODLVL: "{BLACK}Aktuellen Produktiounsniveau: {WHITE}{NUM}",
    NAME: "{BLACK}Numm: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Typ: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Haaptquartéier-Stad: {WHITE}{TOWN}",
    VALID: "{BLACK}Gëlteg Stied: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Besaten Industrien: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Dëst ass e GS-Text. {WHITE}Klick op mech fir d'Stad Geschichtssäit. {BLACK}Hei ass méi Text.",
    OWNER: "Besëtzer: {RAW_STRING}",
    DELIV: "{BLACK}Liwwerunge fir dës Industrie bidroen zum Wuesstem an/oder Gléck vun der Stad",
    INCR: "{INDUSTRY} erhéicht d'Produktioun!",
}
GS_GD = {
    W: "Halò {COMPANY}!{}{}Tha thu a' cluich geama le GS deuchainn CIRS{}{}Tha an t-ainm-phàirt Git den GS seo {NUM}",
    C: "{BLUE}Càl", HAPPY: "toilichte", UNHAPPY: "mi-thoileach",
    TOWN: "Is e {STRING} a th' anns a' bhaile{}{}Gus barrachd fiosrachaidh fhaighinn mun bhaile seo (a' gabhail a-steach riatanasan fàis is sonais), fosgail Leabhar na Sgeulachd agus lorg an duilleag airson {TOWN}",
    GRIND: "{BLACK}Thoir an aire nach dèid ath-nuadhachadh a dhèanamh air an-dràsta mura tèid Grind a chur dheth agus air ais air anns na roghainnean GS",
    RND: "{BLACK}Facal air thuaiream (deuchainn): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Reat fàis làithreach: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Leithbheathan a tha riatanach airson fàs",
    RQH: "{YELLOW}Leithbheathan a tha riatanach airson sonas",
    SUP: "{BLACK}Air a sholar: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Industrian a' bhaile --- {}",
    ACCEPT: "{BLACK}Leithbheathach riatanach a chaidh a sholar am mìos sa chaidh",
    PROD: "{BLACK}Leithbheathach a chaidh a chinneachadh am mìos sa chaidh",
    HIST: "{BLACK}Eachdraidh de mheudachaidhean (maireannach) cinneasachaidh (10 tachartasan mu dheireadh)",
    NEVER: "{WHITE}- cha do mheudaich an industri seo cinneasachadh gu maireannach a-riamh",
    PRODLVL: "{BLACK}Ìre cinneasachaidh làithreach: {WHITE}{NUM}",
    NAME: "{BLACK}Ainm: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Seòrsa: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Am baile prìomh-oifis: {WHITE}{TOWN}",
    VALID: "{BLACK}Bailean dligheach: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Industrian seilbhte: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Is e teacsa GS a tha seo. {WHITE}Thoir cliog orm airson duilleag sgeulachd a' bhaile. {BLACK}Seo barrachd teacsa.",
    OWNER: "Sealbhadair: {RAW_STRING}",
    DELIV: "{BLACK}Bidh liubhairtidhean dhan industri seo a' cur ri fàs agus/no sonas a' bhaile",
    INCR: "{INDUSTRY} a' meudachadh cinneasachaidh!",
}
GS_CY = {
    W: "Helo {COMPANY}!{}{}Rwyt ti'n chwarae gêm gyda GS prawf CIRS{}{}Fersiwn Git y GS hwn yw {NUM}",
    C: "{BLUE}Brwslys", HAPPY: "hapus", UNHAPPY: "anhapus",
    TOWN: "Mae'r dref yn {STRING}{}{}I ddarganfod mwy am y dref hon (gan gynnwys gofynion twf a hapusrwydd), agor y Llyfr Storiau a chwilio am dudalen ar gyfer {TOWN}",
    GRIND: "{BLACK}Cofia nad yw hyn yn adnewyddu ar hyn o bryd oni bai bod Grind wedi'i ddiffodd a'i droi ymlaen eto yn y gosodiadau GS",
    RND: "{BLACK}Gair ar hap (prawf): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Cyfradd twf gyfredol: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Nwyddau gofynnol ar gyfer twf",
    RQH: "{YELLOW}Nwyddau gofynnol ar gyfer hapusrwydd",
    SUP: "{BLACK}Cyflenwyd: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Diwydiannau'r dref --- {}",
    ACCEPT: "{BLACK}Nwydd gofynnol a gyflenwyd y mis diwethaf",
    PROD: "{BLACK}Nwydd a gynhyrchwyd y mis diwethaf",
    HIST: "{BLACK}Hanes y cynnydd (parhaol) yn y cynhyrchiad (10 digwyddiad diwethaf)",
    NEVER: "{WHITE}- ni chynhyrchodd y diwydiant hwn fwy o gynhyrchiad yn barhaol erioed",
    PRODLVL: "{BLACK}Lefel gynhyrchu gyfredol: {WHITE}{NUM}",
    NAME: "{BLACK}Enw: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Math: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Dref y prif bencadlys: {WHITE}{TOWN}",
    VALID: "{BLACK}Trefi dilys: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Diwydiannau perchennog: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Mae hwn yn destun GS. {WHITE}Clicia arna i am dudalen stori'r dref. {BLACK}Dyma fwy o destun.",
    OWNER: "Perchennog: {RAW_STRING}",
    DELIV: "{BLACK}Bydd cyflenwadau i'r diwydiant hwn yn cyfrannu at dwf a/neu hapusrwydd y dref",
    INCR: "{INDUSTRY} yn cynyddu'r cynhyrchiad!",
}
GS_TA = {
    W: "வணக்கம் {COMPANY}!{}{}நீங்கள் CIRS சோதனை GS உடன் ஒரு விளையாட்டை விளையாடுகிறீர்கள்{}{}இந்த GS இன் Git பதிப்பு {NUM}",
    C: "{BLUE}முட்டைக்கோஸ்", HAPPY: "மகிழ்ச்சி", UNHAPPY: "மகிழ்ச்சியற்ற",
    TOWN: "நகரம் {STRING}{}{}இந்த நகரம் பற்றி மேலும் அறிய (வளர்ச்சி மற்றும் மகிழ்ச்சி தேவைகள் உட்பட), கதைப் புத்தகத்தைத் திறந்து {TOWN}க்கான பக்கத்தைக் கண்டறியவும்",
    GRIND: "{BLACK}GS அமைப்புகளில் Grind அணைக்கப்பட்டு மீண்டும் இயக்கப்படாவிட்டால் தவிர, இது தற்போது புதுப்பிக்கப்படாது என்பதை நினைவில் கொள்ளவும்",
    RND: "{BLACK}சீரற்ற சொல் (சோதனை): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}தற்போதைய வளர்ச்சி விகிதம்: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}வளர்ச்சிக்குத் தேவையான சரக்குகள்",
    RQH: "{YELLOW}மகிழ்ச்சிக்குத் தேவையான சரக்குகள்",
    SUP: "{BLACK}வழங்கப்பட்டது: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- நகரத் தொழில்கள் --- {}",
    ACCEPT: "{BLACK}கடந்த மாதம் வழங்கப்பட்ட தேவையான சரக்கு",
    PROD: "{BLACK}கடந்த மாதம் உற்பத்தி செய்யப்பட்ட சரக்கு",
    HIST: "{BLACK}உற்பத்தி (நிரந்தர) அதிகரிப்புகளின் வரலாறு (கடந்த 10 நிகழ்வுகள்)",
    NEVER: "{WHITE}- இந்தத் தொழில் உற்பத்தியை ஒருபோதும் நிரந்தரமாக அதிகரிக்கவில்லை",
    PRODLVL: "{BLACK}தற்போதைய உற்பத்தி நிலை: {WHITE}{NUM}",
    NAME: "{BLACK}பெயர்: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}வகை: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}தலைமையக நகரம்: {WHITE}{TOWN}",
    VALID: "{BLACK}செல்லுபடியாகும் நகரங்கள்: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}சொந்தமான தொழில்கள்: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}இது ஒரு GS உரை. {WHITE}நகரக் கதைப் பக்கத்திற்கு என்னைக் கிளிக் செய்யவும். {BLACK}இங்கே மேலும் உரை உள்ளது.",
    OWNER: "உரிமையாளர்: {RAW_STRING}",
    DELIV: "{BLACK}இந்தத் தொழிலுக்கான விநியோகங்கள் நகரின் வளர்ச்சி மற்றும்/அல்லது மகிழ்ச்சிக்கு பங்களிக்கும்",
    INCR: "{INDUSTRY} உற்பத்தியை அதிகரிக்கிறது!",
}


def main():
    for lang, mp in [("latin", GS_LA), ("luxembourgish", GS_LB), ("gaelic", GS_GD),
                     ("welsh", GS_CY), ("tamil", GS_TA)]:
        n = T.translate_file(os.path.join(ROOT, "src", "gs", "lang", lang + ".toml"), mp, GS_EN)
        print(f"{lang}: {n}")


if __name__ == "__main__":
    main()
