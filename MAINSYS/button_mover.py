from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import csv
import japanize_kivy

class ButtonMoverApp(App):
    def build(self):
        # ウィンドウを作成
        layout = FloatLayout()

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
            layout.add_widget(button)

            # ボタンをリストに追加
            self.buttons.append(button)

        return layout

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

if __name__ == '__main__':
    # アプリケーションを起動
    ButtonMoverApp().run()
