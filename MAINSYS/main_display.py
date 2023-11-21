# main_display.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

# TimeDisplayAppをimport
from time_display_app import TimeDisplayApp

# WeatherAppをimport
from onoD_1day_weather import WeatherApp

class MainDisplayApp(App):
    def build(self):
        # レイアウトのインスタンスを作成
        layout = BoxLayout(orientation='vertical')

        # TimeDisplayAppとWeatherAppのインスタンスを作成
        time_display_app = TimeDisplayApp()
        weather_app = WeatherApp()

        # 各アプリの表示部分を取得
        time_display_layout = time_display_app.build()
        weather_layout = weather_app.build()

        # レイアウトに各アプリの表示部分を追加
        layout.add_widget(time_display_layout)
        layout.add_widget(weather_layout)

        return layout

if __name__ == '__main__':
    MainDisplayApp().run()
