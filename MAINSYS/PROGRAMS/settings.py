from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
import subprocess
import os
import japanize_kivy
import csv

class MyWidget(FloatLayout):
    def __init__(self, **kwargs):
        self.setflg(1)
        super(MyWidget, self).__init__(**kwargs)

        # タイトル表示用のラベルを作成
        title_label = Label(text="設定", font_size=24, size_hint_y=None, height=50, pos_hint={'center_x': 0.5, 'top': 0.9})
        self.add_widget(title_label)

        # 上部に縦並びでボタンを配置するBoxLayout
        top_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=150, spacing=10, pos_hint={'center_x': 0.5, 'top': 0.7})
        
        # ボタンの作成と追加
        button_names = ["時間表示設定", "天気予報", "予定表示", "フォントカラー・背景カラー"]
        for i, name in enumerate(button_names):
            button = Button(text=name, size_hint=(None, None), size=(200, 50))
            button.bind(on_press=self.on_button_press)
            
            top_buttons_layout.add_widget(button)

            # 2列目のボタンを挿入
            if i % 2 == 1:
                top_buttons_layout.add_widget(BoxLayout(size_hint_x=None, width=10))

        # 上部のボタンレイアウトを追加
        self.add_widget(top_buttons_layout)

    
        # 下部に横並びでボタンを配置するBoxLayout
        bottom_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10, pos_hint={'center_x': 0.5, 'top': 0.4})
        
        # ボタンの作成と追加
        button_names = ["背景画像", "追加", "配置設定","フォント"]
        for i, name in enumerate(button_names):
            button = Button(text=name, size_hint=(None, None), size=(200, 50))
            button.bind(on_press=self.on_button_press)
            
            bottom_buttons_layout.add_widget(button)

            # 2列目のボタンを挿入
            if i % 2 == 1:
                bottom_buttons_layout.add_widget(BoxLayout(size_hint_x=None, width=10))

        # 下部のボタンレイアウトを追加
        self.add_widget(bottom_buttons_layout)

        # 戻るボタンを作成して右下に追加
        back_button = Button(text="戻る", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.88, 'y': 0.1})
        back_button.bind(on_press=self.on_button_press)
        self.add_widget(back_button)

    def on_button_press(self, instance):
        button_text = instance.text
        print(f"ボタン {button_text} が押されました！")

        if button_text == "時間表示設定":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/time_display_app.py")
        elif button_text == "天気予報":
            app_path = os.path.join(os.getcwd(), "MAINSYS\PROGRAMS\onoD_weatherSet.py")
        elif button_text == "予定表示":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/main_facter.py")
        elif button_text == "フォントカラー・背景カラー":
            app_path = os.path.join(os.getcwd(), "MAINSYS\PROGRAMS\haikei.py")
        elif button_text == "背景画像":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/haikeigazou.py")
        elif button_text == "追加":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/main_facter.py")
        elif button_text == "配置設定":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/pos_mover.py")
        elif button_text == "フォント":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/font.py")
        elif button_text == "戻る":
            self.setflg(0)
            app_path = os.path.join(os.getcwd(), "MAINSYS\PROGRAMS\main_facter.py")
            App.get_running_app().stop()
        subprocess.Popen(["python", app_path])

    def setflg(self,flgval):   # CSVファイルに設定用フラグを保存するメソッド
        filename = 'MAINSYS\CSV\onoD_opt.csv'
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            print(flgval)
            data[10][1] = flgval
        
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
        print("保存されました！")

            




        return 


class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()
