from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.lang import Builder
from syoki import MainApp
from kivy.factory import Factory

Factory.register('MainApp', cls=MainApp)
kv = '''
BoxLayout:
    orientation: 'horizontal'
    MainApp:
'''

class ExternalApp(App):
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    ExternalApp().run()