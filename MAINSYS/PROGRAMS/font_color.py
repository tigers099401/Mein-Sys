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
import time

class RunningTask:
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            print("Task is running...")
            time.sleep(1)

    def stop(self):
        self.running = False

class BackgroundChangerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # ラベル（文字色変更用）
        label_text = Label(text="文字色変更")
        self.label_text = label_text

        # カラーピッカー（文字色用）
        self.text_color_picker = ColorPicker()
        self.text_color_picker.bind(color=self.on_text_color)

        # ボタン
        button = Button(text="文字色を変更", on_press=self.change_text_color)

        # レイアウトにウィジェットを追加
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
        self.label_text.font_size = font_size

    def on_text_color(self, instance, value):
        # ラベルの文字色を変更
        self.label_text.color = value

    def change_text_color(self, instance):
        # カラーピッカーの選択色をCSVファイルに保存
        text_color = self.text_color_picker.color

        # テキスト色のRGBA値を取得
        text_red, text_green, text_blue, text_alpha = text_color

        # csvファイルの保存先ディレクトリ
        csv_dir = 'MAINSYS/CSV'

        # ディレクトリが存在しない場合、作成
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        # csvファイルの保存パス
        csv_path = os.path.join(csv_dir, 'color_settings.csv')

        # 保存されている背景色の情報を読み込む
        background_red, background_green, background_blue, background_alpha = self.load_background_color_from_csv(csv_path)

        # 背景色と新しいテキスト色の情報をCSVファイルに保存
        self.save_colors_to_csv(csv_path, background_red, background_green, background_blue, background_alpha,
                                text_red, text_green, text_blue, text_alpha)

        # 保存後に別のPythonスクリプトを実行
        script_path = 'MAINSYS\PROGRAMS\pos_mover.py'
        if os.path.exists(script_path):
            subprocess.Popen(["python", script_path])
            App.get_running_app().stop()
        else:
            print(f"スクリプト '{script_path}' は存在しません。")

    def load_background_color_from_csv(self, csv_file):
        # 背景色の情報をCSVファイルから読み込む
        if os.path.exists(csv_file):
            with open(csv_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # CSVファイルから読み込んだ値を変換して返す
                    background_red = float(row['BackgroundRed'])
                    background_green = float(row['BackgroundGreen'])
                    background_blue = float(row['BackgroundBlue'])

                    # BackgroundAlphaが文字列である場合、カンマで分割してから変換
                    background_alpha_str = row['BackgroundAlpha']
                    if ',' in background_alpha_str:
                        # カンマで区切られた文字列のリストが1つの要素として入っているため、その要素を取り出す
                        background_alpha_str = background_alpha_str.replace('[', '').replace(']', '').replace("'", "")
                        background_alpha_values = [float(value) for value in background_alpha_str.split(',')]
                        background_alpha = tuple(background_alpha_values)
                    else:
                        background_alpha = float(background_alpha_str)

                    return background_red, background_green, background_blue, background_alpha
        else:
            return 1.0, 1.0, 1.0, 1.0


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
