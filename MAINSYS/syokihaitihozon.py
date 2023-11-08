from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Rectangle
import csv
import japanize_kivy
import os

class DraggableButton(Scatter):
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
            return True
        return super(DraggableButton, self).on_touch_move(touch)

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

        layout.add_widget(Label())  # 上部の余白用
        layout.add_widget(title_label)

        # ボタンの位置情報をCSVから読み込んで配置
        button_positions = self.get_button_positions_from_csv("MAINSYS/CSV/button_positions.csv")
        for position in button_positions:
            button = DraggableButton(size=(100, 100), pos=position)
            layout.add_widget(button)

        # 「確定」ボタンを右上に配置
        confirm_button = Button(text="確定", size_hint=(None, None), size=(100, 50), pos=(800, 500))
        confirm_button.bind(on_press=self.save_button_positions)
        layout.add_widget(confirm_button)

        # 背景色のRGBA値をCSVから読み込み
        background_color, _, _ = self.get_colors_from_csv("MAINSYS/CSV/color_settings.csv")

        # 背景の色を設定
        with layout.canvas.before:
            self.background_color = Color(*background_color)  # 背景色をRGBAで設定
            self.background_rect = Rectangle(pos=layout.pos, size=layout.size)

        layout.bind(pos=self.update_background, size=self.update_background)

        # 背景画像を設定
        self.set_background_image_from_csv()

        return layout

    def get_button_positions_from_csv(self, csv_file):
        button_positions = []
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        x, y = map(int, row)
                        button_positions.append((x, y))
        except FileNotFoundError:
            pass
        return button_positions

    def save_button_positions(self, instance):
        button_positions = [(int(button.center_x), int(button.center_y)) for button in self.root.children if isinstance(button, DraggableButton)]
        with open("MAINSYS/CSV/button_positions.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for position in button_positions:
                writer.writerow(position)

    def on_start(self):
        background_color, title_color, subtitle_color = self.get_colors_from_csv("MAINSYS/CSV/color_settings.csv")
        self.set_background_color(background_color)
        self.set_text_color(title_color, subtitle_color)

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

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
