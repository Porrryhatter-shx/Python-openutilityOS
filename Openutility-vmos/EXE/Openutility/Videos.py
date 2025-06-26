import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("视频播放器")
        self.root.geometry("800x600")

        self.video_frame = tk.Frame(self.root)
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.video_frame, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.play_button = tk.Button(self.root, text="打开视频", command=self.open_video)
        self.play_button.pack(pady=10)

        self.video_path = None

    def open_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("视频文件", "*.mp4;*.avi;*.mov;*.mkv")])
        if self.video_path:
            self.play_video()

    def play_video(self):
        if self.video_path:
            # 这里可以使用第三方库来播放视频，例如opencv或其他
            messagebox.showinfo("播放", f"正在播放: {os.path.basename(self.video_path)}")
            # 这里添加视频播放逻辑

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()