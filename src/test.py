from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from pathlib import Path


class A(App):
    def build(self):
        LabelBase.register(
            "JP", fn_regular=str(Path("assets/fonts/NotoSansJP-ExtraLight.ttf"))
        )
        return Label(text="こんにちは 世界", font_name="JP", font_size="32sp")


A().run()
