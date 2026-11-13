"""Apply Korean and Arabic GameScript translations.

Both languages already have grf translated (4.x carryover + AI) but their gs
files are still English placeholders. This fills gs with AI translations,
preserving every NML placeholder verbatim.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _translate as T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GS_EN = os.path.join(ROOT, "src", "gs", "lang", "english.toml")

KO = {
    "Hello {COMPANY}!{}{}You are playing a game with CIRS test GS{}{}Git version of this GS is {NUM}":
        "안녕하세요 {COMPANY}님!{}{}CIRS 테스트 GS로 게임을 하고 있습니다{}{}이 GS의 Git 버전은 {NUM}입니다",
    "{BLUE}Cabbage": "{BLUE}양배추",
    "happy": "행복",
    "unhappy": "불행",
    "Town is {STRING}{}{}To find out more about this town (including growth and happiness requirements), open the Story Book, and find the page for {TOWN}":
        "마을은 {STRING}{}{}이 마을에 대해(성장 및 행복 요구사항 포함) 자세히 알아보려면 이야기 책을 열고 {TOWN}에 대한 페이지를 찾으세요",
    "{BLACK}Note that this won't refresh currently unless Grind is turned off and on in GS settings":
        "{BLACK}현재 이 내용은 GS 설정에서 그라인드를 끄고 켜지 않으면 새로고침되지 않습니다",
    "{BLACK}Random word (test): {WHITE}{RAW_STRING}":
        "{BLACK}임의 단어(테스트): {WHITE}{RAW_STRING}",
    "{BLACK}Current growth rate: {WHITE}{RAW_STRING}":
        "{BLACK}현재 성장률: {WHITE}{RAW_STRING}",
    "{YELLOW}Required cargos for growth": "{YELLOW}성장에 필요한 화물",
    "{YELLOW}Required cargos for happiness": "{YELLOW}행복에 필요한 화물",
    "{BLACK}Supplied: {WHITE}{CARGO_LONG}": "{BLACK}공급됨: {WHITE}{CARGO_LONG}",
    "{BLACK}--- Town industries --- {}": "{BLACK}--- 마을 산업 시설 --- {}",
    "{BLACK}Required cargo supplied last month": "{BLACK}지난달 공급된 필수 화물",
    "{BLACK}Cargo produced last month": "{BLACK}지난달 생산된 화물",
    "{BLACK}Production (permanent) increase history (last 10 events)":
        "{BLACK}생산량(영구적) 증가 기록 (최근 10건)",
    "{WHITE}- this industry has never permanently increased production":
        "{WHITE}- 이 산업 시설은 영구적으로 생산량을 증가시킨 적이 없습니다",
    "{BLACK}Current production level: {WHITE}{NUM}":
        "{BLACK}현재 생산 수준: {WHITE}{NUM}",
    "{BLACK}Name: {WHITE}{RAW_STRING}": "{BLACK}이름: {WHITE}{RAW_STRING}",
    "{BLACK}Type: {WHITE}{RAW_STRING}": "{BLACK}유형: {WHITE}{RAW_STRING}",
    "{BLACK}HQ town: {WHITE}{TOWN}": "{BLACK}본사 마을: {WHITE}{TOWN}",
    "{BLACK}Valid towns: {WHITE}{RAW_STRING}": "{BLACK}유효한 마을: {WHITE}{RAW_STRING}",
    "{BLACK}Industries owned: {WHITE}{RAW_STRING}":
        "{BLACK}소유한 산업 시설: {WHITE}{RAW_STRING}",
    "{BLACK}This is a GS text. {WHITE}Click me for the town story page. {BLACK}Here is some more text.":
        "{BLACK}이것은 GS 텍스트입니다. {WHITE}마을 이야기 페이지를 보려면 클릭하세요. {BLACK}더 많은 텍스트가 있습니다.",
    "Owner: {RAW_STRING}": "소유주: {RAW_STRING}",
    "{BLACK}Deliveries to this industry will contribute to town growth and/or happiness":
        "{BLACK}이 산업 시설로의 배송은 마을 성장 및/또는 행복에 기여합니다",
    "{INDUSTRY} increases production!": "{INDUSTRY}가 생산량을 늘립니다!",
}

AR = {
    "Hello {COMPANY}!{}{}You are playing a game with CIRS test GS{}{}Git version of this GS is {NUM}":
        "مرحبًا {COMPANY}!{}{}أنت تلعب لعبة باستخدام نص GS تجريبي لـ CIRS{}{}إصدار Git لهذا الـ GS هو {NUM}",
    "{BLUE}Cabbage": "{BLUE}كرنب",
    "happy": "سعيد",
    "unhappy": "غير سعيد",
    "Town is {STRING}{}{}To find out more about this town (including growth and happiness requirements), open the Story Book, and find the page for {TOWN}":
        "المدينة هي {STRING}{}{}لمعرفة المزيد عن هذه المدينة (بما في ذلك متطلبات النمو والسعادة)، افتح كتاب القصة، وابحث عن الصفحة الخاصة بـ {TOWN}",
    "{BLACK}Note that this won't refresh currently unless Grind is turned off and on in GS settings":
        "{BLACK}لاحظ أنه لن يتم التحديث حاليًا ما لم يتم إيقاف تشغيل الطحن وتشغيله في إعدادات GS",
    "{BLACK}Random word (test): {WHITE}{RAW_STRING}":
        "{BLACK}كلمة عشوائية (اختبار): {WHITE}{RAW_STRING}",
    "{BLACK}Current growth rate: {WHITE}{RAW_STRING}":
        "{BLACK}معدل النمو الحالي: {WHITE}{RAW_STRING}",
    "{YELLOW}Required cargos for growth": "{YELLOW}الشحنات المطلوبة للنمو",
    "{YELLOW}Required cargos for happiness": "{YELLOW}الشحنات المطلوبة للسعادة",
    "{BLACK}Supplied: {WHITE}{CARGO_LONG}": "{BLACK}تم التوريد: {WHITE}{CARGO_LONG}",
    "{BLACK}--- Town industries --- {}": "{BLACK}--- صناعات المدينة --- {}",
    "{BLACK}Required cargo supplied last month": "{BLACK}الشحنة المطلوبة التي تم توريدها الشهر الماضي",
    "{BLACK}Cargo produced last month": "{BLACK}الشحنة المنتجة الشهر الماضي",
    "{BLACK}Production (permanent) increase history (last 10 events)":
        "{BLACK}سجل الزيادة (الدائمة) في الإنتاج (آخر 10 أحداث)",
    "{WHITE}- this industry has never permanently increased production":
        "{WHITE}- هذه الصناعة لم تزد إنتاجها بشكل دائم قط",
    "{BLACK}Current production level: {WHITE}{NUM}":
        "{BLACK}مستوى الإنتاج الحالي: {WHITE}{NUM}",
    "{BLACK}Name: {WHITE}{RAW_STRING}": "{BLACK}الاسم: {WHITE}{RAW_STRING}",
    "{BLACK}Type: {WHITE}{RAW_STRING}": "{BLACK}النوع: {WHITE}{RAW_STRING}",
    "{BLACK}HQ town: {WHITE}{TOWN}": "{BLACK}مدينة المقر: {WHITE}{TOWN}",
    "{BLACK}Valid towns: {WHITE}{RAW_STRING}": "{BLACK}المدن الصالحة: {WHITE}{RAW_STRING}",
    "{BLACK}Industries owned: {WHITE}{RAW_STRING}":
        "{BLACK}الصناعات المملوكة: {WHITE}{RAW_STRING}",
    "{BLACK}This is a GS text. {WHITE}Click me for the town story page. {BLACK}Here is some more text.":
        "{BLACK}هذا نص خاص بـ GS. {WHITE}انقر علي للانتقال إلى صفحة قصة المدينة. {BLACK}إليك المزيد من النص.",
    "Owner: {RAW_STRING}": "المالك: {RAW_STRING}",
    "{BLACK}Deliveries to this industry will contribute to town growth and/or happiness":
        "{BLACK}التسليمات إلى هذه الصناعة تساهم في نمو المدينة و/أو سعادتها",
    "{INDUSTRY} increases production!": "{INDUSTRY} يزيد الإنتاج!",
}


def main():
    for lang, tr in (("korean", KO), ("arabic", AR)):
        path = os.path.join(ROOT, "src", "gs", "lang", f"{lang}.toml")
        n = T.translate_file(path, tr, GS_EN)
        print(f"{lang} gs: {n} values translated")


if __name__ == "__main__":
    main()
