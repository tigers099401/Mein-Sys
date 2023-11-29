import csv

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from WEATHERS.oneday_weather import WeatherApp
#from PROGRAMS.calendar import CalendarApp



# 天気情報：WeatherApp
# 予定情報：CalendarApp
# 時計：App
class MainDisplayApp(App):
    def load_button_position(self,row):
        # CSVファイルからアプリの座標を取得するメソッド

        filename = 'CSV\move.csv'
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            button_pos_x = data[row][0]
            button_pos_y = data[row][1]

        return button_pos_x,button_pos_y
    
    def build(self):
        # レイアウトのインスタンスを作成
        layout = FloatLayout()
        button = Button(text="設定", size_hint=(None, None), pos_hint={'top': 1})
        layout.add_widget(button)


        # calenderApp と WeatherApp のインスタンスを作成
        weather_app = WeatherApp()
        #calender_app = CalendarApp()

        # 各アプリのレイアウトを作成
        weather_layout = weather_app.build()
        #calendar_layout = calender_app.build()

        #天気アプリの座標を読み込み
        posrow = 1 
        x, y = self.load_button_position(posrow)
        weather_layout.pos = (x, y)

        #予定アプリの座標を読み込み
        posrow = 2
        x, y = self.load_button_position(posrow)
        #calendar_layout.pos = (x, y)

        # レイアウトに各アプリの表示部分を追加
        layout.add_widget(weather_layout)
        #layout.add_widget(calendar_layout)

        return layout
    
    
if __name__ == '__main__':
    MainDisplayApp().run() 