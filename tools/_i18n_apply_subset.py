#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _i18n_pipeline as p
subset = set(sys.argv[1:])
orig = p.lang_map
p.lang_map = lambda: {k: v for k, v in orig().items() if k == "english" or k in subset}
p.cmd_apply()
