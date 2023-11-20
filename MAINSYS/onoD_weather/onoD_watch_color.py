from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
import time

import csv

class TimeDisplayApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        back_button = Button(text='戻る', size_hint=(0.1, 0.1))
        back_button.bind(on_press=self.back_action)
        self.layout.add_widget(back_button)

        self.time_label = Label(text=self.get_japanese_time(), font_size='40sp', size_hint=(1, 0.7))
        self.layout.add_widget(self.time_label)

        # 色の選択ボタンを追加
        color_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1), (1, 0, 1, 1), (0, 1, 1, 1), (0.5, 0.5, 0.5, 1), (1, 1, 1, 1)]
        for color in colors:
            color_button = Button(background_color=color, size_hint=(0.125, 1))
            color_button.bind(on_press=lambda instance, color=color: self.change_color(color))
            color_buttons.add_widget(color_button)
            
        self.layout.add_widget(color_buttons)

        confirm_button = Button(text='確定', size_hint=(1, 0.1))
        confirm_button.bind(on_press=self.confirm_action)
        self.layout.add_widget(confirm_button)

        Clock.schedule_interval(self.update_time, 1)  # 1秒ごとに時間を更新

        return self.layout

    def update_time(self, dt):
        self.time_label.text = self.get_japanese_time()

    def get_japanese_time(self):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        return current_time

    def change_color(self, color):
        self.time_label.color = color

    
    def confirm_action(self, color):
        print("確定ボタンが押されました。")
         # ファイルの読み込みと書き込みはここで行います
        file_path = "test\onoD\onoD_csv_list\onoD_opt.csv"
        
        # 既存のCSVファイルを読み込む
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        
        
        # 必要な部分を変更
        data[5][1] = str(color)  # watchを文字列に変換して代入
        
        # 新しいCSVファイルに書き出す
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    
    
    def back_action(self, instance):
        print("戻るボタンが押されました。")

if __name__ == '__main__':
    TimeDisplayApp().run()