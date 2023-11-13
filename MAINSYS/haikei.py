from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.colorpicker import ColorPicker
import csv
import os
from kivy.core.window import Window
import japanize_kivy
import subprocess  # 外部スクリプトを実行するために必要なモジュール

class BackgroundChangerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # ラベル（背景色変更用）
        label_background = Label(text="背景色変更")
        self.label_background = label_background

        # カラーピッカー（背景色用）
        self.background_color_picker = ColorPicker()
        self.background_color_picker.bind(color=self.on_background_color)

        # ラベル（文字色変更用）
        label_text = Label(text="文字色変更")
        self.label_text = label_text

        # カラーピッカー（文字色用）
        self.text_color_picker = ColorPicker()
        self.text_color_picker.bind(color=self.on_text_color)

        # ボタン
        button = Button(text="背景色と文字色を変更", on_press=self.change_background_and_text_color)

        # レイアウトにウィジェットを追加
        layout.add_widget(label_background)
        layout.add_widget(self.background_color_picker)
        layout.add_widget(label_text)
        layout.add_widget(self.text_color_picker)
        layout.add_widget(button)

        # ウィンドウサイズ変更時にオブジェクトを調整
        Window.bind(on_resize=self.on_window_resize)

        return layout

    def on_window_resize(self, instance, width, height):
        # ウィンドウサイズが変更されたときに呼ばれるメソッド
        # フォントサイズを調整
        font_size = int(0.04 * height)  # 画面高さの4%をフォントサイズとする
        self.label_background.font_size = font_size
        self.label_text.font_size = font_size

    def on_background_color(self, instance, value):
        # カラーピッカーの色に背景色を変更
        # バックグラウンド画像を含む場合に使用
        pass

    def on_text_color(self, instance, value):
        # ラベルの文字色を変更
        self.label_background.color = value
        self.label_text.color = value

    def change_background_and_text_color(self, instance):
        # カラーピッカーの選択色をCSVファイルに保存
        background_color = self.background_color_picker.color
        text_color = self.text_color_picker.color

        # 背景色と文字色のRGBA値を取得
        background_red, background_green, background_blue, background_alpha = background_color
        text_red, text_green, text_blue, text_alpha = text_color

        # csvファイルの保存先ディレクトリ
        csv_dir = 'MAINSYS/CSV'

        # ディレクトリが存在しない場合、作成
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        # csvファイルの保存パス
        csv_path = os.path.join(csv_dir, 'color_settings.csv')

        self.save_colors_to_csv(csv_path, background_red, background_green, background_blue, background_alpha,
                                text_red, text_green, text_blue, text_alpha)

        # 保存後に別のPythonスクリプトを実行
        script_path = 'MAINSYS/button_mover.py'
        if os.path.exists(script_path):
            subprocess.Popen(['python', script_path])
        else:
            print(f"スクリプト '{script_path}' は存在しません。")

    def save_colors_to_csv(self, csv_file, background_red, background_green, background_blue, background_alpha,
                           text_red, text_green, text_blue, text_alpha):
        with open(csv_file, 'w', newline='') as csvfile:
            fieldnames = ['BackgroundRed', 'BackgroundGreen', 'BackgroundBlue', 'BackgroundAlpha',
                          'TextRed', 'TextGreen', 'TextBlue', 'TextAlpha']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'BackgroundRed': background_red,
                'BackgroundGreen': background_green,
                'BackgroundBlue': background_blue,
                'BackgroundAlpha': background_alpha,
                'TextRed': text_red,
                'TextGreen': text_green,
                'TextBlue': text_blue,
                'TextAlpha': text_alpha
            })

if __name__ == '__main__':
    BackgroundChangerApp().run()
