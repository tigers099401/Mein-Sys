from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
import csv
import os
import japanize_kivy

class ButtonLoaderApp(App):
    def build(self):
        # ウィンドウを作成
        layout = FloatLayout()

        # 背景の色と画像のパスを取得
        background_color, background_image_path = self.get_background_settings()

        # 背景の色を設定
        with layout.canvas.before:
            Color(*background_color)
            self.background_rect = Rectangle(pos=layout.pos, size=layout.size)

        # 背景画像を設定
        if background_image_path:
            with layout.canvas.before:
                self.background_image = Rectangle(pos=layout.pos, size=layout.size, source=background_image_path)

        # ボタンの情報
        button_info = [
            {"name": "時間表示設定", "pos": (50, 100)},
            {"name": "天気予報", "pos": (200, 100)},
            {"name": "予定表示", "pos": (350, 100)},
            {"name": "追加", "pos": (500, 100)},
        ]

        # ボタンリスト
        self.buttons = []

        for info in button_info:
            # CSVファイルからボタンの座標を取得
            button_pos = self.load_button_position(info["name"])

            # ボタンを作成
            button = Button(text=f'{info["name"]}')
            button.size_hint = (None, None)
            button.size = (100, 50)
            button.pos = button_pos

            # ボタンをレイアウトに追加
            layout.add_widget(button)

            # ボタンをリストに追加
            self.buttons.append(button)

            # ボタンが押下されたときのイベントを追加
            button.bind(on_press=self.on_button_press)

        # ウィンドウのサイズ変更時に呼び出す関数を設定
        layout.bind(size=self.on_size)

        return layout
    
    def on_button_press(self, instance):
        # ボタンが押下されたときの処理
        if instance.text == "時間表示設定":
            # 指定のファイルを実行する
            os.system("python .\Clock.py")

        if instance.text == "天気予報":
            # 指定のファイルを実行する
            os.system("python MAINSYS\天気機能のpathを入力してね")

        if instance.text == "予定表示":
            # 指定のファイルを実行する
            os.system("python MAINSYS\予定表示のpathを入力してね")

        if instance.text == "追加":
            # 指定のファイルを実行する
            os.system("python MAINSYS\追加機能のpathを入力してね")

        else:
            print("ドンマイ")

    def get_background_settings(self):
        # selected_backgrounds.csvから背景画像のパスを取得
        background_image_path = self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv")
        if background_image_path:
            return (1, 1, 1, 1), background_image_path

        # selected_backgrounds.csvがない場合はcolor_settings.csvから背景色を取得
        background_color = self.get_background_color("MAINSYS/CSV/color_settings.csv")
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

    def load_button_position(self, button_name):
        # CSVファイルからボタンの座標を取得するメソッド
        try:
            filename = f'{button_name.lower()}_position.csv'
            with open(filename, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header
                # Check if there are rows in the CSV file
                row = next(csv_reader, None)
                if row:
                    button_pos = [float(row[0]), float(row[1])]
                else:
                    # If there are no rows, use default position
                    button_pos = (100, 100)
        except (FileNotFoundError, ValueError, IndexError):
            # Handle file not found or invalid data gracefully
            button_pos = (100, 100)

        return button_pos

    def on_size(self, instance, value):
        # ウィンドウサイズが変更されたときに呼び出される関数
        self.background_rect.size = instance.size
        if hasattr(self, 'background_image'):
            self.background_image.size = instance.size

if __name__ == '__main__':
    # 別のアプリケーションで座標を読み込み、ボタンを配置
    ButtonLoaderApp().run()
