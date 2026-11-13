"""GS (GameScript) translations - Batch 3: belarusian, hungarian, turkish, indonesian, estonian.
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

GS_BE = {
    W: "Прывітанне {COMPANY}!{}{}Вы гуляеце ў гульню з тэставым GS CIRS{}{}Версія Git гэтага GS: {NUM}",
    C: "{BLUE}Капуста", HAPPY: "шчаслівы", UNHAPPY: "няшчаслівы",
    TOWN: "Горад: {STRING}{}{}Каб даведацца больш пра гэты горад (уключаючы патрабаванні да росту і шчасця), адкрыйце Кнігу гісторый і знайдзіце старонку для {TOWN}",
    GRIND: "{BLACK}Звярніце ўвагу, што зараз гэта не абнаўляецца, пакуль Grind не будзе выключаны і зноў уключаны ў наладах GS",
    RND: "{BLACK}Выпадковае слова (тэст): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Бягучая хуткасць росту: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Патрабаваныя грузы для росту",
    RQH: "{YELLOW}Патрабаваныя грузы для шчасця",
    SUP: "{BLACK}Пастаўлена: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Прамысловасць горада --- {}",
    ACCEPT: "{BLACK}Патрабаваны груз, пастаўлены ў мінулым месяцы",
    PROD: "{BLACK}Выраблены груз у мінулым месяцы",
    HIST: "{BLACK}Гісторыя (пастаянных) павелічэнняў вытворчасці (апошнія 10 падзей)",
    NEVER: "{WHITE}- гэтая прамысловасць ніколі не павялічвала вытворчасць назаўсёды",
    PRODLVL: "{BLACK}Бягучы ўзровень вытворчасці: {WHITE}{NUM}",
    NAME: "{BLACK}Назва: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Тып: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Горад штаб-кватэры: {WHITE}{TOWN}",
    VALID: "{BLACK}Дапушчальныя гарады: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Уласная прамысловасць: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Гэта тэкст GS. {WHITE}Націсніце на мяне для старонкі гісторыі горада. {BLACK}Вось яшчэ тэкст.",
    OWNER: "Уладальнік: {RAW_STRING}",
    DELIV: "{BLACK}Пастаўкі гэтай прамысловасці будуць спрыяць росту горада і/або шчасцю",
    INCR: "{INDUSTRY} павялічвае вытворчасць!",
}
GS_HU = {
    W: "Helló {COMPANY}!{}{}Egy játékot játszol a CIRS teszt-GS-ével{}{}Ennek a GS-nek a Git verziója: {NUM}",
    C: "{BLUE}Káposzta", HAPPY: "boldog", UNHAPPY: "boldogtalan",
    TOWN: "A város: {STRING}{}{}Ha többet szeretnél megtudni erről a városról (beleértve a növekedési és boldogsági követelményeket), nyisd meg a Történetkönyvet, és keresd meg {TOWN} oldalát",
    GRIND: "{BLACK}Vedd figyelembe, hogy ez jelenleg nem frissül, amíg a Grind nincs kikapcsolva és újra bekapcsolva a GS beállításaiban",
    RND: "{BLACK}Véletlen szó (teszt): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Jelenlegi növekedési sebesség: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}A növekedéshez szükséges áruk",
    RQH: "{YELLOW}A boldogsághoz szükséges áruk",
    SUP: "{BLACK}Szállítva: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- A város ipara --- {}",
    ACCEPT: "{BLACK}Az előző hónapban szállított szükséges áru",
    PROD: "{BLACK}Az előző hónapban előállított áru",
    HIST: "{BLACK}A (végleges) termelésnövelések története (utolsó 10 esemény)",
    NEVER: "{WHITE}- ez az iparág soha nem növelte véglegesen a termelést",
    PRODLVL: "{BLACK}Jelenlegi termelési szint: {WHITE}{NUM}",
    NAME: "{BLACK}Név: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Típus: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Központi város: {WHITE}{TOWN}",
    VALID: "{BLACK}Érvényes városok: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Tulajdonolt iparágak: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Ez egy GS szöveg. {WHITE}Kattints rám a város történetoldaláért. {BLACK}Itt van még szöveg.",
    OWNER: "Tulajdonos: {RAW_STRING}",
    DELIV: "{BLACK}Az iparágba érkező szállítmányok hozzájárulnak a város növekedéséhez és/vagy boldogságához",
    INCR: "{INDUSTRY} növeli a termelést!",
}
GS_TR = {
    W: "Merhaba {COMPANY}!{}{}CIRS test GS'i ile bir oyun oynuyorsun{}{}Bu GS'in Git sürümü: {NUM}",
    C: "{BLUE}Lahana", HAPPY: "mutlu", UNHAPPY: "mutsuz",
    TOWN: "Şehir: {STRING}{}{}Bu şehir hakkında daha fazla bilgi edinmek için (büyüme ve mutluluk gereksinimleri dahil) Hikaye Kitabını aç ve {TOWN} sayfasını bul",
    GRIND: "{BLACK}Bunun şu an güncellenmeyeceğini unutma, ta ki GS ayarlarında Grind kapatılıp tekrar açılana kadar",
    RND: "{BLACK}Rastgele kelime (test): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Mevcut büyüme oranı: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Büyüme için gereken yükler",
    RQH: "{YELLOW}Mutluluk için gereken yükler",
    SUP: "{BLACK}Teslim edildi: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Şehrin sanayisi --- {}",
    ACCEPT: "{BLACK}Geçen ay teslim edilen gerekli yük",
    PROD: "{BLACK}Geçen ay üretilen yük",
    HIST: "{BLACK}Üretim (kalıcı) artışlarının geçmişi (son 10 olay)",
    NEVER: "{WHITE}- bu sanayi hiçbir zaman kalıcı olarak üretimi artırmadı",
    PRODLVL: "{BLACK}Mevcut üretim seviyesi: {WHITE}{NUM}",
    NAME: "{BLACK}Ad: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tür: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Genel merkez şehri: {WHITE}{TOWN}",
    VALID: "{BLACK}Geçerli şehirler: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Sahip olunan sanayiler: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Bu bir GS metnidir. {WHITE}Şehrin hikaye sayfası için bana tıkla. {BLACK}İşte biraz daha metin.",
    OWNER: "Sahip: {RAW_STRING}",
    DELIV: "{BLACK}Bu sanayiye yapılan teslimatlar şehrin büyümesine ve/veya mutluluğuna katkıda bulunur",
    INCR: "{INDUSTRY} üretimi artırıyor!",
}
GS_ID = {
    W: "Halo {COMPANY}!{}{}Anda memainkan permainan dengan GS uji CIRS{}{}Versi Git dari GS ini adalah {NUM}",
    C: "{BLUE}Kubis", HAPPY: "senang", UNHAPPY: "tidak senang",
    TOWN: "Kota adalah {STRING}{}{}Untuk mengetahui lebih lanjut tentang kota ini (termasuk persyaratan pertumbuhan dan kebahagiaan), buka Buku Cerita dan temukan halaman untuk {TOWN}",
    GRIND: "{BLACK}Perhatikan bahwa ini tidak akan menyegarkan saat ini kecuali Grind dimatikan dan dihidupkan kembali di pengaturan GS",
    RND: "{BLACK}Kata acak (tes): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Tingkat pertumbuhan saat ini: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Muatan yang diperlukan untuk pertumbuhan",
    RQH: "{YELLOW}Muatan yang diperlukan untuk kebahagiaan",
    SUP: "{BLACK}Disediakan: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Industri kota --- {}",
    ACCEPT: "{BLACK}Muatan yang diperlukan disediakan bulan lalu",
    PROD: "{BLACK}Muatan yang diproduksi bulan lalu",
    HIST: "{BLACK}Riwayat peningkatan produksi (permanen) (10 kejadian terakhir)",
    NEVER: "{WHITE}- industri ini tidak pernah meningkatkan produksi secara permanen",
    PRODLVL: "{BLACK}Tingkat produksi saat ini: {WHITE}{NUM}",
    NAME: "{BLACK}Nama: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tipe: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Kota markas: {WHITE}{TOWN}",
    VALID: "{BLACK}Kota yang valid: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Industri yang dimiliki: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}Ini adalah teks GS. {WHITE}Klik saya untuk halaman cerita kota. {BLACK}Berikut lebih banyak teks.",
    OWNER: "Pemilik: {RAW_STRING}",
    DELIV: "{BLACK}Pengiriman ke industri ini akan berkontribusi pada pertumbuhan dan/atau kebahagiaan kota",
    INCR: "{INDUSTRY} meningkatkan produksi!",
}
GS_ET = {
    W: "Tere {COMPANY}!{}{}Mängid mängu CIRS-i test-GS-iga{}{}Selle GS-i Git-versioon on {NUM}",
    C: "{BLUE}Kapsas", HAPPY: "õnnelik", UNHAPPY: "ebaonnelik",
    TOWN: "Linn on {STRING}{}{}Selle linna kohta lisateabe saamiseks (sealhulgas kasvu- ja õnnetingimused) ava Lugude raamat ja leia {TOWN} leht",
    GRIND: "{BLACK}Pane tähele, et seda ei värskendata praegu, kuni Grind lülitatakse GS-i seadetes välja ja uuesti sisse",
    RND: "{BLACK}Juhuslik sõna (test): {WHITE}{RAW_STRING}",
    GROWTH: "{BLACK}Praegune kasvukiirus: {WHITE}{RAW_STRING}",
    RQG: "{YELLOW}Kasvuks nõutavad veosed",
    RQH: "{YELLOW}Õnneks nõutavad veosed",
    SUP: "{BLACK}Tarnitud: {WHITE}{CARGO_LONG}",
    TI: "{BLACK}--- Linna tööstus --- {}",
    ACCEPT: "{BLACK}Eelmise kuul tarnitud nõutav vedu",
    PROD: "{BLACK}Eelmise kuul toodetud vedu",
    HIST: "{BLACK}(Püsivate) tootmise suurendamiste ajalugu (viimased 10 sündmust)",
    NEVER: "{WHITE}- see tööstus ei ole kunagi tootmist püsivalt suurendanud",
    PRODLVL: "{BLACK}Praegune tootmistase: {WHITE}{NUM}",
    NAME: "{BLACK}Nimi: {WHITE}{RAW_STRING}",
    TYPE: "{BLACK}Tüüp: {WHITE}{RAW_STRING}",
    HQ: "{BLACK}Peakontori linn: {WHITE}{TOWN}",
    VALID: "{BLACK}Kehtivad linnad: {WHITE}{RAW_STRING}",
    OWNED: "{BLACK}Omandatud tööstused: {WHITE}{RAW_STRING}",
    CLICK: "{BLACK}See on GS-tekst. {WHITE}Klõpsa mind linna lugemislehe jaoks. {BLACK}Siin on veel teksti.",
    OWNER: "Omanik: {RAW_STRING}",
    DELIV: "{BLACK}Tarned sellele tööstusele aitavad kaasa linna kasvule ja/või õnnele",
    INCR: "{INDUSTRY} suurendab tootmist!",
}


def main():
    for lang, mp in [("belarusian", GS_BE), ("hungarian", GS_HU), ("turkish", GS_TR),
                     ("indonesian", GS_ID), ("estonian", GS_ET)]:
        n = T.translate_file(os.path.join(ROOT, "src", "gs", "lang", lang + ".toml"), mp, GS_EN)
        print(f"{lang}: {n}")


if __name__ == "__main__":
    main()
