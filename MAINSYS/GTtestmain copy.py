from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import csv
import japanize_kivy
import os

class MainApp(App):
    def build(self):
        layout = GridLayout(cols=1, spacing=10, padding=10)

        # タイトルのラベル
        title_label = Label(
            text="ほしい機能を選んでね",
            font_size=24,
            size_hint_y=None,
            height=50,
            halign="center",
        )

        button1 = Button(text="時間表示設定", size_hint=(None, None))
        button1.bind(on_press=self.launch_main2)

        button2 = Button(text="天気予報", size_hint=(None, None))
        button2.bind(on_press=self.launch_main3)

        button3 = Button(text="予定表示", size_hint=(None, None))
        button3.bind(on_press=self.launch_main4)

        button4 = Button(text="背景設定", size_hint=(None, None))
        button4.bind(on_press=self.launch_main5)

        button5 = Button(text="確定", size_hint=(None, None))
        button5.bind(on_press=self.launch_main6)

        layout.add_widget(Label())  # 上部の余白用
        layout.add_widget(title_label)
        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        layout.add_widget(button4)
        layout.add_widget(button5)

        # 背景の色をCSVファイルから読み込んで設定
        self.bg_color = Color(0, 0, 0, 1)  # デフォルトの背景色（RGBA形式で黒）
        self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)

        layout.canvas.before.add(self.bg_color)
        layout.canvas.before.add(self.bg_rect)

        # ウィンドウサイズ変更時に背景サイズを調整
        layout.bind(size=self.adjust_background_size)

        # 背景画像を設定
        self.set_background_image()

        return layout

    def adjust_background_size(self, instance, value):
        # 背景のサイズをウィンドウサイズに合わせて調整
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def launch_main2(self, instance):
        # main2.pyを実行
        os.system("python button_clock.py")

    def launch_main3(self, instance):
        # main3.pyを実行
        os.system("python weather2.py")
        os.system("python weathersearch.py")

    def launch_main4(self, instance):
        # main3.pyを実行
        os.system("python Calendar.py")

    def launch_main5(self, instance):
        # main3.pyを実行
        os.system("python haikei.py")

    def launch_main6(self, instance):
        # main3.pyを実行
        os.system("python MAINSYS/teshaikei.py")

    def on_start(self):
        # CSVファイルから背景色と文字の色を取得
        background_color, title_color, subtitle_color = self.get_colors_from_csv("MAINSYS\CSV\color_settings.csv")
        self.set_background_color(background_color)
        self.set_text_color(title_color, subtitle_color)
        print("背景色:", background_color)

    def get_colors_from_csv(self, csv_file):
        background_color = (0, 0, 0, 1)  # デフォルトの背景色（RGBA形式で黒）
        title_color = (1, 1, 1, 1)  # デフォルトのタイトル文字色（RGBA形式で白）
        subtitle_color = (1, 1, 1, 1)  # デフォルトのサブタイトル文字色（RGBA形式で白）

        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            # 1行目をスキップ
            next(reader)
            for row in reader:
                try:
                    background_color = (float(row[0]), float(row[1]), float(row[2]), float(row[3]))
                    if len(row) > 4:  # CSVファイルにタイトルの色情報が含まれているか確認
                        title_color = (float(row[4]), float(row[5]), float(row[6]), float(row[7]))
                    if len(row) > 8:  # CSVファイルにサブタイトルの色情報が含まれているか確認
                        subtitle_color = (float(row[8]), float(row[9]), float(row[10]), float(row[11]))
                    break  # 最初の行の値を使用
                except ValueError:
                    pass
        return background_color, title_color, subtitle_color

    def set_background_color(self, color):
        self.bg_color.rgba = color

    def set_text_color(self, title_color, subtitle_color):
        # タイトルとサブタイトルの文字色を変更
        for widget in self.root.walk(restrict=True):
            if isinstance(widget, Label):
                widget.color = title_color

    def set_background_image(self):
        # 背景画像のパスを取得
        background_image_path = self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv")
        if background_image_path:
            self.bg_rect.source = background_image_path

    def get_background_image_path(self, csv_file):
        # 背景画像のパスをCSVファイルから取得
        background_image_path = None
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0:
                        background_image_path = row[0]
                        break  # 最初の行の値を使用
        except FileNotFoundError:
            pass
        return background_image_path

if __name__ == "__main__":
    MainApp().run()
