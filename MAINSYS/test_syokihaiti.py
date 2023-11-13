from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import csv
import japanize_kivy

class ButtonLoaderApp(App):
    def build(self):
        # ウィンドウを作成
        layout = FloatLayout()

        # ボタンの情報
        button_info = [
            {"name": "時間表示設定", "pos": (50, 100)},
            {"name": "天気予報", "pos": (200, 100)},
            {"name": "予定表示", "pos": (350, 100)},
            {"name": "追加", "pos": (500, 100)},
        ]

        # ボタンリスト
        self.buttons = []

        for info in button_info:
            # CSVファイルからボタンの座標を取得
            button_pos = self.load_button_position(info["name"])

            # ボタンを作成
            button = Button(text=f'{info["name"]}')
            button.size_hint = (None, None)
            button.size = (100, 50)
            button.pos = button_pos

            # ボタンをレイアウトに追加
            layout.add_widget(button)

            # ボタンをリストに追加
            self.buttons.append(button)

        return layout

    def load_button_position(self, button_name):
        # CSVファイルからボタンの座標を取得するメソッド
        try:
            filename = f'{button_name.lower()}_position.csv'
            with open(filename, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header
                # Check if there are rows in the CSV file
                row = next(csv_reader, None)
                if row:
                    button_pos = [float(row[0]), float(row[1])]
                else:
                    # If there are no rows, use default position
                    button_pos = (100, 100)
        except (FileNotFoundError, ValueError, IndexError):
            # Handle file not found or invalid data gracefully
            button_pos = (100, 100)

        return button_pos

if __name__ == '__main__':
    # 別のアプリケーションで座標を読み込み、ボタンを配置
    ButtonLoaderApp().run()
