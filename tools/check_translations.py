#!/usr/bin/env python3
"""CIRS 翻译完整性校验。

校验内容：
1. 每个非英文语言文件与英文基准文件的键集合、键顺序完全一致；
2. 每条文本中的 NML 占位符（含 {} 换行标记）数量与顺序一致；
3. NewGRF 语言文件包含 GLOBAL_PRAGMA，且 grflangid 不重复；
4. 网页语言包与文档专用字符串保持同样的键集合。
"""

from __future__ import annotations

import re
import sys
import tomllib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_0-9]*)\}")


def load_toml(path: Path) -> dict:
    """读取 TOML 文件，统一使用二进制模式以正确处理 UTF-8。"""
    with path.open("rb") as fp:
        return tomllib.load(fp)


def get_keys(data: dict) -> list[str]:
    """返回参与翻译比对的键，GLOBAL_PRAGMA 是元数据不参与比对。"""
    return [key for key in data.keys() if key != "GLOBAL_PRAGMA"]


def placeholders(value: str) -> Counter:
    """提取文本中的占位符多重集合；{} 表示换行，同样参与计数。"""
    return Counter(PLACEHOLDER_RE.findall(value))


def check_file_pair(reference_path: Path, target_path: Path, errors: list[str]) -> None:
    """比对一组基准语言文件与目标语言文件的键、顺序与占位符。"""
    reference = load_toml(reference_path)
    target = load_toml(target_path)
    reference_keys = get_keys(reference)
    target_keys = get_keys(target)

    missing = [key for key in reference_keys if key not in target_keys]
    extra = [key for key in target_keys if key not in reference_keys]
    if missing:
        errors.append(f"{target_path}: 缺少键 {', '.join(missing[:8])}")
    if extra:
        errors.append(f"{target_path}: 多出键 {', '.join(extra[:8])}")
    if not missing and not extra and reference_keys != target_keys:
        errors.append(f"{target_path}: 键顺序与 {reference_path.name} 不一致")

    for key in reference_keys:
        if key not in target:
            continue
        reference_node = reference[key]
        target_node = target[key]
        if isinstance(reference_node, dict):
            if not isinstance(target_node, dict):
                errors.append(f"{target_path}: 键 {key} 应为表结构")
                continue
            for attribute, reference_value in reference_node.items():
                if attribute not in target_node:
                    errors.append(f"{target_path}: 键 {key} 缺少属性 {attribute}")
                    continue
                if not isinstance(reference_value, str):
                    continue
                target_value = str(target_node[attribute])
                if placeholders(reference_value) != placeholders(target_value):
                    errors.append(
                        f"{target_path}: 键 {key}.{attribute} 的占位符不一致 "
                        f"({placeholders(reference_value)} != {placeholders(target_value)})"
                    )
        elif isinstance(reference_node, str):
            target_value = str(target_node)
            if placeholders(reference_node) != placeholders(target_value):
                errors.append(
                    f"{target_path}: 键 {key} 的占位符不一致 "
                    f"({placeholders(reference_node)} != {placeholders(target_value)})"
                )


def check_grf_pragma(path: Path, data: dict, errors: list[str]) -> None:
    """检查非英文 NewGRF 语言文件的 GLOBAL_PRAGMA 与语言 ID。"""
    pragma = data.get("GLOBAL_PRAGMA")
    if not isinstance(pragma, dict):
        errors.append(f"{path}: 缺少 [GLOBAL_PRAGMA]")
        return
    if "grflangid" not in pragma:
        errors.append(f"{path}: GLOBAL_PRAGMA 缺少 grflangid")
    if "plural" not in pragma:
        errors.append(f"{path}: GLOBAL_PRAGMA 缺少 plural")


def check_lang_dir(kind: str, errors: list[str]) -> list[str]:
    """校验 src/grf/lang 或 src/gs/lang 目录，返回已检查的语言文件名。"""
    lang_dir = ROOT / "src" / kind / "lang"
    reference_path = lang_dir / "english.toml"
    if not reference_path.exists():
        errors.append(f"{reference_path}: 基准语言文件不存在")
        return []

    checked = []
    for target_path in sorted(lang_dir.glob("*.toml")):
        if target_path == reference_path:
            continue
        check_file_pair(reference_path, target_path, errors)
        target_data = load_toml(target_path)
        if kind == "grf":
            check_grf_pragma(target_path, target_data, errors)
        checked.append(target_path.name)
    return checked


def check_grf_lang_ids(errors: list[str]) -> None:
    """确保每种 NewGRF 语言的 grflangid 唯一，避免游戏内语言选择互相覆盖。"""
    seen: dict[str, str] = {}
    for path in sorted((ROOT / "src" / "grf" / "lang").glob("*.toml")):
        data = load_toml(path)
        pragma = data.get("GLOBAL_PRAGMA", {})
        language_id = pragma.get("grflangid")
        if not language_id:
            continue
        if language_id in seen:
            errors.append(
                f"{path}: grflangid {language_id} 与 {seen[language_id]} 重复"
            )
        seen[language_id] = path.name


def check_docs(errors: list[str]) -> tuple[list[str], list[str]]:
    """校验网页语言包和文档专用字符串目录。"""
    docs_dir = ROOT / "src" / "docs"
    lang_dir = docs_dir / "lang"
    reference_path = lang_dir / "english.toml"

    checked_langs = []
    for target_path in sorted(lang_dir.glob("*.toml")):
        if target_path == reference_path:
            continue
        check_file_pair(reference_path, target_path, errors)
        checked_langs.append(target_path.name)

    checked_extra = []
    extra_reference = docs_dir / "extra_strings.toml"
    for target_path in sorted(docs_dir.glob("extra_strings_*.toml")):
        check_file_pair(extra_reference, target_path, errors)
        checked_extra.append(target_path.name)

    return checked_langs, checked_extra


def main() -> int:
    """执行全部检查，返回进程退出码。"""
    errors: list[str] = []

    grf_langs = check_lang_dir("grf", errors)
    gs_langs = check_lang_dir("gs", errors)
    check_grf_lang_ids(errors)
    docs_langs, docs_extra = check_docs(errors)

    if errors:
        print("[TRANSLATIONS] FAILED")
        for error in errors:
            print("  - " + error)
        return 1

    print("[TRANSLATIONS] OK")
    print(f"  NewGRF languages: {', '.join(['english.toml'] + grf_langs)}")
    print(f"  GameScript languages: {', '.join(['english.toml'] + gs_langs)}")
    print(f"  Website languages: {', '.join(['english.toml'] + docs_langs)}")
    print(f"  Website extra strings: {', '.join(['extra_strings.toml'] + docs_extra)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
