from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Line, Color, Ellipse
from math import sin, cos, radians
from datetime import datetime

class ClockApp(App):
    def build(self):
        # ウィジェットを配置するためのレイアウト
        layout = BoxLayout(orientation='vertical')

        # アナログ時計表示用のウィジェット
        self.analog_clock_widget = AnalogClockWidget(size=(300, 300))
        layout.add_widget(self.analog_clock_widget)

        # タイマーを設定して1秒ごとに時間を更新
        Clock.schedule_interval(self.update_time, 1)

        return layout

    def update_time(self, dt):
        # アナログ時計の更新
        now = datetime.now()
        self.analog_clock_widget.update_time(now)

    def show_digital_clock(self):
        # デジタル時計を表示するメソッド
        digital_clock_app = DigitalClockApp()
        digital_clock_app.run()

class AnalogClockWidget(Widget):
    def __init__(self, **kwargs):
        super(AnalogClockWidget, self).__init__(**kwargs)
        self.hour_hand = Line()
        self.minute_hand = Line()
        self.second_hand = Line()
        self.draw_clock()

    def draw_clock(self):
        with self.canvas:
            Color(1, 1, 1)
            Ellipse(pos=self.pos, size=self.size)

            Color(0, 0, 0)
            Ellipse(pos=self.pos, size=self.size, angle_end=360)

            self.hour_hand.points = [self.center_x, self.center_y, self.center_x, self.center_y]
            self.minute_hand.points = [self.center_x, self.center_y, self.center_x, self.center_y]
            self.second_hand.points = [self.center_x, self.center_y, self.center_x, self.center_y]

    def update_time(self, now):
        # アナログ時計の針の角度を計算
        hour_angle = (now.hour % 12 + now.minute / 60.0) * 30.0
        minute_angle = now.minute * 6.0
        second_angle = now.second * 6.0

        # 針の長さを設定
        hour_length = self.width / 4.0
        minute_length = self.width / 3.0
        second_length = self.width / 2.5

        # 針を描画
        self.draw_hand(self.hour_hand, hour_angle, hour_length)
        self.draw_hand(self.minute_hand, minute_angle, minute_length)
        self.draw_hand(self.second_hand, second_angle, second_length)

    def draw_hand(self, hand, angle, length):
        hand.points = [self.center_x, self.center_y,
                       self.center_x + length * 0.8 * sin(radians(angle)),
                       self.center_y + length * 0.8 * cos(radians(angle))]

    def on_touch_down(self, touch):
        # タッチでアナログ時計をクリックした際にデジタル時計に切り替える
        if self.collide_point(*touch.pos):
            ClockApp().show_digital_clock()

class DigitalClockApp(App):
    def build(self):
        # ウィジェットを配置するためのレイアウト
        layout = BoxLayout(orientation='vertical')

        # デジタル時計表示用のラベル
        self.digital_clock_label = Label(font_size=50)
        layout.add_widget(self.digital_clock_label)

        # タイマーを設定して1秒ごとに時間を更新
        Clock.schedule_interval(self.update_time, 1)

        return layout

    def update_time(self, dt):
        # デジタル時計の更新
        now = datetime.now()
        formatted_time = now.strftime("%H:%M:%S")
        self.digital_clock_label.text = formatted_time

if __name__ == '__main__':
    ClockApp().run()
