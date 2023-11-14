from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
import csv
import subprocess
import time
import os.path
import japanize_kivy

class RunningTask:
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            print("タスクが実行中...")
            time.sleep(1)

    def stop(self):
        self.running = False

class ButtonMoverApp(App):
    def build(self):
        # ウィンドウを作成
        self.layout = FloatLayout()

        # ボタンリスト
        self.buttons = []  # ここで初期化
        self.background_color = [1, 1, 1, 1]  # デフォルトは白い背景

        # 背景色と文字色の設定を読み込む
        self.load_color_settings()

        # selected_backgrounds.csvから背景画像のパスを取得
        background_image_path = self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv")

        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.background_image = Rectangle(pos=self.layout.pos, size=self.layout.size, source=background_image_path)

        # ボタンの名前と初期位置
        button_info = [
            {"name": "時間表示設定", "pos": (50, 100)},
            {"name": "天気予報", "pos": (200, 100)},
            {"name": "予定表示", "pos": (350, 100)},
            {"name": "追加", "pos": (500, 100)},
        ]

        for info in button_info:
            # ボタンを作成
            button = Button(text=info["name"])
            button.size_hint = (None, None)
            button.size = (100, 50)
            button.pos = info["pos"]

            # ボタンが移動したときのイベントを追加
            button.bind(on_touch_move=self.on_button_move)

            # ボタンの背景色と文字色を設定
            button.background_color = self.background_color
            button.color = [0, 0, 0, 1]  # デフォルトは黒い文字

            # ボタンをレイアウトに追加
            self.layout.add_widget(button)

            # ボタンをリストに追加
            self.buttons.append(button)  # ここで追加

        # 確定ボタンを作成
        confirm_button = Button(text="確定", size_hint=(None, None), size=(100, 50), pos=(self.layout.width - 100, 0))
        confirm_button.bind(on_press=self.on_confirm_button_press)
        self.layout.add_widget(confirm_button)

        # ウィンドウのサイズ変更時に呼び出す関数を設定
        self.layout.bind(size=self.on_size)

        return self.layout

    def on_button_move(self, instance, touch):
        # ボタンがタッチされ、移動したときに呼ばれるメソッド
        if instance.collide_point(*touch.pos):
            instance.pos = (touch.x - instance.width / 2, touch.y - instance.height / 2)

    def on_stop(self):
        # アプリケーションが終了するときに呼ばれるメソッド
        self.save_button_positions()

    def save_button_positions(self):
        # 各ボタンの座標をCSVファイルに保存するメソッド
        for button in self.buttons:
            button_pos = button.pos
            filename = f'{button.text.lower()}_position.csv'
            with open(filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['x', 'y'])
                csv_writer.writerow([button_pos[0], button_pos[1]])

    def on_confirm_button_press(self, instance):
        # 確定ボタンが押下されたときの処理
        self.save_button_positions()
        # button_loader.py を実行
        subprocess.Popen(["python", "MAINSYS/botton_loader.py"])
        App.get_running_app().stop()

    def load_color_settings(self):
        # 色設定を読み込むメソッド
        try:
            with open('MAINSYS/CSV/color_settings.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile)

                # ヘッダー行を読み飛ばす
                header = next(csv_reader)

                row = next(csv_reader)  # 次の行を読み込む
                print("読み込んだ色の値:", row)

                self.background_color = [float(value) for value in row[:4]]

                # 背景色を設定
                self.layout.canvas.before.clear()
                with self.layout.canvas.before:
                    Color(*self.background_color)
                    Rectangle(pos=self.layout.pos, size=self.layout.size)

                # ボタンの背景色を設定
                for button in self.buttons:
                    button.background_color = self.background_color

        except FileNotFoundError:
            print("color_settings.csv が見つかりません。デフォルトの色を使用します。")

    def get_background_image_path(self, csv_file):
        try:
            if os.path.isfile(csv_file):
                with open(csv_file, "r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) > 0:
                            background_image_path = row[0]
                            return background_image_path
        except FileNotFoundError:
            pass
        return None

    def on_size(self, instance, value):
        print("on_sizeメソッドが呼ばれました。")
        # ウィンドウサイズが変更されたときに呼び出される関数
        self.load_color_settings()  # 色を再読み込みする
        background_image_path = self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv")

        # 背景画像を設定
        if background_image_path:
            if not hasattr(self, 'background_image'):
                with self.layout.canvas.before:
                    self.background_image = Rectangle(pos=self.layout.pos, size=self.layout.size, source=background_image_path)
            else:
                self.background_image.source = background_image_path

if __name__ == '__main__':
    # アプリケーションを起動
    ButtonMoverApp().run()
