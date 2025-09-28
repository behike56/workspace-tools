from __future__ import annotations
import os
from typing import Dict, List, Tuple


def _list_files(dir_path: str, recursive: bool = False) -> List[str]:
    if recursive:
        names = []
        for root, _, files in os.walk(dir_path):
            for f in files:
                names.append(f)  # 同名比較は「ファイル名のみ」でOKならこれで十分
        return names
    else:
        return [
            f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))
        ]


def compare_filenames(
    dir_a: str,
    dir_b: str,
    *,
    recursive: bool = False,
    case_insensitive: bool = False,
) -> Dict[str, List[str]]:
    """
    2つのディレクトリの「ファイル名」を比較して、
    共通 / 片方のみ を返す。
    戻り値キー: common, only_a, only_b, total_a, total_b（いずれもソート済み）
    """
    a_files = _list_files(dir_a, recursive)
    b_files = _list_files(dir_b, recursive)

    if case_insensitive:
        a_set_map = {name.lower(): name for name in a_files}
        b_set_map = {name.lower(): name for name in b_files}
        aset = set(a_set_map.keys())
        bset = set(b_set_map.keys())
        common_keys = sorted(aset & bset)
        only_a_keys = sorted(aset - bset)
        only_b_keys = sorted(bset - aset)
        common = [a_set_map[k] for k in common_keys]
        only_a = [a_set_map[k] for k in only_a_keys]
        only_b = [b_set_map[k] for k in only_b_keys]
    else:
        aset = set(a_files)
        bset = set(b_files)
        common = sorted(aset & bset)
        only_a = sorted(aset - bset)
        only_b = sorted(bset - aset)

    return {
        "common": common,
        "only_a": only_a,
        "only_b": only_b,
        "total_a": sorted(a_files),
        "total_b": sorted(b_files),
    }
