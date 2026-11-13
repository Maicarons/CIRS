"""GS (GameScript) translations - Batch 1: es_MX, catalan, galician, pt_BR, romanian.
Value-keyed. Placeholder-only GS strings are intentionally omitted (stay English)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _translate as T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GS_EN = os.path.join(ROOT, "src", "gs", "lang", "english.toml")

# shared translatable english values
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

GS_ESMX = {
    W: "Hola {COMPANY}!{}{}Estás jugando una partida con el GS de prueba de CIRS{}{}La versión de Git de este GS es {NUM}",
    C: "{BLUE}Repollo", HAPPY: "feliz", UNHAPPY: "infeliz",
    TOWN: "La ciudad es {STRING}{}{}Para saber más de esta ciudad (incluyendo requisitos de crecimiento y felicidad), abre el Libro de historias y encuentra la página de {TOWN}",
    GRIND: "{BLACK}Ten en cuenta que esto no se actualizará actualmente a menos que Grind se apague y se encienda en la configuración del GS",
    RND: "{BLACK}Palabra aleatoria (prueba): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Tasa de crecimiento actual: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Cargas requeridas para el crecimiento",
    RQH: "{YELLOW}Cargas requeridas para la felicidad",
    SUP: "{BLACK}Suministrado: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Industrias de la ciudad --- {}",
    ACCEPT: "{BLACK}Carga requerida suministrada el mes pasado",
    PROD: "{BLACK}Carga producida el mes pasado",
    HIST: "{BLACK}Historial de aumentos (permanentes) de producción (últimos 10 eventos)",
    NEVER: "{WHITE}- esta industria nunca ha aumentado la producción de forma permanente",
    PRODLVL: "{BLACK}Nivel de producción actual: {WHITE}{NUM}",
    NAME: "{BLACK}Nombre: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tipo: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Ciudad de la sede: {WHITE}{TOWN}",
    VALID: "{BLACK}Ciudades válidas: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Industrias propiedad de: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Este es un texto del GS. {WHITE}Haz clic en mí para ver la página de historia de la ciudad. {BLACK}Aquí hay más texto.",
    OWNER: "Propietario: {RAW_STRING}",
    DELIV: "{BLACK}Las entregas a esta industria contribuirán al crecimiento y/o la felicidad de la ciudad",
    INCR: "{INDUSTRY} ¡aumenta la producción!",
}
GS_CA = {
    W: "Hola {COMPANY}!{}{}Esteu jugant una partida amb el GS de prova de CIRS{}{}La versió de Git d'aquest GS és {NUM}",
    C: "{BLUE}Col", HAPPY: "feliç", UNHAPPY: "infeliç",
    TOWN: "La ciutat és {STRING}{}{}Per saber-ne més d'aquesta ciutat (inclosos els requisits de creixement i felicitat), obriu el Llibre d'històries i trobeu la pàgina de {TOWN}",
    GRIND: "{BLACK}Observeu que això no s'actualitzarà actualment tret que Grind s'apagui i s'encengui a la configuració del GS",
    RND: "{BLACK}Paraula aleatòria (prova): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Taxa de creixement actual: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Càrregues requerides per al creixement",
    RQH: "{YELLOW}Càrregues requerides per a la felicitat",
    SUP: "{BLACK}Subministrat: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Indústries de la ciutat --- {}",
    ACCEPT: "{BLACK}Càrrega requerida subministrada el mes passat",
    PROD: "{BLACK}Càrrega produïda el mes passat",
    HIST: "{BLACK}Historial d'augments (permanents) de producció (últims 10 esdeveniments)",
    NEVER: "{WHITE}- aquesta indústria mai ha augmentat la producció de manera permanent",
    PRODLVL: "{BLACK}Nivell de producció actual: {WHITE}{NUM}",
    NAME: "{BLACK}Nom: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tipus: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Ciutat de la seu: {WHITE}{TOWN}",
    VALID: "{BLACK}Ciutats vàlides: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Indústries en propietat de: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Aquest és un text del GS. {WHITE}Feu clic a mi per veure la pàgina d'història de la ciutat. {BLACK}Aquí hi ha més text.",
    OWNER: "Propietari: {RAW_STRING}",
    DELIV: "{BLACK}Els lliuraments a aquesta indústria contribuiran al creixement i/o la felicitat de la ciutat",
    INCR: "{INDUSTRY} augmenta la producció!",
}
GS_GL = {
    W: "Ola {COMPANY}!{}{}Estás xogando unha partida co GS de proba de CIRS{}{}A versión de Git deste GS é {NUM}",
    C: "{BLUE}Repolo", HAPPY: "feliz", UNHAPPY: "infeliz",
    TOWN: "A cidade é {STRING}{}{}Para saber máis desta cidade (incluíndo requisitos de crecemento e felicidade), abre o Libro de historias e atopa a páxina de {TOWN}",
    GRIND: "{BLACK}Tecnos en conta que isto non se actualizará actualmente a menos que Grind se apague e acenda na configuración do GS",
    RND: "{BLACK}Palabra aleatoria (proba): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Taxa de crecemento actual: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Cargas requiridas para o crecemento",
    RQH: "{YELLOW}Cargas requiridas para a felicidade",
    SUP: "{BLACK}Suministrado: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Industrias da cidade --- {}",
    ACCEPT: "{BLACK}Carga requirida suministrada o mes pasado",
    PROD: "{BLACK}Carga producida o mes pasado",
    HIST: "{BLACK}Historial de aumentos (permanentes) de produción (últimos 10 eventos)",
    NEVER: "{WHITE}- esta industria nunca aumentou a produción de forma permanente",
    PRODLVL: "{BLACK}Nivel de produción actual: {WHITE}{NUM}",
    NAME: "{BLACK}Nome: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tipo: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Cidade da sede: {WHITE}{TOWN}",
    VALID: "{BLACK}Cidades válidas: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Industrias en propiedade de: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Este é un texto do GS. {WHITE}Fai clic en min para ver a páxina de historia da cidade. {BLACK}Aquí hai máis texto.",
    OWNER: "Propietario: {RAW_STRING}",
    DELIV: "{BLACK}As entregas a esta industria contribuirán ao crecemento e/ou á felicidade da cidade",
    INCR: "{INDUSTRY} aumenta a produción!",
}
GS_PTBR = {
    W: "Olá {COMPANY}!{}{}Você está jogando um jogo com o GS de teste do CIRS{}{}A versão Git deste GS é {NUM}",
    C: "{BLUE}Repolho", HAPPY: "feliz", UNHAPPY: "infeliz",
    TOWN: "A cidade é {STRING}{}{}Para saber mais sobre esta cidade (incluindo requisitos de crescimento e felicidade), abra o Livro de Histórias e encontre a página de {TOWN}",
    GRIND: "{BLACK}Observe que isso não será atualizado no momento, a menos que o Grind seja desligado e ligado novamente nas configurações do GS",
    RND: "{BLACK}Palavra aleatória (teste): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Taxa de crescimento atual: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Cargas necessárias para o crescimento",
    RQH: "{YELLOW}Cargas necessárias para a felicidade",
    SUP: "{BLACK}Fornecido: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Indústrias da cidade --- {}",
    ACCEPT: "{BLACK}Carga necessária fornecida no mês passado",
    PROD: "{BLACK}Carga produzida no mês passado",
    HIST: "{BLACK}Histórico de aumentos (permanentes) de produção (últimos 10 eventos)",
    NEVER: "{WHITE}- esta indústria nunca aumentou a produção permanentemente",
    PRODLVL: "{BLACK}Nível de produção atual: {WHITE}{NUM}",
    NAME: "{BLACK}Nome: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tipo: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Cidade da sede: {WHITE}{TOWN}",
    VALID: "{BLACK}Cidades válidas: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Indústrias de propriedade de: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Este é um texto do GS. {WHITE}Clique em mim para a página de histórico da cidade. {BLACK}Aqui está mais texto.",
    OWNER: "Proprietário: {RAW_STRING}",
    DELIV: "{BLACK}As entregas a esta indústria contribuirão para o crescimento e/ou felicidade da cidade",
    INCR: "{INDUSTRY} aumenta a produção!",
}
GS_RO = {
    W: "Salut {COMPANY}!{}{}Jucați un joc cu GS-ul de test CIRS{}{}Versiunea Git a acestui GS este {NUM}",
    C: "{BLUE}Varză", HAPPY: "fericit", UNHAPPY: "nefericit",
    TOWN: "Orașul este {STRING}{}{}Pentru a afla mai multe despre acest oraș (inclusiv cerințele de creștere și fericire), deschideți Cartea de Povești și găsiți pagina pentru {TOWN}",
    GRIND: "{BLACK}Rețineți că acest lucru nu se va reîmprospăta în prezent decât dacă Grind este oprit și pornit din nou în setările GS",
    RND: "{BLACK}Cuvânt aleatoriu (test): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Rata de creștere actuală: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Mărfuri necesare pentru creștere",
    RQH: "{YELLOW}Mărfuri necesare pentru fericire",
    SUP: "{BLACK}Furnizat: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Industriile orașului --- {}",
    ACCEPT: "{BLACK}Marfă necesară furnizată luna trecută",
    PROD: "{BLACK}Marfă produsă luna trecută",
    HIST: "{BLACK}Istoricul creșterilor (permanente) de producție (ultimele 10 evenimente)",
    NEVER: "{WHITE}- această industrie nu a crescut niciodată producția în mod permanent",
    PRODLVL: "{BLACK}Nivelul de producție actual: {WHITE}{NUM}",
    NAME: "{BLACK}Nume: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tip: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Orașul sediului: {WHITE}{TOWN}",
    VALID: "{BLACK}Orașe valide: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Industrii deținute de: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Acesta este un text GS. {WHITE}Faceți clic pe mine pentru pagina de poveste a orașului. {BLACK}Iată mai mult text.",
    OWNER: "Proprietar: {RAW_STRING}",
    DELIV: "{BLACK}Livrările către această industrie vor contribui la creșterea și/sau fericirea orașului",
    INCR: "{INDUSTRY} crește producția!",
}


def main():
    for lang, mp in [("spanish_MX", GS_ESMX), ("catalan", GS_CA), ("galician", GS_GL),
                     ("portuguese_BR", GS_PTBR), ("romanian", GS_RO)]:
        n = T.translate_file(os.path.join(ROOT, "src", "gs", "lang", lang + ".toml"), mp, GS_EN)
        print(f"{lang}: {n}")


if __name__ == "__main__":
    main()
