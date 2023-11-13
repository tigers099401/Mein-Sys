from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
import csv
import os
import japanize_kivy

class ButtonMoverApp(App):
    def build(self):
        # ウィンドウを作成
        self.layout = FloatLayout()

        # ボタンの名前と初期位置
        button_info = [
            {"name": "時間表示設定", "pos": (50, 100)},
            {"name": "天気予報", "pos": (200, 100)},
            {"name": "予定表示", "pos": (350, 100)},
            {"name": "追加", "pos": (500, 100)},
        ]

        # ボタンリスト
        self.buttons = []

        for info in button_info:
            # ボタンを作成
            button = Button(text=info["name"])
            button.size_hint = (None, None)
            button.size = (100, 50)
            button.pos = info["pos"]

            # ボタンが移動したときのイベントを追加
            button.bind(on_touch_move=self.on_button_move)

            # ボタンをレイアウトに追加
            self.layout.add_widget(button)

            # ボタンをリストに追加
            self.buttons.append(button)

            # 確定ボタンを作成
            confirm_button = Button(text="確定", size_hint=(None, None), size=(100, 50), pos=(self.layout.width - 100, 0))
            confirm_button.bind(on_press=self.on_confirm_button_press)
            self.layout.add_widget(confirm_button)

        # 初回の背景設定を行う
        self.apply_background_settings()

        return self.layout

    def apply_background_settings(self):
        # selected_backgrounds.csvから背景画像のパスを取得
        background_image_path = self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv")

        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.background_image = Rectangle(pos=self.layout.pos, size=self.layout.size, source=background_image_path)

        else:
            # selected_backgrounds.csvがない場合はcolor_settings.csvから背景色を取得
            background_color = self.get_background_color("MAINSYS/CSV/color_settings.csv")

            # 背景の色を設定
            with self.layout.canvas.before:
                Color(*background_color)
                self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)

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
        # 背景設定を更新
        self.apply_background_settings()
        # button_loader.py を実行
        os.system("python MAINSYS/botton_loader.py")

if __name__ == '__main__':
    # アプリケーションを起動
    ButtonMoverApp().run()
