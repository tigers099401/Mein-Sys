
import os
import cv2
import numpy as np

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.clock import Clock
from kivy.graphics.texture import Texture

#画像ボタンクラス
class MyButton(ToggleButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        #画像ボタンの画像名を格納
        self.source = kwargs["source"]
        #画像を編集できるようにテクスチャーとして扱う
        self.texture = self.button_texture(self.source)

    # トグルボタンの状態、状態によって画像が変化する
    def on_state(self, widget, value):
        if value == 'down':
            self.texture = self.button_texture(self.source, off=True)
        else:
            self.texture = self.button_texture(self.source)

    # 画像を変化させる、押した状態の時に矩形+色を暗く
    def button_texture(self, data, off=False):
        im = cv2.imread(data)
        im = self.square_image(im)
        if off:
            im = self.adjust(im, alpha=0.6, beta=0.0)
            im = cv2.rectangle(im, (2, 2), (im.shape[1]-2, im.shape[0]-2), (255, 255, 0), 10)

        # 上下反転
        buf = cv2.flip(im, 0)
        image_texture = Texture.create(size=(im.shape[1], im.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        return image_texture

    # 画像を正方形にする
    def square_image(self, img):
        h, w = img.shape[:2]
        if h > w:
            x = int((h-w)/2)
            img = img[x:x + w, :, :]
        elif h < w:
            x = int((w - h) / 2)
            img = img[:, x:x + h, :]

        return img

    # 画像の色を暗くする
    def adjust(self, img, alpha=1.0, beta=0.0):
        # 積和演算を行う。
        dst = alpha * img + beta
        # [0, 255] でクリップし、uint8 型にする。
        return np.clip(dst, 0, 255).astype(np.uint8)


class Test(BoxLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        # 読み込むディレクトリ
        image_dir = "MAINSYS\IMAGE"

        # 縦配置
        self.orientation = 'vertical'

        # 画像ファイルの名前を管理
        self.image_name = ""

        # 画像を表示するウィジェットの準備
        self.image = Image(size_hint=(1, 0.5))
        self.add_widget(self.image)

        # 画像ボタンを配置する、スクロールビューの定義
        sc_view = ScrollView(size_hint=(1, None), size=(self.width, self.height*4))

        # スクロールビューには１つのウィジェットしか配置できないため
        box = GridLayout(cols=5, spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        # 画像ボタンの一括定義、グリッドレイアウトに配置
        box = self.image_load(image_dir, box)

        sc_view.add_widget(box)
        self.add_widget(sc_view)

    # 画像ボタンの読み込み
    def image_load(self, im_dir, grid):
        images = sorted(os.listdir(im_dir))

        for image in images:
            button = MyButton(size_hint_y=None,
                              height=300,
                              source=os.path.join(im_dir, image),
                              group="g1")
            button.bind(on_press=self.set_image)
            grid.add_widget(button)

        return grid

    # 画像をボタンを押した時、画像ウィジェットに画像を表示
    def set_image(self, btn):
        if btn.state=="down":
            self.image_name = btn.source
            #画面を更新
            Clock.schedule_once(self.update)

    # 画面更新
    def update(self, t):
        self.image.source = self.image_name


class SampleApp(App):
    def build(self):
        return Test()


SampleApp().run()
