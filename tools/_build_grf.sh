#!/usr/bin/env bash
set -u
PY="C:/Users/Maicarons/AppData/Local/Python/bin/python.exe"
# Makefile passes empty TEST_INDUSTRY / NO_MP: '' ''. A non-empty first arg
# makes render_nml.py build ONLY that industry, leaving spritesets undefined.
A1="" ; A2=""
step() { echo "=== $1 ==="; }
step "[1/5] render_lang.py  (grf .lng + gs .txt)"
"$PY" src/render_lang.py "$A1" "$A2" || { echo FAIL1; exit 1; }
step "[2/5] render_nml.py"
"$PY" src/render_nml.py "$A1" "$A2" || { echo FAIL2; exit 1; }
step "[3/5] render_graphics.py"
"$PY" src/render_graphics.py "$A1" "$A2" || echo "WARN render_graphics"
step "[4/5] render_docs.py"
"$PY" src/render_docs.py "$A1" "$A2" || echo "WARN render_docs"
step "[5/5] nmlc compile"
rm -f generated/cirs.grf
nmlc -c -l generated/lang --verbosity=4 --no-optimisation-warning --list-unused-strings --grf=generated/cirs.grf generated/cirs.nml > /tmp/cirs_nmlc.log 2>&1
RC=$?
echo "nmlc exit=$RC  (log lines: $(wc -l < /tmp/cirs_nmlc.log))"
tail -30 /tmp/cirs_nmlc.log
if [ "$RC" -ne 0 ]; then echo FAIL5; exit 1; fi
step "BUILD DONE"
stat -c "%y %s %n" generated/cirs.grf generated/cirs.nml
echo "=== lang files ==="; ls generated/lang/*.lng | wc -l
