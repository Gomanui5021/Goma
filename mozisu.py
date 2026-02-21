import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

ffmpeg_path = resource_path("ffmpeg.exe")

def select_input_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg")]
    )
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3", "*.mp3"), ("WAV", "*.wav")]
    )
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

def process_audio():
    input_file = input_entry.get()
    output_file = output_entry.get()
    text = text_entry.get("1.0", tk.END).strip()

    try:
        if not os.path.exists(input_file):
            raise Exception("入力ファイルが存在しません")

        if text == "":
            raise Exception("文章が空です")

        count = len(text)

        # 出力拡張子取得
        ext = os.path.splitext(output_file)[1].lower()

        if ext == ".mp3":
            codec = "libmp3lame"
        elif ext == ".wav":
            codec = "pcm_s16le"
        else:
            raise Exception("対応していない形式です")
        
        command = [
        ffmpeg_path,
        "-y",
        "-stream_loop", str(count - 1),
        "-i", input_file,
        "-c:a", codec,
        output_file
         ]
        
        result = subprocess.run(command)

        if result.returncode != 0:
            raise Exception("ffmpeg処理失敗")

        messagebox.showinfo("結果", f"成功：{count}回再生音声を作成しました")

    except Exception as e:
        messagebox.showerror("結果", f"失敗：{str(e)}")

#文字数
def update_char_count(event=None):
    text = text_entry.get("1.0", "end-1c")
    count = len(text)
    char_count_label.config(text=f"現在 {count} 文字")

# ===== GUI =====
root = tk.Tk()
root.title("文字数音声鳴らしツール")
root.geometry("500x400")

#アイコン
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

root.iconbitmap(resource_path("icon.ico"))

tk.Label(root, text="入力音声ファイル").pack()
input_entry = tk.Entry(root, width=50)
input_entry.pack()
tk.Button(root, text="参照", command=select_input_file).pack()

tk.Label(root, text="保存先ファイル").pack()
output_entry = tk.Entry(root, width=50)
output_entry.pack()
tk.Button(root, text="保存先選択", command=select_output_file).pack()

tk.Label(root, text="文章入力").pack()
text_entry = tk.Text(root, width=50, height=6)
text_entry.pack()
text = text_entry.get("1.0", "end-1c")
char_count_label = tk.Label(root, text="現在 0 文字")
char_count_label.pack()
text_entry.bind("<KeyRelease>", update_char_count)

tk.Label(root, text="1文字あたりのミリ秒").pack()
ms_entry = tk.Entry(root)
ms_entry.insert(0, "80")
ms_entry.pack()

tk.Button(root, text="実行", command=process_audio).pack(pady=10)

root.mainloop()