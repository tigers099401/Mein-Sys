from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
import requests
import japanize_kivy
import csv
import os

class WeatherApp(App):
    def load_csv(self):

        file_path = "MAINSYS/CSV/onoD_opt.csv"
        # CSVファイルを読み込む
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        # 必要な部分を変更
        url_data = data[2][1] 

        # 新しいCSVファイルとして書き出す
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        return url_data

    def build(self):
        #url_data = self.load_csv()
        #self.api_url = url_data
        self.api_url = "https://api.open-meteo.com/v1/forecast?latitude=34.7&longitude=135.5&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=Asia%2FTokyo"
        self.data = None

        # ルート レイアウトを作成
        self.root_layout = BoxLayout(orientation='vertical')

        # 天気情報のための BoxLayout を作成
        self.weather_layout = BoxLayout()
        self.root_layout.add_widget(self.weather_layout)

        # 初回のデータ取得と定期的な更新をスケジュール
        self.update_weather_data()
        Clock.schedule_interval(lambda dt: self.update_weather_data(), 3600)  # 1時間ごとに更新

        return self.root_layout

    def update_weather_data(self, dt=None):
        response = requests.get(self.api_url)
        data = response.json()
        self.data = data
        self.update_display(1)  # 初回は1日分のデータを表示

    def update_display(self, days):
        if self.data:
            daily_data = self.data.get("daily", {})
            time = daily_data.get("time", [])
            max_temperature = daily_data.get("temperature_2m_max", [])
            min_temperature = daily_data.get("temperature_2m_min", [])
            weather_code = daily_data.get("weather_code", [])

            if time and max_temperature and min_temperature and weather_code:
                weekly_data = []  # 指定された日数分のデータを格納するリスト
                for i in range(min(days, len(time))):  # days とデータの個数の小さい方を使用
                    day_data = {
                        'day': time[i],
                        'max_temp': max_temperature[i],
                        'min_temp': min_temperature[i],
                        'weather': get_weather_meaning(weather_code[i])
                    }
                    weekly_data.append(day_data)

                # 指定された日数分のデータを更新
                self.update_weekly_data(weekly_data)

    def update_weekly_data(self, weekly_data):
        # 指定された日数分のデータをレイアウトに反映
        self.weather_layout.clear_widgets()
        for day_data in weekly_data:
            day_layout = BoxLayout(orientation='vertical', spacing=5)
            dLabel1 = Label()
            title_label = Label(text="天候情報",font_size='25sp',color=(1, 0, 0, 1))
            day_label = Label(text=day_data['day'],font_size='20sp')
            max_temp_label = Label(text=f"最高気温: {day_data['max_temp']}°C",font_size='20sp')
            min_temp_label = Label(text=f"最低気温: {day_data['min_temp']}°C",font_size='20sp')
            weather_label = Label(text=f"天気: {day_data['weather']}",font_size='20sp')
            dLabel2 = Label()
            # 天気に対応する画像を表示
            weather_image = Image(source=get_weather_image(day_data['weather']))
            day_layout.add_widget(title_label)
            day_layout.add_widget(dLabel1)
            day_layout.add_widget(day_label)
            day_layout.add_widget(max_temp_label)
            day_layout.add_widget(min_temp_label)
            day_layout.add_widget(weather_label)
            day_layout.add_widget(weather_image)
            day_layout.add_widget(dLabel2)
            self.weather_layout.add_widget(day_layout)

def get_weather_meaning(weather_code):
    if 0 <= weather_code <= 3:
        return "00 - 03 晴れ"
    elif 4 <= weather_code <= 9:
        return "04 - 09 霞、ほこり、砂または煙"
    elif 20 <= weather_code <= 29:
        return "20 - 29 降水、霧、氷霧、または雷雨"
    elif 30 <= weather_code <= 35:
        return "30 - 35 塵嵐、砂嵐"
    elif 36 <= weather_code <= 39:
        return "36 - 39 吹雪または吹雪"
    elif 40 <= weather_code <= 49:
        return "40 - 49 霧または氷"
    elif 40 <= weather_code <= 49:
        return "40 - 49 霧または氷霧"
    elif 50 <= weather_code <= 59:
        return "50 - 59 霧雨"
    elif 60 <= weather_code <= 69:
        return "60 - 69 雨"
    elif 70 <= weather_code <= 79:
        return "70 - 79 にわか降水（シャワーではない）"
    elif 80 <= weather_code <= 99:
        return "80 - 99 にわか降水、または現在または直近の雷雨"
    else:
        return "不明"

def get_weather_image(weather_meaning):
    # 仮の実装: 天気に応じて異なる画像を返す
    if '晴れ' in weather_meaning:
        return 'test/onoD/sun.png' #実施環境用にパスを変更してください
    elif '雨' in weather_meaning:
        return 'test/onoD/umbrella.png'
    elif '霞、ほこり、砂または煙' in weather_meaning:
        return 'test/onoD/umbrella.png'
    elif '降水、霧、氷霧、または雷雨' in weather_meaning:
        return 'test/onoD/umbrella.png'
    elif '塵嵐、砂嵐' in weather_meaning:
        return 'test/onoD/umbrella.png'
    elif '吹雪または吹雪' in weather_meaning:
        return 'test/onoD/umbrella.png'
    elif '霧または氷' in weather_meaning:
        return 'test/onoD/umbrella.png'
    elif '霧または氷霧' in weather_meaning:
        return 'test/onoD/umbrella.png'
    elif '霧雨' in weather_meaning:
        return 'test/onoD/umbrella.png'
    elif 'にわか降水（シャワーではない）' in weather_meaning:
        return 'test/onoD/umbrella.png'
    elif 'にわか降水、または現在または直近の雷雨' in weather_meaning:
        return 'test/onoD/umbrella.png'
    else:
        return 'test/onoD/umbrella.png'

if __name__ == '__main__':
    WeatherApp().run()