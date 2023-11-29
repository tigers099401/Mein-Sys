# time_display_app.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
import time
import japanize_kivy

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

        # フォント変更ボタン
        font_button = Button(text='フォント変更', on_press=self.show_font_chooser, size_hint=(1, 0.3))
        self.layout.add_widget(font_button)

        # 定期的に時間を更新するためのClockイベント
        Clock.schedule_interval(self.update_time, 1)

        return self.layout

    def update_time(self, dt):
        # 時間を更新する
        self.time_label.text = self.get_japanese_time()

    def get_japanese_time(self):
        # 現在時刻を取得する
        return time.strftime("%H:%M:%S", time.localtime())

    def show_font_chooser(self, instance):
        popup = Popup(title='フォントを選択', size_hint=(0.9, 0.9))

        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path='MAINSYS/FONT', filters=['*.ttf'])
        content.add_widget(file_chooser)

        def set_font(selected_font):
            self.time_label.font_name = selected_font
            popup.dismiss()

        button_layout = BoxLayout(size_hint_y=None, height=40)
        button_layout.add_widget(Button(text='キャンセル', on_press=popup.dismiss))
        button_layout.add_widget(Button(text='選択', on_press=lambda instance: set_font(file_chooser.selection[0])))

        content.add_widget(button_layout)
        popup.content = content  # Set the content after creating the content

        popup.open()

if __name__ == '__main__':
    TimeDisplayApp().run()
