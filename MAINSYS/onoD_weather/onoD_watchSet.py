from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import csv
import japanize_kivy

class ImageButtonApp(App):
    def build(self):

        # タイトルラベルを作成
        title_label = Label(text='時計形式くらい自分で選択しろ', font_size='24sp', bold=True, color = (1,1,1,1))

        # 画像ボタンを作成
        image_path = r'C:\Users\204012\Desktop\image\click.jpg'
        image_fst_button = Button(background_normal=image_path, background_down=image_path, size_hint=(None, None), width=500, height=500)
        image_fst_button.bind(on_press=self.on_button_press)
        
        # 画像ボタンを作成
        image_path = r'C:\Users\204012\Desktop\image\click.jpg'
        image_sec_button = Button(background_normal=image_path, background_down=image_path, size_hint=(None, None), width=500, height=500)
        image_sec_button.bind(on_press=self.on_button_press)

        # レイアウトを作成し、ボタンを追加
        layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        layout.add_widget(title_label)
        layout.add_widget(image_fst_button)
        layout.add_widget(image_sec_button)
        
        return layout


    def on_button_press(self, instance):
        print('1つ目のボタンが押されました！')
        watch = 1
        self.update_csv(watch)

    def on_second_button_press(self, instance):
        print('2つ目のボタンが押されました！')
        watch = 2
        self.update_csv(watch)

    def update_csv(self, watch):
        # ファイルの読み込みと書き込みはここで行います
        file_path = r'C:\Users\204012\Desktop\test_git\test\onoD\onoD_Opt.csv'
        
        # 既存のCSVファイルを読み込む
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
            
        # 必要な部分を変更
        data[1][1] = str(watch)  # watchを文字列に変換して代入
        
        # 新しいCSVファイルに書き出す
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

if __name__ == '__main__':
    ImageButtonApp().run()