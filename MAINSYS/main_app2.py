from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from syoki import MainApp
from Clock import TimeDisplayApp
from kivy.factory import Factory

# ファクトリにクラスを登録
Factory.register('MainApp', cls=MainApp)
Factory.register('TimeDisplayApp', cls=TimeDisplayApp)

kv = '''
BoxLayout:
    orientation: 'horizontal'

    MainApp:
        size_hint: 0.5, 1
        pos_hint: {'x': 0, 'y': 0}

    TimeDisplayApp
        size_hint: 0.5, 1
        pos_hint: {'x': 0, 'y': 0}
    

'''

class ExternalApp(App):
    def build(self):
        return Builder.load_string(kv)
    
if __name__ == '__main__':
    ExternalApp().run()
