from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from kivy.core.window import Window
import csv
import japanize_kivy
from kivy.properties import ListProperty
from kivy.uix.relativelayout import RelativeLayout

Config.set('graphics', 'width', 1920)
Config.set('graphics', 'height', 1080)

class DraggableButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return super(DraggableButton, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super(DraggableButton, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.center_x = touch.x
            self.center_y = touch.y
            return True
        return super(DraggableButton, self).on_touch_move(touch)

class MainApp(App):
    background_color = ListProperty([1, 1, 1, 1])

    def build(self):
        layout = GridLayout(cols=1, spacing=10, padding=10)
        self.layout = layout

        title_label = Label(
            text="ほしい機能を選んでね",
            font_size=24,
            size_hint_y=None,
            height=50,
            halign="center",
        )

        with layout.canvas.before:
            Color(*self.background_color)
            self.background = Rectangle(pos=layout.pos, size=layout.size)
        
        button1 = DraggableButton(text="時間表示設定", size_hint=(None, None))
        button1.bind(on_press=self.launch_main2)

        button2 = DraggableButton(text="天気予報", size_hint=(None, None))
        button2.bind(on_press=self.launch_main3)

        button3 = DraggableButton(text="予定表示", size_hint=(None, None))
        button3.bind(on_press=self.launch_main4)

        button4 = DraggableButton(text="背景設定", size_hint=(None, None))
        button4.bind(on_press=self.launch_main5)

        button5 = DraggableButton(text="確認画面", size_hint=(None, None))
        button5.bind(on_press=self.launch_main6)

        layout.add_widget(Label())
        layout.add_widget(title_label)
        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        layout.add_widget(button4)
        layout.add_widget(button5)

        confirm_button = Button(text="確定", size_hint=(None, None))
        confirm_button.bind(on_press=self.save_button_positions)
        layout.add_widget(confirm_button)

        Window.bind(on_resize=self.update_background_size)

        # 起動時にボタン位置を読み込み
        self.load_button_positions()

        return layout

    def launch_main2(self, instance):
        # この部分は適切なコードで置き換えてください
        pass

    def launch_main3(self, instance):
        # この部分は適切なコードで置き換えてください
        pass

    def launch_main4(self, instance):
        # この部分は適切なコードで置き換えてください
        pass

    def launch_main5(self, instance):
        # この部分は適切なコードで置き換えてください
        pass

    def launch_main6(self, instance):
        # この部分は適切なコードで置き換えてください
        pass

    def save_button_positions(self, instance):
        button_positions = []
        for child in self.layout.children:
            if isinstance(child, DraggableButton):
                button_positions.append([child.text, child.center_x, child.center_y])

        with open("test/MAINSYS/CSV/dbutton_positions.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(button_positions)

    def load_button_positions(self):
        button_positions = []
        try:
            with open("MAINSYS/CSV/button_positions.csv", "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    button_positions.append(row)
        except FileNotFoundError:
            pass

        for text, x, y in button_positions:
            for child in self.layout.children:
                if isinstance(child, DraggableButton) and child.text == text:
                    child.center_x = float(x)
                    child.center_y = float(y)

    def on_start(self):
        background_color, title_color, subtitle_color = self.get_colors_from_csv("MAINSYS/CSV/color_settings.csv")
        self.set_background_color(background_color)

        image_link = self.get_image_link_from_csv("MAINSYS/CSV/selected_backgrounds.csv")
        if image_link:
            self.set_background_image(image_link)

    def get_colors_from_csv(self, csv_file):
        background_color = (1, 1, 1)
        title_color = (0, 0, 0)
        subtitle_color = (0, 0, 0)

        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    background_color = [float(val) for val in row]
                    break
                except ValueError:
                    pass
        return background_color

    def set_background_color(self, color):
        self.background_color = color

    def update_background_size(self, instance, width, height):
        self.background.size = (width, height)

if __name__ == "__main__":
    MainApp().run()
