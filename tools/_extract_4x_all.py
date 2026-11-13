"""Extract every 4.x (FIRS) language .lng file from the v4-maintenance-track
branch into tools/_4x_ref, so we can carry over translations for ALL languages.
"""
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(REPO, "tools", "_4x_ref")
os.makedirs(REF, exist_ok=True)

LANGS = [
    "afrikaans", "belarusian", "catalan", "croatian", "czech", "danish",
    "dutch", "english", "english_au", "english_us", "esperanto", "estonian",
    "finnish", "french", "gaelic", "galician", "german", "hungarian",
    "indonesian", "italian", "japanese", "korean", "latin", "luxembourgish",
    "norwegian_bokmal", "polish", "portuguese", "portuguese_BR", "romanian",
    "russian", "serbian", "simplified_chinese", "slovak", "spanish",
    "spanish_MX", "swedish", "tamil", "traditional_chinese", "turkish", "welsh",
]

saved = []
miss = []
for l in LANGS:
    r = subprocess.run(
        ["git", "show", f"upstream/v4-maintenance-track:src/lang/{l}.lng"],
        cwd=REPO, capture_output=True,
    )
    if r.returncode == 0 and r.stdout:
        open(os.path.join(REF, f"{l}.lng"), "wb").write(r.stdout)
        saved.append(l)
    else:
        miss.append(l)

print("saved:", len(saved))
print(", ".join(saved))
if miss:
    print("MISSING:", ", ".join(miss))
