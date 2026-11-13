#!/usr/bin/env python3
import importlib.util, json, io, os
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
lm = p.lang_map(); extras = p.extra_files(lm)
out = io.StringIO()
def vals(file):
    return p.leaves(p.load(R/file))
def show(langs, file, keys):
    out.write("=== " + file + " ===\n")
    for l in langs:
        try: v = vals(file.replace("<L>", l))
        except Exception as e: out.write("  " + l + " ERR " + str(e) + "\n"); continue
        for k in keys:
            if k in v: out.write("  " + l + " | " + k + " = " + v[k] + "\n")
show(["croatian","serbian","slovak","czech","polish"], "src/docs/extra_strings_<L>.toml", ["CARGO_INFO_PLANT_AND_MACHINERY.base"])
show(["danish","norwegian_bokmal","swedish","german","dutch"], "src/grf/lang/<L>.toml", ["STR_CARGO_AMMONIA_AND_NITRIC_PRODUCTS.name"])
show(["traditional_chinese","simplified_chinese","japanese"], "src/docs/extra_strings_<L>.toml", ["CARGO_INFO_WOOD_PULP.base"])
# zhant native-name keys
v = vals("src/docs/lang/traditional_chinese.toml")
out.write("=== traditional_chinese docs lang native names ===\n")
for k in sorted(v):
    if k.startswith("DOC_TRANS_LANG"): out.write("  " + k + " = " + v[k] + "\n")
# Indonesian station siblings
out.write("=== Indonesian station names vs siblings ===\n")
for l in ["indonesian","malay","dutch","german","japanese","korean","simplified_chinese","spanish","french"]:
    f = "src/grf/lang/" + l + ".toml"
    if not os.path.exists(R/f): continue
    v = vals(f)
    ks = [k for k in v if k.startswith("STR_STATION_") and k.endswith(".base")]
    picks = {k:v[k] for k in ks if k in ["STR_STATION_FACTORY.base","STR_STATION_WORKS.base","STR_STATION_MILL.base","STR_STATION_PLANT.base","STR_STATION_HEAVY_INDUSTRY_2.base"]}
    out.write("  " + l + " " + json.dumps(picks, ensure_ascii=False) + "\n")
open("tools/_i18n_round3_patch_data.txt","w",encoding="utf-8").write(out.getvalue())
print("wrote", len(out.getvalue()), "chars")
