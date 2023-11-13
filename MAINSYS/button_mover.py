# button_mover.py
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import csv

class ButtonMoverApp(App):
    def build(self):
        # ウィンドウを作成
        layout = FloatLayout()

        # ボタンの数
        num_buttons = 4

        # ボタンリスト
        self.buttons = []

        for i in range(num_buttons):
            # ボタンを作成
            button = Button(text=f'Move me {i+1}!')
            button.size_hint = (None, None)
            button.size = (100, 50)
            button.pos = (i * 150 + 50, 100)

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
        for i, button in enumerate(self.buttons):
            button_pos = button.pos
            filename = f'button_{i + 1}_position.csv'
            with open(filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['x', 'y'])
                csv_writer.writerow([button_pos[0], button_pos[1]])

if __name__ == '__main__':
    # アプリケーションを起動
    ButtonMoverApp().run()
