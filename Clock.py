from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.label import Label 
import time
import csv
class TimeDisplayApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.time_label = Label(text=self.get_japanese_time(), font_size='40sp', size_hint=(1, 0.7))
        self.layout.add_widget(self.time_label)

        Clock.schedule_interval(self.update_time, 1)  # 1秒ごとに時間を更新

        return self.layout

    def update_time(self, dt):
        self.time_label.text = self.get_japanese_time()

    def get_japanese_time(self):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        return current_time

if __name__ == '__main__':
    TimeDisplayApp().run()