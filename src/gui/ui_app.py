from __future__ import annotations
import os
from typing import Dict, List, Tuple
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.properties import StringProperty, ListProperty, DictProperty

from files.pdf_file_rename import rename_pdfs_in_directory
from files.file_rename import rename_files_with_prefix
from files.dir_compare import compare_filenames

PROJECT_ROOT = Path(__file__).parents[2]
FONT_DIR = PROJECT_ROOT / "assets" / "fonts"
KV_PATH = Path(__file__).with_name("ui.kv")  # 同ディレクトリのui.kv


class Root(BoxLayout):
    dir_path = StringProperty("")
    status = StringProperty("準備OK")
    result_files = ListProperty([])

    dir_a = StringProperty("")
    dir_b = StringProperty("")
    compare_view = StringProperty("common")  # "common" | "only_a" | "only_b"
    compare_result: DictProperty = DictProperty({})
    compare_list: ListProperty = ListProperty([])

    def set_status(self, msg: str) -> None:
        self.status = msg

    def _refresh_rv(self) -> None:
        rv = self.ids.get("rv")
        if rv is not None:
            rv.data = [{"text": f, "font_name": "JP"} for f in self.result_files]

    def on_kv_post(self, base_widget) -> None:
        # kv の読み込み後に初期反映
        self._refresh_rv()

    def on_result_files(self, *_args) -> None:
        # プロパティが更新されたら RecycleView に反映
        self._refresh_rv()

    def run_prefix(self) -> None:
        path = (self.dir_path or "").strip()
        if not path:
            self.set_status("ディレクトリを指定してください")
            return
        try:
            files = rename_files_with_prefix(path)
            self.result_files = files  # ← これで on_result_files が走る
            self.set_status(f"完了: {len(files)} 件")
        except Exception as e:
            self.set_status(f"エラー: {e!r}")

    def run_pdf(self) -> None:
        path = (self.dir_path or "").strip()
        if not path:
            self.set_status("ディレクトリを指定してください")
            return
        try:
            files = rename_pdfs_in_directory(path)
            self.result_files = files  # ← 同上
            self.set_status(f"完了: {len(files)} 件")
        except Exception as e:
            self.set_status(f"エラー: {e!r}")

    def _refresh_rv_compare(self) -> None:
        rv = self.ids.get("rv_compare")
        if rv is not None:
            rv.data = [{"text": f, "font_name": "JP"} for f in self.compare_list]

    def on_compare_view(self, *_):
        # 表示切替時にcompare_listを反映
        if not self.compare_result:
            self.compare_list = []
        else:
            self.compare_list = self.compare_result.get(self.compare_view, [])
        self._refresh_rv_compare()

    def run_compare(self) -> None:
        a = (self.dir_a or "").strip()
        b = (self.dir_b or "").strip()
        if not a or not b:
            self.status = "A/B 両方のディレクトリを指定してください"
            return
        try:
            res = compare_filenames(a, b, recursive=False, case_insensitive=False)
            self.compare_result = res
            # 現在のビューに合わせて表示
            self.compare_list = res.get(self.compare_view, [])
            # 件数の概要をステータスに表示
            msg = f"比較完了 | 共通:{len(res['common'])} Aのみ:{len(res['only_a'])} Bのみ:{len(res['only_b'])}"
            self.status = msg
            self._refresh_rv_compare()
        except Exception as e:
            self.status = f"エラー: {e!r}"


class RenameApp(App):
    def build(self):
        Window.size = (900, 600)
        font_regular = FONT_DIR / "NotoSansJP-ExtraLight.ttf"
        if not font_regular.exists():
            raise FileNotFoundError(f"Font not found: {font_regular}")
        LabelBase.register(name="JP", fn_regular=str(font_regular))
        Builder.load_file(str(KV_PATH))
        return Root()
