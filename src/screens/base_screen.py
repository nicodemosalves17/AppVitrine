from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class BaseScreen(Screen):
    pass

Builder.load_string("""
<BaseScreen>:
    canvas.before:
        Color:
            rgba: 1, 0.647, 0, 1  # #ffa500
        Rectangle:
            pos: self.pos
            size: self.size
""")