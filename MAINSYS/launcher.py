# launcher.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
import subprocess

class LauncherApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # syoki.py を実行して結果を表示するラベル
        syoki_output_label = Label(text=self.run_syoki())
        layout.add_widget(syoki_output_label)

        return layout

    def run_syoki(self):
        # "syoki.py" を実行して出力を取得
        process = subprocess.Popen(["C:/Users/204004/AppData/Local/Programs/Python/Python311/python.exe", "MAINSYS/syoki.py"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        output, error = process.communicate()

        # エラーが発生した場合はエラーメッセージを表示
        if process.returncode != 0:
            return f"Error: {error}"

        return output

if __name__ == '__main__':
    LauncherApp().run()
