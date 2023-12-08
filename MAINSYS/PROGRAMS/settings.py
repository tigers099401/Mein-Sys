from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
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

    def on_button_press(self, instance):
        button_text = instance.text
        print(f"ボタン {button_text} が押されました！")

        if button_text == "時間表示設定":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/time_display_app.py")
        elif button_text == "天気予報":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/main_facter.py")
        elif button_text == "予定表示":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/main_facter.py")
        elif button_text == "フォント・カラー":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/main_facter.py")
        elif button_text == "背景画像":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/haikeigazou.py")
        elif button_text == "追加":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/main_facter.py")
        elif button_text == "配置設定":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/pos_mover.py")
        elif button_text == "戻る":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/main_facter.py")

        process = subprocess.Popen(["python", app_path])
        process.communicate()

class MyApp(App):
    def build(self):
        return MyWidget(orientation='vertical', spacing=10, padding=10)

if __name__ == '__main__':
    MyApp().run()
