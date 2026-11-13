"""Extract FIRS 4.x .lng reference translations from git history, version-aligned.

For each target language we find the commit that introduced the language file
and extract BOTH that file and english.lng from the *same* commit, because the
string IDs must line up between the English source and the translation. The
files are UTF-8 in git; some are double-encoded (Latin-1 bytes read as UTF-8),
which the build script repairs.
"""
import subprocess
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "_4x_ref")
os.makedirs(OUT, exist_ok=True)

ENGLISH_CANDIDATES = [
    "lang/english.lng",
    "src/lang/english.lng",
    "src copy main/lang/english.lng",
]

CANDIDATES = {
    "german": ["lang/02.lng"],
    "french": ["lang/03.lng"],
    "spanish": ["lang/04.lng", "lang/spanish.lng"],
    "portuguese": ["lang/portuguese.lng"],
    "portuguese_br": ["lang/portuguese_BR.lng"],
    "korean": ["lang/korean.lng"],
}


def find_commit(path):
    out = subprocess.run(
        ["git", "log", "--all", "--diff-filter=A", "--format=%H", "--", path],
        cwd=ROOT, capture_output=True, text=True,
    )
    commits = [c for c in out.stdout.splitlines() if c.strip()]
    return commits[0] if commits else None


def git_show(commit, path):
    res = subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True,
    )
    if res.returncode != 0:
        return None
    return res.stdout


def main():
    for lang, paths in CANDIDATES.items():
        for p in paths:
            commit = find_commit(p)
            if not commit:
                continue
            data = git_show(commit, p)
            if not data:
                continue
            text = data.decode("utf-8")
            with open(os.path.join(OUT, f"{lang}.lng"), "w", encoding="utf-8") as f:
                f.write(text)
            print(f"OK   {lang:12s} <- {p}  ({len(text.splitlines())} lines)")
            # english from the same commit
            for ep in ENGLISH_CANDIDATES:
                en = git_show(commit, ep)
                if en:
                    etext = en.decode("utf-8")
                    with open(os.path.join(OUT, f"{lang}_en.lng"), "w", encoding="utf-8") as f:
                        f.write(etext)
                    print(f"     english (same commit) <- {ep}  ({len(etext.splitlines())} lines)")
                    break
            else:
                print(f"     (no english.lng at this commit)")
            break
        else:
            print(f"MISS {lang:12s}")


if __name__ == "__main__":
    main()
