from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import os
import subprocess
import csv
import japanize_kivy

class BackgroundApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # 画像表示用のウィジェット
        self.image_widget = Image(source="MAINSYS/IMAGE/haro.jpg", size=(400, 400), allow_stretch=True)
        self.layout.add_widget(self.image_widget)

        # ファイル選択ボタン
        file_select_button = Button(text='背景画像を選択', on_press=self.show_file_chooser, size_hint=(1, 0.1))
        self.layout.add_widget(file_select_button)

        # 次へボタン
        next_button = Button(text='次へ', on_press=self.next_page, size_hint=(1, 0.1))
        self.layout.add_widget(next_button)

        # 選択された背景画像の相対パスを保存するCSVファイルのパス
        self.csv_file_path = "MAINSYS/CSV/selected_backgrounds.csv"

        return self.layout

    def show_file_chooser(self, instance):
        file_chooser = FileChooserListView(path='MAINSYS/IMAGE', filters=['*.jpg', '*.png'])
        file_chooser.bind(on_submit=self.update_background)

        # Popupのインスタンスを作成
        self.popup = Popup(title='背景画像を選択', content=file_chooser, size_hint=(0.9, 0.9))
        self.popup.open()

    def update_background(self, instance, value, *args):
        # ファイル選択ダイアログで選ばれた画像を表示
        selected_background = os.path.abspath(os.path.join('MAINSYS/IMAGE', value[0]))

        # CSVファイルに絶対パスを保存（上書き）
        self.save_to_csv(selected_background)

        self.image_widget.source = selected_background
        self.image_widget.reload()

        # ファイル選択後にFileChooserListViewの表示を非表示にする
        self.dismiss_popup()

    def dismiss_popup(self):
        # Popupを閉じる
        if self.popup:
            self.popup.dismiss()

    def save_to_csv(self, selected_background):
        # CSVファイルに絶対パスを保存（上書き）
        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([selected_background])

    def next_page(self, instance):
        # ここに次へボタンが押されたときの処理を書く
        # subprocessを使用してpos_mover.pyを実行する
        subprocess.run(["python", "MAINSYS/PROGRAMS/pos_mover.py"])

        # オプションで、新しいスクリプトを開始した後に現在のKivyアプリを終了することができます
        App.get_running_app().stop()

if __name__ == '__main__':
    BackgroundApp().run()
