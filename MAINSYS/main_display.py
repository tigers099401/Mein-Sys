# main_display.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from time_display_app import TimeDisplayApp
from onoD_1day_weather import WeatherApp

class MainDisplayApp(App):
    def build(self):
        time_display_app = TimeDisplayApp()
        time_display_app.build()  # TimeDisplayAppのbuildメソッドを呼び出すことでlayoutにアクセス
        weather_app = WeatherApp()
        
        # レイアウトの配置などは要件に応じて調整してください
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(time_display_app.layout)  # ここでlayoutを追加
        layout.add_widget(weather_app.root_layout)

        return layout

if __name__ == '__main__':
    MainDisplayApp().run()
