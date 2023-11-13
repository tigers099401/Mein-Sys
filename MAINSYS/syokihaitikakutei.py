from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import csv
import japanize_kivy
import os

class DraggableButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return super(DraggableButton, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super(DraggableButton, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.center_x = touch.x
            self.center_y = touch.y
            self.on_button_move()  # ボタンが移動したときの処理を追加
            return True
        return super(DraggableButton, self).on_touch_move(touch)

    def on_button_move(self):
        # ボタンが移動したときの処理
        App.get_running_app().on_button_move(self)

class MainApp(App):
    def build(self):
        layout = GridLayout(cols=2, spacing=10, padding=10)

        # 左側に機能ボタンを配置
        left_layout = GridLayout(cols=1, spacing=10, size_hint_x=None, width=200)
        right_layout = GridLayout(cols=1, spacing=10)
        
        # タイトルのラベル
        title_label = Label(
            text="ほしい機能を選んでね",
            font_size=24,
            size_hint_y=None,
            height=50,
            halign="center",
        )

        button1 = DraggableButton(text=u"時間表示設定", size_hint=(None, None))
        button1.bind(on_press=self.launch_main2)
        button1.bind(on_button_move=self.on_button_move)  # ボタンが移動したときの処理を追加

        button2 = DraggableButton(text=u"天気予報", size_hint=(None, None))
        button2.bind(on_press=self.launch_main3)
        button2.bind(on_button_move=self.on_button_move)

        button3 = DraggableButton(text=u"予定表示", size_hint=(None, None))
        button3.bind(on_press=self.launch_main4)
        button3.bind(on_button_move=self.on_button_move)

        button4 = DraggableButton(text=u"背景設定", size_hint=(None, None))
        button4.bind(on_press=self.launch_main5)
        button4.bind(on_button_move=self.on_button_move)

        # 確定ボタンを右側の上部に配置
        confirm_button = Button(text="確定", size_hint=(None, None))
        confirm_button.bind(on_press=self.save_button_positions)

        left_layout.add_widget(Label())  # 上部の余白用
        left_layout.add_widget(title_label)
        left_layout.add_widget(button1)
        left_layout.add_widget(button2)
        left_layout.add_widget(button3)
        left_layout.add_widget(button4)

        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        layout.add_widget(confirm_button)  # 確定ボタンを追加

        # 背景色のRGBA値をCSVから読み込み
        background_color, _, _ = self.get_colors_from_csv("MAINSYS/CSV/color_settings.csv")

        # 背景の色を設定
        with layout.canvas.before:
            self.background_color = Color(*background_color)  # 背景色をRGBAで設定
            self.background_rect = Rectangle(pos=layout.pos, size=layout.size)

        layout.bind(pos=self.update_background, size=self.update_background)

        # 背景画像を設定
        self.set_background_image_from_csv()

        # ボタンの位置情報を保存するリスト
        self.button_positions = []

        return layout

    def launch_main2(self, instance):
        os.system("python button_clock.py")

    def launch_main3(self, instance):
        os.system("python weather2.py")
        os.system("python weathersearch.py")

    def launch_main4(self, instance):
        os.system("python Calendar.py")

    def launch_main5(self, instance):
        os.system("python haikei.py")

    def on_start(self):
        background_color, title_color, subtitle_color = self.get_colors_from_csv("MAINSYS/CSV/color_settings.csv")
        self.set_background_color(background_color)
        self.set_text_color(title_color, subtitle_color)

    def on_button_move(self, instance):
        # ボタンが移動したときに呼ばれるメソッド
        self.save_button_positions()

    def get_colors_from_csv(self, csv_file):
        background_color = (0.5, 0.7, 1, 1)  # 背景色（RGBA値を使用）
        title_color = (0.1, 0.2, 0.3, 1)  # タイトル文字色（RGBA値を使用）
        subtitle_color = (0.3, 0.4, 0.5, 1)  # サブタイトル文字色（RGBA値を使用）

        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  # ヘッダ行をスキップ
            for row in reader:
                try:
                    background_color = (float(row[0]), float(row[1]), float(row[2]), float(row[3]))  # 背景色のRGBA値を設定
                    if len(row) > 5:  # CSVファイルにタイトルとサブタイトルの色情報が含まれているか確認
                        title_color = (float(row[4]), float(row[5]), float(row[6]), float(row[7]))  # タイトル文字色のRGBA値を設定
                    if len(row) > 8:  # CSVファイルにサブタイトルの色情報が含まれているか確認
                        subtitle_color = (float(row[4]), float(row[5]), float(row[6]), float(row[7]))  # サブタイトル文字色のRGBA値を設定
                    break  # 最初の行の値を使用
                except ValueError:
                    pass
        return background_color, title_color, subtitle_color

    def update_background(self, instance, value):
        self.background_rect.pos = instance.pos
        self.background_rect.size = instance.size

    def set_background_color(self, color):
        self.background_color.rgba = color

    def set_text_color(self, title_color, subtitle_color):
        for child in self.root.children:
            if isinstance(child, Label):
                child.color = title_color

    def set_background_image_from_csv(self):
        # CSVファイルから背景画像のパスを取得
        background_image_path = self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv")
        if background_image_path:
            self.set_background_image(background_image_path)

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

    def set_background_image(self, image_path):
        # 背景画像のパスを指定して背景を設定
        self.background_rect.source = image_path

    def save_button_positions(self):
        # ボタンの位置情報を CSV ファイルに保存
        with open("MAINSYS/CSV/button_positions.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ButtonName", "X", "Y"])  # ヘッダー行

            # ボタンの位置情報を保存
            for child in self.root.children:
                if isinstance(child, DraggableButton) and child.text != "確定":
                    writer.writerow([child.text, child.center_x, child.center_y])

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
