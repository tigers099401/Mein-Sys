import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import os
import subprocess

# メインウィンドウの作成
root = tk.Tk()
root.title("背景画像選択")

# 画像表示用のキャンバスを作成
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# 背景画像の初期値
selected_background = "MAINSYS/FONT/haro.jpg"  # 初期の背景画像パス

def change_background():
    global selected_background
    # ファイル選択ダイアログを表示して画像を選択
    file_path = filedialog.askopenfilename(initialdir="MAINSYS/FONT", filetypes=[("Image files", "*.jpg *.png")])
    
    if file_path:
        selected_background = file_path
        update_background()
        save_to_csv(selected_background)  # 選択した画像のリンクをCSVに保存

def update_background():
    # 選択された背景画像を読み込み、キャンバスに表示
    background_image = Image.open(selected_background)
    background_image = background_image.resize((400, 400), Image.BOX)  # リサンプリングフィルターを指定
    background_photo = ImageTk.PhotoImage(background_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    canvas.background_photo = background_photo

def save_to_csv(image_link):
    csv_folder = "MAINSYS/CSV"
    os.makedirs(csv_folder, exist_ok=True)  # フォルダが存在しない場合、作成する

    csv_file = os.path.join(csv_folder, "selected_backgrounds.csv")

    # CSVファイルが既に存在する場合は上書きモード "w" で開く
    with open(csv_file, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([image_link])  # データを書き込む

# 「次へ」ボタンが押されたときの処理
def launch_syokihaiti():
    root.destroy()  # メインウィンドウを閉じる
    subprocess.run(["python", "mainsys/button_mover.py"])

# 「次へ」ボタンを作成
next_button = tk.Button(root, text="次へ", command=launch_syokihaiti)
next_button.pack()

# ファイル選択ボタンを作成
select_button = tk.Button(root, text="背景画像を選択", command=change_background)
select_button.pack()

# 初期背景を表示
update_background()

# Tkinterのメインループを実行
root.mainloop()
