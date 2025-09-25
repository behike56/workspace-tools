from pathlib import Path
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (
    ListProperty,
    StringProperty,
    NumericProperty,
    BooleanProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.lang import Builder
from kivy.core.window import Window


class SelectableRecycleBoxLayout(
    FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout
):
    """選択機能付きのレイアウト（標準レシピ）"""

    touch_deselect_last = False


class SelectableLabel(RecycleDataViewBehavior, Label):
    """各行のView。選択状態を保持して見た目を切り替える"""

    index = NumericProperty(0)
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            # 親レイアウトに「このindexを選択した」と通知
            self.parent.select_with_touch(self.index, touch)
            return True
        return False

    def apply_selection(self, rv, index, is_selected):
        # RecycleView側で選択が確定したときに呼ばれる
        self.selected = is_selected
        if is_selected:
            App.get_running_app().root.set_status(f"選択: {self.text}")


class Root(BoxLayout):
    """画面のルート。検索とリストの制御を担当"""

    query = StringProperty("")  # 検索テキスト
    status = StringProperty("準備OK")  # 下部ステータス
    sort_asc = BooleanProperty(True)  # ソート昇順/降順

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # サンプルデータ（任意の構造に置き換えOK）
        names = [
            ("Apple", "Fruit"),
            ("Avocado", "Fruit"),
            ("Banana", "Fruit"),
            ("Blueberry", "Fruit"),
            ("Cherry", "Fruit"),
            ("Cucumber", "Vegetable"),
            ("Daikon", "Vegetable"),
            ("Eggplant", "Vegetable"),
            ("Fig", "Fruit"),
            ("Grape", "Fruit"),
            ("Grapefruit", "Fruit"),
            ("Kiwi", "Fruit"),
            ("Lemon", "Fruit"),
            ("Lettuce", "Vegetable"),
            ("Mango", "Fruit"),
            ("Nectarine", "Fruit"),
            ("Onion", "Vegetable"),
            ("Orange", "Fruit"),
            ("Peach", "Fruit"),
            ("Pear", "Fruit"),
            ("Pepper", "Vegetable"),
            ("Pineapple", "Fruit"),
            ("Plum", "Fruit"),
            ("Potato", "Vegetable"),
            ("Spinach", "Vegetable"),
            ("Strawberry", "Fruit"),
            ("Tomato", "Vegetable"),
            ("Ume", "Fruit"),
            ("Watermelon", "Fruit"),
            ("Yam", "Vegetable"),
        ]
        self._all_items = [
            {"id": i + 1, "name": n, "category": c} for i, (n, c) in enumerate(names)
        ]
        # 入力の打鍵ごとに呼びすぎないようデバウンス
        self._filter_trigger = Clock.create_trigger(
            lambda dt: self._apply_filter(), 0.12
        )
        Clock.schedule_once(lambda dt: self._apply_filter(), 0)

    def on_query(self, *_):
        self._filter_trigger()

    def set_status(self, msg: str):
        self.status = msg

    def clear_query(self):
        self.query = ""

    def toggle_sort(self):
        self.sort_asc = not self.sort_asc
        self._apply_filter()

    def _apply_filter(self):
        """queryでフィルタ・ソートしてRecycleViewに反映"""
        q = (self.query or "").strip().lower()
        tokens = [t for t in q.split() if t]  # スペース区切りAND検索

        def hit(item):
            if not tokens:
                return True
            hay = f"{item['name']} {item['category']}".lower()
            return all(t in hay for t in tokens)

        filtered = [it for it in self._all_items if hit(it)]
        # ソート（名前で昇順/降順）
        filtered.sort(key=lambda x: x["name"], reverse=not self.sort_asc)

        # RecycleView用のdataに詰め替え
        # viewclass(SelectableLabel)が受け取るのは、少なくとも text と index
        data = [
            {"text": f"{it['name']} · {it['category']}", "index": i, "selected": False}
            for i, it in enumerate(filtered)
        ]
        self.ids.rv.data = data
        self.set_status(
            f"件数: {len(filtered)}（{'昇順' if self.sort_asc else '降順'}）"
        )


class SearchListApp(App):
    def build(self):
        # 画面サイズを固定して「出ているか」を目視しやすく
        Window.size = (900, 600)
        # src/main.py と同じディレクトリに ui.kv がある前提で明示的にロード
        kv_path = Path(__file__).with_name("ui.kv")
        Builder.load_file(str(kv_path))
        return Root()
