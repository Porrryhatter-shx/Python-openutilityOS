'''
Openutility 所要安装的第三方库:
    pip install +:
    tkinterweb
    pygments
    pillow
'''
import subprocess
import sys
import time
from tkinter import ttk, messagebox
import tkinter as tk
import math

from ZeroClocks import ZeroClocks
print('准备Openutility环境...')
print('Openutility                                                                       -done')
print('Openutility                                                                       -start')

try:
    import tkinterweb
    import pygments
    from PIL import Image, ImageTk
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinterweb"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygments"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    import tkinterweb
    import pygments
    import math
    from PIL import Image, ImageTk
    import platform
print('Openutility                                                                   -starting')


class BootAnimation:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete

        #创建全屏窗口
        self.window = tk.Toplevel(root)
        self.window.attributes('-fullscreen',  True)
        self.window.overrideredirect(True)#移除窗口装饰

        #黑色背景
        self.canvas = tk.Canvas(self.window,  bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH,  expand=True)

        #Logo
        try:
            self.logo_img = Image.open("Openutility-removebg-preview.png")
            self.logo_img = self.logo_img.resize((300,  300))
            self.logo_img = ImageTk.PhotoImage(self.logo_img)
            self.logo = self.canvas.create_image(
                self.window.winfo_screenwidth()//2,
                self.window.winfo_screenheight()//2 - 100,
                image=self.logo_img,
                state=tk.HIDDEN
            )
        except:
            self.logo = None
            self.logo_text = self.canvas.create_text(
                self.window.winfo_screenwidth()//2,
                self.window.winfo_screenheight()//2 - 50,
                text="Openutility-OS",
                font=('Arial', 48, 'bold'),
                fill='white',
                state=tk.HIDDEN
            )

        #添加文字
        self.loading_text = self.canvas.create_text(
            self.window.winfo_screenwidth()//2,
            self.window.winfo_screenheight()//2 + 100,
            text='正在启动系统',
            font=('Arial', 12),
            fill='white',
            state=tk.HIDDEN
        )

        #初始化状态文本
        self.status_text = self.canvas.create_text(
            self.window.winfo_screenwidth()//2,
            self.window.winfo_screenheight()//2 + 160,
            text="",
            font=('Arial', 10),
            fill='white',
            state=tk.HIDDEN
        )

        #模拟初始化步骤
        self.init_steps = [
            ("正在初始化显示系统...", 500),
            ("加载系统组件...", 800),
            ("准备桌面环境...", 1200),
            ("启动Openutility服务...", 1500)
        ]

        #启动动画序列
        self.start_animation()

    def start_animation(self):
        '''启动完整的动画序列'''
        #渐显Logo
        if self.logo:
            self.fade_in(self.logo,  duration=1000)
        else:
            self.fade_in(self.logo_text,  duration=1000)

        #渐显加载文本
        self.fade_in(self.loading_text,  delay=500, duration=800)
        #更新状态文本
        self.update_status()
        #启动进度条动画
        self.animate_loading()

    def fade_in(self, item, duration=1000, delay=0):
        '''渐显动画效果'''
        self.canvas.itemconfig(item,  state=tk.NORMAL)
        if isinstance(item, int):#canvas对象
            for i in range(0, 101, 5):
                alpha = i/100
                color = self._rgb_to_hex((300, 300, 300, alpha))
        else:    #图片简化处理
            self.root.after(delay, lambda: self.canvas.itemconfig(
                item,  state=tk.NORMAL))

    def animate_loading(self):
        '''加载进度条动画'''
        #创建进度条背景
        self.progress_bg = self.canvas.create_rectangle(
            self.window.winfo_screenwidth()//2 - 100,
            self.window.winfo_screenheight()//2 + 130,
            self.window.winfo_screenwidth()//2 + 100,
            self.window.winfo_screenheight()//2 + 140,
            fill='#333333',
            outline=''
        )

        #创建进度条前景
        self.progress = self.canvas.create_rectangle(
            self.window.winfo_screenwidth()//2 - 100,
            self.window.winfo_screenheight()//2 + 130,
            self.window.winfo_screenwidth()//2 - 100,
            self.window.winfo_screenheight()//2 + 140,
            fill='#4CAF50',
            outline=''
        )

        #动画进度
        def update_progress(progress=0):
            if progress <= 100:
                width = 200 * (progress/100)
                self.canvas.coords(
                    self.progress,
                    self.window.winfo_screenwidth()//2 - 100,
                    self.window.winfo_screenheight()//2 + 130,
                    self.window.winfo_screenwidth()//2 - 100 + width,
                    self.window.winfo_screenheight()//2 + 140
                )
                self.root.after(20,  update_progress, progress + 1)
            else:
                self.fade_out()

        update_progress()

    def fade_out(self):
        '''完成后淡出效果'''
        for i in range(100, -1, -5):
            alpha = i/100
            bg_color = self._rgb_to_hex((0, 0, 0, alpha))
            self.window.after(20, lambda c=bg_color: self.window.config(bg=c))
        self.window.after(500,  self.on_complete)
        self.window.after(1000,  self.window.destroy)

    def update_status(self, step=0):
        '''更新初始化状态文本'''
        if step < len(self.init_steps):
            text, delay = self.init_steps[step]
            self.canvas.itemconfig(
                self.status_text,  text=text, state=tk.NORMAL)
            self.root.after(delay,  self.update_status,  step + 1)

    def _rgb_to_hex(self, rgba):
        '''RGB转十六进制颜色'''
        return "#%02x%02x%02x" % rgba[:3]


class Openutility:
    '''
    Openutility-OS 主类
    模拟桌面操作系统，包含任务栏、窗口管理、系统应用等功能
    '''
    def __init__(self, root):
        '''初始化操作系统界面'''
        self.root = root
        self.root.withdraw()#先隐藏主窗口
        BootAnimation(root, self.on_boot_complete)#显示开机动画

    def on_boot_complete(self):
        '''开机动画完成后的回调函数 '''
        #显示主窗口并初始化系统
        self.root.deiconify()
        self.root.title('Openutility-OS 1.0')
        self.root.geometry('1024x1024')
        self.root.attributes('-fullscreen', True)


        #锁屏相关变量
        self.is_locked = False
        self.lock_screen = None
        self.idle_time = 0
        self.lock_timeout = 300
        self.password = "0955"
            
        self.canvas = tk.Canvas(self.root, bg='#2d2d2d')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        #初始化系统组件
        self.create_taskbar()
        self.windows=[]
        self.running_apps={}


        #系统应用列表
        self.system_apps = [
            ('计算器', self.open_calculator),
            ('文件管理器', self.open_file_explorer),
            ('浏览器', self.open_browser),
            ('日历', self.open_ZeroCalendar),
            ('时钟', self.open_ZeroClocks),
            ('设置', self.open_Settings),
            ('应用商店', self.open_ZeroStore),
            ('视频播放器', self.open_VideoPlayer),
            ('草稿本', self.open_caogaoben),
            ('关于', self.open_gy),
            ('')
        ]

        #第三方应用列表
        self.third_party_apps = {}
        #创建桌面图标
        self.create_desktop_icons()
        #系统托盘时钟初始化
        self.update_clock()

        #绑定鼠标和键盘事件
        self.root.bind("<Motion>", self.reset_idle_timer)
        self.root.bind("<Key>", self.reset_idle_timer)

        #启动空闲检测定时器
        self.check_idle_time()

    def create_taskbar(self):
        '''
        创建任务栏
            包含开始按钮、任务列表区域和系统托盘区域
        '''
        #任务栏主框架
        self.taskbar = tk.Frame(self.root, bg='#BEBEBE', height=60,
                               relief=tk.SUNKEN, bd=1)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        #开始按钮区域
        start_btn_frame = tk.Frame(self.taskbar, bg='#1a1a1a')
        start_btn_frame.pack(side=tk.LEFT, padx=(5, 0))

        start_btn = tk.Button(start_btn_frame, text="开始",
                             bg='#1a1a1a', fg='white',
                             activebackground='#9D9D9D',
                             bd=0, command=self.show_start_menu)

        start_btn.pack(side=tk.LEFT, padx=2)

        #任务列表区域
        self.task_list = tk.Frame(self.taskbar, bg='#1a1a1a')
        self.task_list.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        #系统托盘区域
        self.tray_frame = tk.Frame(self.taskbar, bg='#1a1a1a')
        self.tray_frame.pack(side=tk.RIGHT)
        #时钟显示
        self.tray_icon = tk.Label(self.tray_frame, text=time.strftime('%H:%M:%S '),
                                 bg='#1a1a1a', fg='white', font=('Segoe UI', 10))
        self.tray_icon.pack(side=tk.RIGHT, padx=5)

        #锁屏
        self.lock_icon = tk.Label(self.tray_frame, text="锁屏",
                                bg='#1a1a1a', fg='white',font=('Segoe UI', 10),
                                cursor="hand2")
        self.lock_icon.pack(side=tk.RIGHT, padx=5)
        self.lock_icon.bind("<Button-1>", lambda e: self.lock_screen_func())

    def focus_window(self, window):
        '''
        将指定窗口带到最前面并获取焦点        
        参数:
            window: 要聚焦的窗口对象
        '''
        window.lift()    #将窗口置于顶层
        window.focus_set()    #设置键盘焦点到该窗口

    def create_window(self, title, content):
        
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("400x300")  #默认大小
        self.windows.append(window)  #添加到窗口管理列表

        #窗口标题栏-深背景
        title_bar = tk.Frame(window, bg='#333', height=30)
                
        #窗口标题标签
        title_label = tk.Label(title_bar, text=title, bg='#333', fg='white')

        #打包标题栏组件
        title_bar.pack(side=tk.TOP, fill=tk.X)
        title_label.pack(side=tk.LEFT, padx=10)
        #close_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        #窗口内容区域
        content_frame = ttk.Frame(window)
        content(content_frame)  # 调用内容生成函数填充窗口内容
        content_frame.pack(fill=tk.BOTH, expand=True)

        #窗口拖动实现
        def start_move(event):
            #记录拖动开始时的鼠标位置
            window.x = event.x
            window.y = event.y

        def do_move(event):
            #根据鼠标移动计算新窗口位置
            deltax = event.x - window.x
            deltay = event.y - window.y
            x = window.winfo_x() + deltax
            y = window.winfo_y() + deltay
            window.geometry(f"+{x}+{y}")

        #绑定标题栏的鼠标事件实现拖动
        title_bar.bind("<Button-1>", start_move)
        title_bar.bind("<B1-Motion>", do_move)

        return

    def update_clock(self):
        '''
        更新系统时钟显示
        每秒自动更新一次
        '''
        self.tray_icon.config(text=time.strftime("%Y/%M/%D  %H:%M:%S"))#更新时间文本
        self.root.after(1000, self.update_clock)#1秒后再次调用自身

    def create_desktop_icons(self):
        '''创建桌面图标'''
        #清空现有图标
        for child in self.canvas.winfo_children():
            child.destroy()
            
        #系统应用图标(左侧)
        for i, (name, cmd) in enumerate(self.system_apps):
            icon = tk.Label(self.canvas, text=name,
                          fg='white', bg='#2d2d2d',
                          font=('Helvetica', 12))
            icon.bind("<Double-Button-1>", lambda e, c=cmd: c())
            self.canvas.create_window(50, 50+i*40, window=icon)
            
        #第三方应用图标(右侧)
        for i, (name, cmd) in enumerate(self.third_party_apps.items()):
            icon = tk.Label(self.canvas, text=name,
                          fg='white', bg='#2d2d2d',
                          font=('Helvetica', 12))
            icon.bind("<Double-Button-1>", lambda e, c=cmd: c())
            self.canvas.create_window(150, 50+i*40, window=icon)

    def add_third_party_app(self, app_name, app_command):
        '''
        添加第三方应用到桌面
        :param app_name: 应用名称
        :param app_command: 点击时执行的命令
        '''
        self.third_party_apps[app_name] = app_command
        self.create_desktop_icons()

    def open_calculator(self):
        '''计算器
         for  朱**
        '''
        def calc_content(frame):
            #结果显示框

            display_var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=display_var,
                              font=('Arial', 14), justify='right')
            entry.pack(fill=tk.X,  padx=5, pady=5)

            #按钮布局
            btn_frame = ttk.Frame(frame)
            buttons = [(',', 'sqrt(', 'latus(', 'sin(', 'cos('),
                       ('//', '%', '**', '(', ')'),
                       ('7', '8', '9', 'AC', 'pi'),
                       ('4', '5', '6', '*', '/'),
                       ('1', '2', '3', '+', '-'),
                       ('0', '.', '*(10**', 'self.r', '=')
                       ]

            #按钮点击处理
            def on_click(char):
                def latus(a, b):
                    c = a**(1/b)
                    return c

                def sin(a):
                    c = math.sin(math.radians(a))
                    return c

                def cos(a):
                    c = math.cos(math.radians(a))
                    return c
                if char == '=':

                    print(display_var.get())
                    try:
                        self.r = eval(display_var.get())

                        display_var.set(str(self.r))

                    except Exception as e:
                        display_var.set(e)

                elif char == 'AC':
                    display_var.set('')
                else:
                    display_var.set(display_var.get() + char)

            #创建计算器按钮
            for r, row in enumerate(buttons):
                for c, char in enumerate(row):
                    btn = ttk.Button(btn_frame, text=char, width=5,
                                     command=lambda ch=char: on_click(ch))
                    btn.grid(row=r,  column=c, padx=2, pady=2)

            btn_frame.pack()

        self.create_window("计算器", calc_content)

    def open_file_explorer(self):
        '''文件管理器'''
        from FileExplorer import FileExplorer
        root = tk.Tk()
        app = FileExplorer(root)
        root.mainloop()

    def open_browser(self):
        '''浏览器'''
        from Browser import SimpleBrowser
        root = tk.Tk()
        app = SimpleBrowser(root)
        root.mainloop()
    
    def open_ZeroCalendar(self):
        '''日历'''
        from zero_calendar import ZeroCalendar
        root = tk.Tk()
        app = ZeroCalendar(root)
        root.mainloop()
        
    def open_ZeroClocks(self):
        '''时钟'''
        from ZeroClocks import ZeroClocks
        root = tk.Tk()
        app = ZeroClocks()
        app.mainloop()

    def open_caogaoben(self):
        '''草稿本'''
        from caogaoben import zerocgb
        root = tk.Tk()
        app = zerocgb(root)
        root.mainloop()


    def open_Settings(self):
        window=tk.Toplevel(self.root)
        window.title('设置')
        window.geometry('500x700')
        window.resizable(False, False)
        window.configure(bg="white")

        label=tk.Label(
            window,
            text='系统设置',
            font=('Arial', 25, 'bold'),
            fg='black',
            bg='white',
            padx=20,
            pady=5
        )
        label.pack(pady=10)

        #锁屏时间设置
        lock_label = tk.Label(window, text='锁屏超时时间(秒)', font=('Arial', 14), bg='white')
        lock_label.pack(pady=10)
        lock_var = tk.IntVar(value=self.lock_timeout)
        def set_lock_time():
            self.lock_timeout = lock_var.get()
        lock_entry = tk.Entry(window, textvariable=lock_var, font=("Arial", 12), width=10)
        lock_entry.pack()
        lock_btn = tk.Button(window, text="设置锁屏时间", command=set_lock_time)
        lock_btn.pack(pady=5)

        #密码修改
        pw_label = tk.Label(window, text='修改锁屏密码', font=('Arial', 14), bg='white')
        pw_label.pack(pady=10)
        pw_var = tk.StringVar()
        def set_password():
            if pw_var.get():
                self.password = pw_var.get()
                messagebox.showinfo('System', '密码已修改')
        pw_entry = tk.Entry(window, textvariable=pw_var, font=('Arial', 12), show='*')
        pw_entry.pack()
        pw_btn = tk.Button(window, text='修改密码', command=set_password)
        pw_btn.pack(pady=5)

        # 恢复出厂设置
        reset_btn = tk.Button(window, text='恢复出厂设置', command=self.hf, bg='#ff5555', fg='white', font=('Arial', 12))
        reset_btn.pack(pady=40)

    def hf(self):
        '''恢复出厂设置'''
        if messagebox.askyesno('System', '恢复出厂设置...'):
            time.sleep(1.6)
            self.root.destroy()
            Openutility(tk.Tk()).root.mainloop()
            time.sleep(3)

    def open_gy(self):
        root = tk.Tk()
        root.title('-About')
        root.geometry('450x300')
        label = tk.Label(
            root,
            text='Openutility--VMOS \n      1.0  2025',
            font=("Arial", 35, "bold"),#字体
            fg="black",#文字颜色
            bg="white",#背景色
            padx=20,#水平内边距
            pady=5#垂直内边距
        )
        label.pack(pady=10)#pady设置上下边距
        button = tk.Button(root, text='已是最新版本')
        button.pack(pady=40)
        
    def open_ZeroStore(self):
        '''打开应用商店'''
        store_window = tk.Toplevel(self.root)
        from zerostore import ZeroStore
        store = ZeroStore(store_window, self.add_third_party_app)
        
    def open_VideoPlayer(self):
        from Videos import VideoPlayer
        
    def show_start_menu(self):
        #显示开始菜单
        menu = tk.Menu(self.root,  tearoff=0)
        menu.add_command(label=' 计算器', command=self.open_calculator)
        menu.add_command(label=' 文件管理器', command=self.open_file_explorer)
        menu.add_command(label=' 浏览器', command=self.open_browser)
        menu.add_command(label=' 日历', command=self.open_ZeroCalendar)
        menu.add_command(label=' 时钟', command=self.open_ZeroClocks)
        menu.add_command(label=' 设置', command=self.open_Settings)
        menu.add_command(label=' 应用商店', command=self.open_ZeroStore)
        menu.add_command(label=' 视频播放器', command=self.open_VideoPlayer)
        menu.add_command(label=' 草稿', command=self.open_caogaoben)
        menu.add_separator()
        menu.add_command(label=' 锁屏', command=self.lock_screen_func)
        menu.add_command(label=' 关机', command=self.shutdown)
        menu.add_command(label=' 重启', command=self.restart)
        menu.add_separator()
        menu.add_command(label='Openutility--VMOS1.0 \n  2025',command=self.open_gy)

        #在开始按钮下方显示菜单
        menu.post(self.root.winfo_x() + 10,
                  self.root.winfo_y() + self.root.winfo_height()-40)

    def shutdown(self):
        '''关机'''
        if messagebox.askyesno('System', '确定关机'):#选择框
            time.sleep(2)
            sys.exit()

    def restart(self):
        '''重启'''
        if messagebox.askyesno('System', '系统重启'):
            time.sleep(1.6)
            self.root.destroy()
            #重启
            Openutility(tk.Tk()).root.mainloop()
            
    def lock_screen_func(self):
        '''锁屏'''
        if self.is_locked:
            return
            
        self.is_locked = True
        
        #创建锁屏窗口
        self.lock_screen = tk.Toplevel(self.root)
        self.lock_screen.attributes('-fullscreen', True)
        self.lock_screen.attributes('-topmost', True)  # 确保锁屏窗口在最前面
        
        #锁屏背景
        lock_bg = tk.Frame(self.lock_screen, bg='#BEBEBE')
        lock_bg.pack(fill=tk.BOTH, expand=True)
        
        #锁屏内容
        lock_content = tk.Frame(lock_bg, bg='white')
        lock_content.place(relx=0.5, rely=0.5, anchor='center')
        
        #显示时间
        time_label = tk.Label(lock_content, 
                            text=time.strftime('%H:%M'), 
                            font=('Arial', 48), 
                            fg='white', 
                            bg='black')
        time_label.pack(pady=20)

        #密码输入框
        pw_frame = tk.Frame(lock_content, bg='#2d2d2d')
        pw_frame.pack(pady=30)
        
        tk.Label(pw_frame, 
                text='输入密码以解锁', 
                font=('Arial', 12), 
                fg='white', 
                bg='black').pack(side=tk.LEFT)
                
        pw_entry = tk.Entry(pw_frame, 
                           show="*", 
                           font=('Arial', 12), 
                           width=15)
        pw_entry.pack(side=tk.LEFT, padx=5)
        pw_entry.focus_set()#自动聚焦到密码输入框
        
        #解锁按钮
        def attempt_unlock():
            if pw_entry.get() == self.password:
                self.unlock_screen()
            else:
                messagebox.showerror("错误", "密码不正确")
                pw_entry.delete(0, tk.END)
                
        unlock_btn = tk.Button(lock_content, 
                              text="解锁", 
                              command=attempt_unlock,
                              font=('Arial', 12),
                              width=10)
        unlock_btn.pack(pady=10)
        
        #绑定回车键解锁
        self.lock_screen.bind('<Return>', lambda e: attempt_unlock())
        
        #更新时间显示
        def update_lock_time():
            time_label.config(text=time.strftime('%H:%M'))
            time_label.config(text=time.strftime('%Y年%m月%D日%A'))
            self.lock_screen.after(1000, update_lock_time)
            
        update_lock_time()
        
        #隐藏所有其他窗口
        for window in self.windows:
            window.withdraw()
            
    def unlock_screen(self):
        #解锁屏幕
        if not self.is_locked:
            return
            
        self.is_locked = False
        self.lock_screen.destroy()
        self.lock_screen = None
        
        #恢复所有窗口
        for window in self.windows:
            window.deiconify()
            
        #重置空闲计时器
        self.reset_idle_timer()   
    def reset_idle_timer(self, event=None):
        self.idle_time = 0
        
    def check_idle_time(self):
        '''检查空闲时间-锁屏'''
        if not self.is_locked and self.lock_timeout > 0:
            self.idle_time += 1
            if self.idle_time >= self.lock_timeout:
                self.lock_screen_func()
                
        self.root.after(1000, self.check_idle_time)#每秒检查一次


if __name__ == "__main__":
    #启动程序
    root = tk.Tk()
    os = Openutility(root)
    root.mainloop()



#2025/7/17