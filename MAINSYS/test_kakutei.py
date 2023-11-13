from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import csv

class ButtonMoverApp(App):
    def build(self):
        # ウィンドウを作成
        layout = FloatLayout()

        # ボタンの初期座標を指定
        initial_button_pos = (100, 100)

        # ボタンを作成
        self.button = Button(text='Move me!')
        self.button.size_hint = (None, None)
        self.button.size = (100, 50)
        self.button.pos = initial_button_pos

        # ボタンをレイアウトに追加
        layout.add_widget(self.button)

        # ボタンが移動したときのイベントを追加
        self.button.bind(on_touch_move=self.on_button_move)

        return layout

    def on_button_move(self, instance, touch):
        # ボタンがタッチされ、移動したときに呼ばれるメソッド
        if self.button.collide_point(*touch.pos):
            self.button.pos = touch.pos

    def on_stop(self):
        # アプリケーションが終了するときに呼ばれるメソッド
        self.save_button_position()

    def save_button_position(self):
        # ボタンの座標をCSVファイルに保存するメソッド
        button_pos = self.button.pos
        with open('button_position.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['x', 'y'])
            csv_writer.writerow([button_pos[0], button_pos[1]])

class ButtonLoaderApp(App):
    def build(self):
        # ウィンドウを作成
        layout = FloatLayout()

        # CSVファイルからボタンの座標を取得
        button_pos = self.load_button_position()

        # ボタンを作成
        self.button = Button(text='Loaded Button')
        self.button.size_hint = (None, None)
        self.button.size = (100, 50)
        self.button.pos = button_pos

        # ボタンをレイアウトに追加
        layout.add_widget(self.button)

        return layout

    def load_button_position(self):
        # CSVファイルからボタンの座標を取得するメソッド
        try:
            with open('button_position.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header
                button_pos = [float(row[0]), float(row[1])]
        except (FileNotFoundError, IndexError):
            # ファイルが存在しないか、座標が取得できない場合は初期値を返す
            button_pos = (100, 100)
        return button_pos

if __name__ == '__main__':
    # アプリケーションを起動
    ButtonMoverApp().run()

    # 別のアプリケーションで座標を読み込み、ボタンを配置
    ButtonLoaderApp().run()
