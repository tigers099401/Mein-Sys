from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import csv
import os

class ButtonPositionApp(App):
    def build(self):
        # メインのレイアウト
        layout = BoxLayout(orientation='vertical')

        # ボタンを作成して配置
        buttons = self.load_button_positions()
        if buttons:
            for button in buttons:
                layout.add_widget(button)

        return layout

    def load_button_positions(self):
        csv_file = "CSV/GTcsv.csv"
        buttons = []

        if os.path.isfile(csv_file):
            with open(csv_file, newline='') as file:
                reader = csv.reader(file)
                next(reader)  # ヘッダー行をスキップ
                for row in reader:
                    x, y = map(float, row)
                    button = self.create_button(x, y)
                    buttons.append(button)  # ここでボタンをリストに追加

        return buttons

    def create_button(self, x, y):
        button = Button(text="Drag me", size_hint=(None, None), size=(100, 50))  # 幅100、高さ50のボタン
        button.pos = (x, y)
        return button

if __name__ == '__main__':
    ButtonPositionApp().run()
