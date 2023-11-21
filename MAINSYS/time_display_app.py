# time_display_app.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import time

class MovableBoxLayout(BoxLayout):
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.pos = (touch.x - self.width / 2, touch.y - self.height / 2)

class TimeDisplayApp(App):
    def build(self):
        self.layout = MovableBoxLayout(orientation='vertical', size_hint=(1, 1))

        # 時刻表示用のラベル
        self.time_label = Label(text=self.get_japanese_time(), font_size='40sp', size_hint=(1, 0.7))
        self.layout.add_widget(self.time_label)

        # 定期的に時間を更新するためのClockイベント
        Clock.schedule_interval(self.update_time, 1)

        return self.layout

    def update_time(self, dt):
        # 時間を更新する
        self.time_label.text = self.get_japanese_time()

    def get_japanese_time(self):
        # 現在時刻を取得する
        return time.strftime("%H:%M:%S", time.localtime())

if __name__ == '__main__':
    TimeDisplayApp().run()
