import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
try:
    import cv2
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
import cv2


class ZeroCamera:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero Camera")
        
        # 摄像头状态
        self.camera = None
        self.camera_running = False
        self.current_frame = None
        
        # 照片保存目录
        self.photos_dir = "zero_photos"
        self.create_photos_dir()
        
        # 界面缩放因子
        self.scale_factor = 1.0
        
        # 创建界面
        self.create_widgets()
        
        # 默认摄像头分辨率
        self.camera_width = 640
        self.camera_height = 480
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_photos_dir(self):
        """创建保存照片的目录"""
        if not os.path.exists(self.photos_dir):
            os.makedirs(self.photos_dir)
    
    def generate_filename(self):
        """生成基于时间戳的文件名"""
        now = datetime.now()
        return os.path.join(self.photos_dir, f"zero_photo_{now.strftime('%Y%m%d_%H%M%S')}.jpg")
    
    def create_widgets(self):
        """创建GUI界面"""
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 视频显示区域
        self.video_label = ttk.Label(self.main_frame)
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # 控制按钮框架
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # 开始/停止按钮
        self.start_stop_btn = ttk.Button(
            self.control_frame, 
            text="启动摄像头", 
            command=self.toggle_camera
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 拍照按钮
        self.capture_btn = ttk.Button(
            self.control_frame, 
            text="拍照", 
            command=self.take_photo,
            state=tk.DISABLED
        )
        self.capture_btn.pack(side=tk.LEFT, padx=5)
        
        # 设置按钮
        self.settings_btn = ttk.Button(
            self.control_frame, 
            text="设置", 
            command=self.show_settings
        )
        self.settings_btn.pack(side=tk.RIGHT, padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪")
        self.status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X)
        
    def toggle_camera(self):
        """切换摄像头状态"""
        if self.camera_running:
            self.stop_camera()
        else:
            self.start_camera()
    
    def start_camera(self):
        """启动摄像头"""
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
            
            self.camera_running = True
            self.start_stop_btn.config(text="停止摄像头")
            self.capture_btn.config(state=tk.NORMAL)
            self.status_var.set("摄像头已启动")
            
            # 开始视频流线程
            self.video_thread = threading.Thread(target=self.update_video, daemon=True)
            self.video_thread.start()
        except Exception as e:
            messagebox.showerror("错误", f"无法启动摄像头: {str(e)}")
    
    def stop_camera(self):
        """停止摄像头"""
        self.camera_running = False
        if self.camera:
            self.camera.release()
        self.start_stop_btn.config(text="启动摄像头")
        self.capture_btn.config(state=tk.DISABLED)
        self.status_var.set("摄像头已停止")
        
        # 清除视频显示
        self.video_label.config(image='')
        self.video_label.image = None
    
    def update_video(self):
        """更新视频流"""
        while self.camera_running:
            ret, frame = self.camera.read()
            if ret:
                self.current_frame = frame
                # 转换颜色空间 BGR -> RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # 调整大小
                if self.scale_factor != 1.0:
                    frame = cv2.resize(frame, None, fx=self.scale_factor, fy=self.scale_factor)
                
                # 转换为PIL Image
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # 更新显示
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)
            else:
                self.status_var.set("无法获取摄像头画面")
                break
    
    def take_photo(self):
        """拍照"""
        if self.current_frame is not None:
            filename = self.generate_filename()
            try:
                # 保存照片
                cv2.imwrite(filename, self.current_frame)
                
                # 显示拍照效果
                self.video_label.config(relief=tk.SUNKEN)
                self.root.after(200, lambda: self.video_label.config(relief=tk.FLAT))
                
                self.status_var.set(f"照片已保存: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"无法保存照片: {str(e)}")
    
    def show_settings(self):
        """显示设置对话框"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.resizable(False, False)
        
        # 分辨率设置
        ttk.Label(settings_window, text="分辨率:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.resolution_var = tk.StringVar()
        self.resolution_var.set(f"{self.camera_width}x{self.camera_height}")
        resolution_combo = ttk.Combobox(
            settings_window, 
            textvariable=self.resolution_var,
            values=["320x240", "640x480", "800x600", "1024x768", "1280x720"],
            state="readonly"
        )
        resolution_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # 显示缩放
        ttk.Label(settings_window, text="显示缩放:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.scale_var = tk.StringVar()
        self.scale_var.set(f"{self.scale_factor*100:.0f}%")
        scale_combo = ttk.Combobox(
            settings_window, 
            textvariable=self.scale_var,
            values=["50%", "75%", "100%", "125%", "150%"],
            state="readonly"
        )
        scale_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # 保存目录
        ttk.Label(settings_window, text="照片保存目录:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        dir_frame = ttk.Frame(settings_window)
        dir_frame.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.dir_var = tk.StringVar()
        self.dir_var.set(os.path.abspath(self.photos_dir))
        ttk.Entry(dir_frame, textvariable=self.dir_var, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(dir_frame, text="浏览...", command=lambda: self.browse_directory(settings_window)).pack(side=tk.RIGHT)
        
        # 按钮框架
        button_frame = ttk.Frame(settings_window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame, 
            text="保存", 
            command=lambda: self.save_settings(settings_window)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="取消", 
            command=settings_window.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def browse_directory(self, parent):
        """浏览选择保存目录"""
        dir_path = filedialog.askdirectory(parent=parent, initialdir=self.photos_dir)
        if dir_path:
            self.dir_var.set(dir_path)
    
    def save_settings(self, settings_window):
        """保存设置"""
        try:
            # 解析分辨率
            width, height = map(int, self.resolution_var.get().split('x'))
            self.camera_width = width
            self.camera_height = height
            
            # 解析缩放因子
            scale_str = self.scale_var.get().replace('%', '')
            self.scale_factor = float(scale_str) / 100.0
            
            # 更新保存目录
            self.photos_dir = self.dir_var.get()
            self.create_photos_dir()
            
            settings_window.destroy()
            self.status_var.set("设置已保存")
            
            # 如果摄像头正在运行，需要重启以应用新分辨率
            if self.camera_running:
                was_running = True
                self.stop_camera()
                if was_running:
                    self.start_camera()
        except Exception as e:
            messagebox.showerror("错误", f"无效设置: {str(e)}")
    
    def on_close(self):
        """关闭窗口时的清理工作"""
        if self.camera_running:
            self.stop_camera()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ZeroCamera(root)
    
    # 设置窗口大小
    root.geometry("800x600")
    root.minsize(400, 300)
    
    # 启动主循环
    root.mainloop()