from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import csv
import os

class PositionSaverApp(App):
    def build(self):
        # メインのレイアウト
        layout = BoxLayout(orientation='vertical')

        # ボタンの位置情報をCSVファイルから読み込み
        button_positions = self.load_button_positions()

        if button_positions:
            # CSVファイルから位置情報が読み込まれた場合
            for position in button_positions:
                # 位置情報を元にボタンを作成
                button = Button(text="ドラッグして位置を変更")
                button.center_x, button.center_y = position

                # ボタンの移動を有効にする
                button.bind(on_touch_move=self.on_button_move)

                # レイアウトにボタンを追加
                layout.add_widget(button)
        else:
            # 位置情報がCSVファイルにない場合、デフォルトのボタンを作成
            button = Button(text="ドラッグして位置を変更")
            button.bind(on_touch_move=self.on_button_move)
            layout.add_widget(button)

        return layout

    def on_button_move(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # ボタンがタッチされた場合
            if touch.grab_current is None:
                # ボタンがまだタッチされていない場合
                touch.grab(instance)
            else:
                # ボタンがタッチされている場合、位置情報を更新
                instance.center_x = touch.x
                instance.center_y = touch.y

    def load_button_positions(self):
        # CSVファイルからボタンの位置情報を読み込む
        csv_file = "CSV/GTcsv.csv"
        button_positions = []
        if os.path.exists(csv_file):
            with open(csv_file, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        position = [float(row[0]), float(row[1])]
                        button_positions.append(position)
                    except (ValueError, IndexError):
                        pass
        return button_positions

if __name__ == '__main__':
    PositionSaverApp().run()
