from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
import subprocess
import os
import japanize_kivy

class MyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)

        # 上部の中央に横並びでボタンを配置するBoxLayout
        top_buttons_layout = GridLayout(cols=3, size_hint_y=None, height=100, spacing=10, pos_hint={'center_y': 0.9})

        # ボタンの作成と追加
        button_names = ["時間表示設定", "天気予報", "予定表示", "フォント・カラー", "背景画像", "追加", "配置設定"]
        for name in button_names:
            button = Button(text=name, size_hint=(None, None), size=(200, 50))
            button.bind(on_press=self.on_button_press)
            top_buttons_layout.add_widget(button)

        # 上部のボタンを追加
        self.add_widget(top_buttons_layout)

        # 確定ボタンを作成して右下に追加（左に少しだけ寄せる）
        confirm_button = Button(text="戻る", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.88, 'center_y': 0})
        confirm_button.bind(on_press=self.on_button_press)
        self.add_widget(confirm_button)

    #時間表示設定
    def on_button_press(self, instance):
        button_text = instance.text
        print(f"Button {button_text} pressed!")
        
        if button_text == "時間表示設定":
            # time_display_app.pyを実行する
            app_path = os.path.join(os.getcwd(), "testplay/testplay22/time_display_app.py")
            process = subprocess.Popen(["python", app_path])
            process.communicate()

    #天気予報
    def on_button_press(self, instance):
        button_text = instance.text
        print(f"Button {button_text} pressed!")
        
        if button_text == "天気予報":
            # time_display_app.pyを実行する
            app_path = os.path.join(os.getcwd(), "testplay/testplay22/time_display_app.py")
            process = subprocess.Popen(["python", app_path])
            process.communicate()

    #予定表示
    def on_button_press(self, instance):
        button_text = instance.text
        print(f"Button {button_text} pressed!")
        
        if button_text == "予定表示":
            # time_display_app.pyを実行する
            app_path = os.path.join(os.getcwd(), "testplay/testplay22/time_display_app.py")
            process = subprocess.Popen(["python", app_path])
            process.communicate()

    #フォント・カラー
    def on_button_press(self, instance):
        button_text = instance.text
        print(f"Button {button_text} pressed!")
        
        if button_text == "フォント・カラー":
            # time_display_app.pyを実行する
            app_path = os.path.join(os.getcwd(), "testplay/testplay22/time_display_app.py")
            process = subprocess.Popen(["python", app_path])
            process.communicate()

    #背景画像
    def on_button_press(self, instance):
        button_text = instance.text
        print(f"Button {button_text} pressed!")
        
        if button_text == "背景画像":
            # time_display_app.pyを実行する
            app_path = os.path.join(os.getcwd(), "testplay/testplay22/time_display_app.py")
            process = subprocess.Popen(["python", app_path])
            process.communicate()

    #追加
    def on_button_press(self, instance):
        button_text = instance.text
        print(f"Button {button_text} pressed!")
        
        if button_text == "追加":
            # time_display_app.pyを実行する
            app_path = os.path.join(os.getcwd(), "testplay/testplay22/time_display_app.py")
            process = subprocess.Popen(["python", app_path])
            process.communicate()

    #配置設定
    def on_button_press(self, instance):
        button_text = instance.text
        print(f"Button {button_text} pressed!")
        
        if button_text == "配置設定":
            # time_display_app.pyを実行する
            app_path = os.path.join(os.getcwd(), "testplay/testplay22/time_display_app.py")
            process = subprocess.Popen(["python", app_path])
            process.communicate()

    #戻る
    def on_button_press(self, instance):
        button_text = instance.text
        print(f"Button {button_text} pressed!")
        
        if button_text == "戻る":
            # time_display_app.pyを実行する
            app_path = os.path.join(os.getcwd(), "PROGRAMS\main_facter.py")
            process = subprocess.Popen(["python", app_path])
            process.communicate()

class MyApp(App):
    def build(self):
        return MyWidget(orientation='vertical', spacing=10, padding=10)

if __name__ == '__main__':
    MyApp().run()
