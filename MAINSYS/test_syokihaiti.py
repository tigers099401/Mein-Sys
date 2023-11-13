from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import csv

class ButtonLoaderApp(App):
    def build(self):
        layout = FloatLayout()

        # CSVファイルから位置情報を読み込み
        button_position = self.load_button_position()

        # 位置情報を元にボタンを配置
        move_button = Button(text="Move Me!", pos=(button_position["x"], button_position["y"]))
        layout.add_widget(move_button)

        return layout

    def load_button_position(self):
        try:
            with open("button_position.csv", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    return {"x": float(row["x"]), "y": float(row["y"])}
        except FileNotFoundError:
            return {"x": 0, "y": 0}

if __name__ == "__main__":
    ButtonLoaderApp().run()
