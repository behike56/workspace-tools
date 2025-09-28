# src/gui/ui_app.py
from pathlib import Path
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase

from files.pdf_file_rename import rename_pdfs_in_directory
from files.file_rename import rename_files_with_prefix

PROJECT_ROOT = Path(__file__).parents[2]
FONT_DIR = PROJECT_ROOT / "assets" / "fonts"
KV_PATH = Path(__file__).with_name("ui.kv")  # 同ディレクトリのui.kv


class Root(BoxLayout):
    dir_path = StringProperty("")
    status = StringProperty("準備OK")
    result_files = ListProperty([])

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


class RenameApp(App):
    def build(self):
        Window.size = (900, 600)
        font_regular = FONT_DIR / "NotoSansJP-ExtraLight.ttf"
        if not font_regular.exists():
            raise FileNotFoundError(f"Font not found: {font_regular}")
        LabelBase.register(name="JP", fn_regular=str(font_regular))
        Builder.load_file(str(KV_PATH))
        return Root()
