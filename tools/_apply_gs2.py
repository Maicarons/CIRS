"""GS (GameScript) translations - Batch 2: czech, slovak, croatian, serbian, russian.
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

GS_CS = {
    W: "Ahoj {COMPANY}!{}{}Hraješ hru s testovacím GS CIRS{}{}Verze Git tohoto GS je {NUM}",
    C: "{BLUE}Kapusta", HAPPY: "šťastný", UNHAPPY: "nešťastný",
    TOWN: "Město je {STRING}{}{}Chcete-li zjistit více o tomto městě (včetně požadavků na růst a spokojenost), otevřete Knihu příběhů a najděte stránku pro {TOWN}",
    GRIND: "{BLACK}Upozorňujeme, že se to aktuálně neobnovuje, dokud nebude Grind vypnut a znovu zapnut v nastavení GS",
    RND: "{BLACK}Náhodné slovo (test): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Aktuální rychlost růstu: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Náklad požadovaný pro růst",
    RQH: "{YELLOW}Náklad požadovaný pro spokojenost",
    SUP: "{BLACK}Dodáno: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Průmysl města --- {}",
    ACCEPT: "{BLACK}Požadovaný náklad dodaný minulý měsíc",
    PROD: "{BLACK}Vyrobený náklad minulý měsíc",
    HIST: "{BLACK}Historie (trvalého) zvýšení výroby (posledních 10 událostí)",
    NEVER: "{WHITE}- tento průmysl nikdy trvale nezvýšil výrobu",
    PRODLVL: "{BLACK}Aktuální úroveň výroby: {WHITE}{NUM}",
    NAME: "{BLACK}Název: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Typ: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Město sídla: {WHITE}{TOWN}",
    VALID: "{BLACK}Platná města: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Vlastněný průmysl: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Toto je text GS. {WHITE}Klikněte na mě pro stránku příběhu města. {BLACK}Zde je další text.",
    OWNER: "Vlastník: {RAW_STRING}",
    DELIV: "{BLACK}Dodávky tomuto průmyslu přispějí k růstu města a/nebo spokojenosti",
    INCR: "{INDUSTRY} zvyšuje výrobu!",
}
GS_SK = {
    W: "Ahoj {COMPANY}!{}{}Hráte hru s testovacím GS CIRS{}{}Verzia Git tohto GS je {NUM}",
    C: "{BLUE}Kapusta", HAPPY: "šťastný", UNHAPPY: "nešťastný",
    TOWN: "Mesto je {STRING}{}{}Ak chcete zistiť viac o tomto meste (vrátane požiadaviek na rast a spokojnosť), otvorte Knihu príbehov a nájdite stránku pre {TOWN}",
    GRIND: "{BLACK}Upozorňujeme, že sa to aktuálne neobnovuje, kým sa Grind nevypne a znova nezapne v nastaveniach GS",
    RND: "{BLACK}Náhodné slovo (test): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Aktuálna rýchlosť rastu: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Náklad vyžadovaný pre rast",
    RQH: "{YELLOW}Náklad vyžadovaný pre spokojnosť",
    SUP: "{BLACK}Dodané: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Priemysel mesta --- {}",
    ACCEPT: "{BLACK}Požadovaný náklad dodaný minulý mesiac",
    PROD: "{BLACK}Vyrobený náklad minulý mesiac",
    HIST: "{BLACK}História (trvalého) zvýšenia výroby (posledných 10 udalostí)",
    NEVER: "{WHITE}- tento priemysel nikdy trvalo nezvýšil výrobu",
    PRODLVL: "{BLACK}Aktuálna úroveň výroby: {WHITE}{NUM}",
    NAME: "{BLACK}Názov: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Typ: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Mesto sídla: {WHITE}{TOWN}",
    VALID: "{BLACK}Platné mestá: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Vlastnený priemysel: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Toto je text GS. {WHITE}Kliknite na mňa pre stránku príbehu mesta. {BLACK}Tu je viac textu.",
    OWNER: "Vlastník: {RAW_STRING}",
    DELIV: "{BLACK}Dodávky tomuto priemyslu prispievajú k rastu mesta a/alebo spokojnosti",
    INCR: "{INDUSTRY} zvyšuje výrobu!",
}
GS_HR = {
    W: "Bok {COMPANY}!{}{}Igraš igru s testnim GS-om CIRS{}{}Git verzija ovog GS-a je {NUM}",
    C: "{BLUE}Kupus", HAPPY: "sretan", UNHAPPY: "nesretan",
    TOWN: "Grad je {STRING}{}{}Da biste saznali više o ovom gradu (uključujući zahtjeve za rast i sreću), otvorite Knjigu priča i pronađite stranicu za {TOWN}",
    GRIND: "{BLACK}Imajte na umu da se ovo trenutno neće osvježiti osim ako se Grind ne isključi i uključi ponovno u postavkama GS-a",
    RND: "{BLACK}Slučajna riječ (test): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Trenutna stopa rasta: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Potrebni tereti za rast",
    RQH: "{YELLOW}Potrebni tereti za sreću",
    SUP: "{BLACK}Dostavljeno: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Industrija grada --- {}",
    ACCEPT: "{BLACK}Potreban teret isporučen prošli mjesec",
    PROD: "{BLACK}Proizveden teret prošli mjesec",
    HIST: "{BLACK}Povijest (trajnih) povećanja proizvodnje (zadnjih 10 događaja)",
    NEVER: "{WHITE}- ova industrija nikada trajno nije povećala proizvodnju",
    PRODLVL: "{BLACK}Trenutna razina proizvodnje: {WHITE}{NUM}",
    NAME: "{BLACK}Naziv: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Vrsta: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Grad sjedišta: {WHITE}{TOWN}",
    VALID: "{BLACK}Valjani gradovi: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Vlasnička industrija: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Ovo je GS tekst. {WHITE}Kliknite me za stranicu priče grada. {BLACK}Ovdje je još teksta.",
    OWNER: "Vlasnik: {RAW_STRING}",
    DELIV: "{BLACK}Isporuke ovoj industriji doprinijet će rastu grada i/ili sreći",
    INCR: "{INDUSTRY} povećava proizvodnju!",
}
GS_SR = {
    W: "Zdravo {COMPANY}!{}{}Igrate igru sa test GS-om CIRS{}{}Git verzija ovog GS-a je {NUM}",
    C: "{BLUE}Kupus", HAPPY: "srećan", UNHAPPY: "nesrećan",
    TOWN: "Grad je {STRING}{}{}Da biste saznali više o ovom gradu (uključujući zahteve za rast i sreću), otvorite Knjigu priča i pronađite stranicu za {TOWN}",
    GRIND: "{BLACK}Imajte na umu da se ovo trenutno neće osvežiti osim ako se Grind ne isključi i uključi ponovo u podešavanjima GS-a",
    RND: "{BLACK}Slučajna reč (test): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Trenutna stopa rasta: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Potrebni tovari za rast",
    RQH: "{YELLOW}Potrebni tovari za sreću",
    SUP: "{BLACK}Isporučeno: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Industrija grada --- {}",
    ACCEPT: "{BLACK}Potreban tovar isporučen prošlog meseca",
    PROD: "{BLACK}Proizveden tovar prošlog meseca",
    HIST: "{BLACK}Istorija (trajnih) povećanja proizvodnje (poslednjih 10 događaja)",
    NEVER: "{WHITE}- ova industrija nikada trajno nije povećala proizvodnju",
    PRODLVL: "{BLACK}Trenutni nivo proizvodnje: {WHITE}{NUM}",
    NAME: "{BLACK}Naziv: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Vrsta: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Grad sedišta: {WHITE}{TOWN}",
    VALID: "{BLACK}Važeći gradovi: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Vlasnička industrija: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Ovo je GS tekst. {WHITE}Kliknite me za stranicu priče grada. {BLACK}Ovdje je još teksta.",
    OWNER: "Vlasnik: {RAW_STRING}",
    DELIV: "{BLACK}Isporuke ovoj industriji doprineće rastu grada i/ili sreći",
    INCR: "{INDUSTRY} povećava proizvodnju!",
}
GS_RU = {
    W: "Привет {COMPANY}!{}{}Вы играете в игру с тестовым GS CIRS{}{}Версия Git этого GS: {NUM}",
    C: "{BLUE}Капуста", HAPPY: "счастлив", UNHAPPY: "несчастлив",
    TOWN: "Город: {STRING}{}{}Чтобы узнать больше об этом городе (включая требования к росту и счастью), откройте Книгу историй и найдите страницу для {TOWN}",
    GRIND: "{BLACK}Обратите внимание, что сейчас это не обновляется, пока Grind не будет выключен и снова включён в настройках GS",
    RND: "{BLACK}Случайное слово (тест): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Текущая скорость роста: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Требуемые грузы для роста",
    RQH: "{YELLOW}Требуемые грузы для счастья",
    SUP: "{BLACK}Поставлено: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Промышленность города --- {}",
    ACCEPT: "{BLACK}Требуемый груз, поставленный в прошлом месяце",
    PROD: "{BLACK}Произведённый груз в прошлом месяце",
    HIST: "{BLACK}История (постоянных) увеличений производства (последние 10 событий)",
    NEVER: "{WHITE}- эта промышленность никогда не увеличивала производство навсегда",
    PRODLVL: "{BLACK}Текущий уровень производства: {WHITE}{NUM}",
    NAME: "{BLACK}Название: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Тип: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Город штаб-квартиры: {WHITE}{TOWN}",
    VALID: "{BLACK}Допустимые города: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Принадлежащие промышленности: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Это текст GS. {WHITE}Нажмите на меня для страницы истории города. {BLACK}Вот ещё текст.",
    OWNER: "Владелец: {RAW_STRING}",
    DELIV: "{BLACK}Поставки этой промышленности будут способствовать росту города и/или счастью",
    INCR: "{INDUSTRY} увеличивает производство!",
}


def main():
    for lang, mp in [("czech", GS_CS), ("slovak", GS_SK), ("croatian", GS_HR),
                     ("serbian", GS_SR), ("russian", GS_RU)]:
        n = T.translate_file(os.path.join(ROOT, "src", "gs", "lang", lang + ".toml"), mp, GS_EN)
        print(f"{lang}: {n}")


if __name__ == "__main__":
    main()
