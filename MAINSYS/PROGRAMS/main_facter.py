import csv
import os
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from WEATHERS.oneday_weather import WeatherApp
from onoD_calendar import CalendarApp

# 天気情報：WeatherApp
# 予定情報：CalendarApp
# 時計：App
class MainDisplayApp(App):
    
    def build(self):
        # レイアウトのインスタンスを作成
        self.layout = FloatLayout()
        
        self.background_color = [1, 1, 1, 1]  # デフォルトは白い背景

        bgopt = self.loadhaikei()
        # 背景の色と画像のパスを取得
        background_color, background_image_path = self.get_background_settings(bgopt)
        
        # 背景の色を設定
        with self.layout.canvas.before:
            Color(*background_color)
            self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)

        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.load_background_image(background_image_path)
        
        # ウィンドウのサイズ変更時に呼び出す関数を設定
        self.layout.bind(size=self.on_size)

        # calenderApp と WeatherApp のインスタンスを作成
        weather_app = WeatherApp()
        calender_app = CalendarApp()

        # 各アプリのレイアウトを作成
        weather_layout = weather_app.build()
        calendar_layout = calender_app.build()

        # 天気アプリの座標を読み込み
        posrow = 1 
        x, y = self.load_button_position(posrow)
        weather_layout.pos = (x, y)

        # 予定アプリの座標を読み込み
        posrow = 2
        x, y = self.load_button_position(posrow)
        calendar_layout.pos = (x, y)

        # 設定ボタンの生成
        button = Button(text="設定", size_hint=(None, None), pos_hint={'top': 1})
        button.bind(on_press=self.on_settings_button_press)
        
        self.layout.add_widget(button)
        self.layout.add_widget(weather_layout)
        self.layout.add_widget(calendar_layout)

        return self.layout
    

    # 設定ボタンが押されたときの処理
    def on_settings_button_press(self, instance):
        os.system("python PROGRAMS\settings.py")


    def get_background_settings(self,bgopt):
        # selected_backgrounds.csvから背景画像のパスを取得
        if bgopt == 1:
            background_image_path = self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv")
            if background_image_path:
                return (1, 1, 1, 1), background_image_path
        else:
        # selected_backgrounds.csvがない場合はcolor_settings.csvから背景色を取得
            background_color = self.get_background_color("MAINSYS\CSV\color_settings.csv")
            return background_color, None


    def get_background_image_path(self, csv_file):
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0:
                        background_image_path = row[0]
                        return background_image_path
        except FileNotFoundError:
            pass
        return None
    

    def get_background_color(self, csv_file):
        # color_settings.csvから背景色を取得
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # ヘッダー行をスキップ
                row = next(reader, None)
                if row:
                    background_color = (float(row[0]), float(row[1]), float(row[2]), float(row[3]))
                else:
                    background_color = (1, 1, 1, 1)  # デフォルト値
        except (FileNotFoundError, ValueError, IndexError):
            # ファイルが存在しない、不正な値、またはインデックスエラーが発生した場合はデフォルト値を返す
            background_color = (1, 1, 1, 1)
        return background_color
    
    def load_background_image(self, background_image_path):
        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.background_image = Rectangle(pos=self.layout.pos, size=self.layout.size, source=background_image_path)

    def on_size(self, instance, value):
        print("on_sizeメソッドが呼ばれました。")
        # ウィンドウサイズが変更されたときに呼び出される関数
        self.update_background_size()
        self.load_background_image(self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv"))

    def update_background_size(self):
        # 背景のサイズをウィンドウのサイズに合わせる
        self.background_rect.size = self.layout.size
    
    # CSVファイルからアプリの座標を取得するメソッド
    def load_button_position(self,row):
        filename = 'MAINSYS\CSV\move.csv'
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            button_pos_x = data[row][0]
            button_pos_y = data[row][1]

        return button_pos_x,button_pos_y
    
    def loadhaikei(self):
        filename = 'MAINSYS\CSV\onoD_opt.csv'
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[4][1]

        return optdata

if __name__ == '__main__':
    MainDisplayApp().run() 
