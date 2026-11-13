"""Restore the 6 mis-translated Spanish GS test/story strings to their English
source. They are debug strings; the AI pass produced translations of the
WRONG source key (broken placeholders). English = correct placeholders."""
import io

PATH = "src/gs/lang/spanish.toml"
with open(PATH, encoding="utf-8") as f:
    lines = f.read().split("\n")

fixes = {
    32: 'base = "{BLACK}Random word (test): {WHITE}{RAW_STRING}"',
    44: 'base = "{BLACK}Supplied: {WHITE}{CARGO_LONG}"',
    50: 'base = "{BLACK}Required cargo supplied last month"',
    104: 'base = "{BLACK}Random word (test): {WHITE}{RAW_STRING}"',
    116: 'base = "{BLACK}Valid towns: {WHITE}{RAW_STRING}"',
    122: 'base = "{BLACK}This is a GS text. {WHITE}Click me for the town story page. {BLACK}Here is some more text."',
}
for ln, val in fixes.items():
    # ln is 1-indexed
    assert lines[ln - 1].startswith('base = "'), f"unexpected line {ln}: {lines[ln-1]!r}"
    lines[ln - 1] = val

with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(lines))
print("fixed", len(fixes), "Spanish GS test strings")
