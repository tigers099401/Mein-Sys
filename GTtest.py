from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import csv

class PositionSaverApp(App):
    def build(self):
        # ボタン位置情報を保存するリスト
        self.button_positions = []

        # メインのレイアウト
        layout = BoxLayout(orientation='vertical')

        # ボタンを作成
        button = Button(text="ドラッグして位置を変更")
        button.bind(on_touch_move=self.on_button_move)

        # レイアウトにボタンを追加
        layout.add_widget(button)

        # CSVファイルから位置情報を読み込む
        self.load_button_positions()

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
                self.update_button_positions(instance)

    def update_button_positions(self, button):
        # ボタンの位置情報を更新
        self.button_positions = [[button.center_x, button.center_y]]

    def load_button_positions(self):
        # CSVファイルから位置情報を読み込み、最後に配置されたボタンの位置を復元
        try:
            with open("CSV/GTcsv.csv", "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        self.button_positions = [[float(row[0]), float(row[1])]]
        except FileNotFoundError:
            pass

    def on_stop(self):
        # アプリが終了するときにボタン位置情報をCSVファイルに保存
        with open("CSV/GTcsv.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for position in self.button_positions:
                writer.writerow(position)

if __name__ == '__main__':
    PositionSaverApp().run()
