import datetime
import time
import tkinter as tk
import winsound
from tkinter import messagebox, ttk

class ZeroClocks(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zero Clock")
        self.geometry("400x500")
        self.resizable(False, False)  # 禁止调整窗口大小
        self.alarms = []
        
        # 设置应用图标（如果有）
        try:
            self.iconbitmap('clock.ico')  # 替换为您的图标文件路径
        except:
            pass
        
        # 创建主界面容器
        self.create_widgets()
        self.update_clock()
        
        # 设置窗口关闭时的处理
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """窗口关闭时的确认"""
        if messagebox.askokcancel("退出", "确定要退出Zero Clock吗？"):
            self.destroy()

    def create_widgets(self):
        # 主时钟显示
        self.clock_label = tk.Label(self, font=('Arial', 40), fg='blue')
        self.clock_label.pack(pady=20)

        # 日期显示
        self.date_label = tk.Label(self, font=('Arial', 20))
        self.date_label.pack()

        # 创建功能选项卡
        self.notebook = ttk.Notebook(self)

        # 闹钟界面
        self.alarm_frame = ttk.Frame(self.notebook)
        self.create_alarm_tab()

        # 计时器界面
        self.timer_frame = ttk.Frame(self.notebook)
        self.create_timer_tab()

        # 秒表界面
        self.stopwatch_frame = ttk.Frame(self.notebook)
        self.create_stopwatch_tab()

        self.notebook.add(self.alarm_frame, text="闹钟")
        self.notebook.add(self.timer_frame, text="计时器")
        self.notebook.add(self.stopwatch_frame, text="秒表")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

    def update_clock(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d %A")
        self.clock_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.check_alarms()
        self.after(1000, self.update_clock)

    #--------------------闹钟功能--------------------
    def create_alarm_tab(self):
        tk.Label(self.alarm_frame, text="设置闹钟(HH:MM)").pack(pady=5)

        # 使用StringVar验证输入
        self.alarm_var = tk.StringVar()
        self.alarm_entry = tk.Entry(self.alarm_frame, textvariable=self.alarm_var)
        self.alarm_entry.pack(pady=5)
        
        # 添加输入提示
        self.alarm_entry.insert(0, "例如: 08:30")
        self.alarm_entry.bind("<FocusIn>", lambda e: self.alarm_entry.delete(0, "end") if self.alarm_entry.get() == "例如: 08:30" else None)

        set_button = tk.Button(self.alarm_frame, text="设置闹钟", command=self.set_alarm)
        set_button.pack(pady=5)

        # 添加闹钟列表滚动条
        scrollbar = tk.Scrollbar(self.alarm_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.alarm_listbox = tk.Listbox(self.alarm_frame, yscrollcommand=scrollbar.set)
        self.alarm_listbox.pack(pady=5, fill='both', expand=True)
        
        scrollbar.config(command=self.alarm_listbox.yview)

        del_button = tk.Button(self.alarm_frame, text="删除选中", command=self.delete_alarm)
        del_button.pack(pady=4)

    def set_alarm(self):
        alarm_time = self.alarm_entry.get()
        try:
            # 验证时间格式
            datetime.datetime.strptime(alarm_time, "%H:%M")
            if alarm_time in self.alarms:
                messagebox.showwarning("警告", "该闹钟已存在！")
                return
                
            self.alarms.append(alarm_time)
            self.alarms.sort()  # 按时间排序
            self.alarm_listbox.delete(0, tk.END)  # 清空后重新插入
            for alarm in self.alarms:
                self.alarm_listbox.insert(tk.END, alarm)
            self.alarm_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("错误", "时间格式应为 HH:MM")

    def delete_alarm(self):
        selected = self.alarm_listbox.curselection()
        if selected:
            self.alarm_listbox.delete(selected[0])
            del self.alarms[selected[0]]

    def check_alarms(self):
        current = datetime.datetime.now().strftime("%H:%M")
        for alarm in self.alarms:
            if current == alarm:
                # 使用线程播放声音，避免阻塞UI
                import threading
                def play_sound():
                    for _ in range(3):  # 播放3次
                        winsound.Beep(1000, 1000)
                        time.sleep(1)
                
                threading.Thread(target=play_sound).start()
                messagebox.showinfo("闹钟", f"时间到！现在是 {alarm}")
                self.alarms.remove(alarm)
                self.alarm_listbox.delete(0, tk.END)
                for a in self.alarms:
                    self.alarm_listbox.insert(tk.END, a)

    #--------------------计时器功能--------------------
    def create_timer_tab(self):
        self.timer_running = False
        self.timer_remaining = 0

        tk.Label(self.timer_frame, text="设置分钟数:").pack(pady=5)

        # 验证输入只能是数字
        vcmd = (self.register(self.validate_number), '%P')
        self.timer_entry = tk.Entry(self.timer_frame, validate="key", validatecommand=vcmd)
        self.timer_entry.pack(pady=5)

        self.timer_label = tk.Label(self.timer_frame, font=('Arial', 24))
        self.timer_label.pack(pady=10)

        btn_frame = tk.Frame(self.timer_frame)
        btn_frame.pack(pady=5)

        self.start_btn = tk.Button(btn_frame, text="开始", command=self.start_timer)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="重置", command=self.reset_timer).pack(side=tk.LEFT)

    def validate_number(self, P):
        """验证输入是否为数字"""
        if P == "" or P.isdigit():
            return True
        return False

    def start_timer(self):
        if not self.timer_running:
            try:
                minutes = int(self.timer_entry.get())
                if minutes <= 0:
                    messagebox.showerror("错误", "请输入大于0的数字")
                    return
                    
                self.timer_remaining = minutes * 60
                self.timer_running = True
                self.start_btn.config(text="暂停")
                self.update_timer()
            except ValueError:
                messagebox.showerror("错误", "请输入有效数字")
        else:
            self.timer_running = False
            self.start_btn.config(text="继续")

    def update_timer(self):
        if self.timer_running and self.timer_remaining > 0:
            mins, secs = divmod(self.timer_remaining, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.timer_remaining -= 1
            self.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.start_btn.config(text="开始")
            if self.timer_remaining == 0:
                # 计时结束时播放声音
                import threading
                def play_sound():
                    for _ in range(3):
                        winsound.Beep(1000, 500)
                        time.sleep(0.5)
                
                threading.Thread(target=play_sound).start()
                messagebox.showinfo("计时器", "时间到！")
                self.timer_label.config(text="00:00")

    def reset_timer(self):
        self.timer_running = False
        self.timer_remaining = 0
        self.timer_label.config(text="00:00")
        self.start_btn.config(text="开始")
        self.timer_entry.delete(0, tk.END)

    #--------------------秒表功能--------------------
    def create_stopwatch_tab(self):
        self.stopwatch_running = False
        self.start_time = None
        self.elapsed = 0
        self.laps = []

        self.stopwatch_label = tk.Label(self.stopwatch_frame, font=('Arial', 24))
        self.stopwatch_label.pack(pady=20)

        btn_frame = tk.Frame(self.stopwatch_frame)
        btn_frame.pack(pady=10)

        self.sw_start_btn = tk.Button(btn_frame, text="开始", command=self.sw_start_stop)
        self.sw_start_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="重置", command=self.sw_reset).pack(side=tk.LEFT)
        
        tk.Button(btn_frame, text="计次", command=self.record_lap).pack(side=tk.LEFT, padx=5)

        # 计次列表
        self.lap_listbox = tk.Listbox(self.stopwatch_frame, height=5)
        self.lap_listbox.pack(pady=10, fill='both', expand=True)

    def sw_start_stop(self):
        if not self.stopwatch_running:
            self.start_time = time.time() - self.elapsed
            self.stopwatch_running = True
            self.sw_start_btn.config(text="停止")
            self.update_stopwatch()
        else:
            self.stopwatch_running = False
            self.sw_start_btn.config(text="继续")

    def update_stopwatch(self):
        if self.stopwatch_running:
            self.elapsed = time.time() - self.start_time
            mins, secs = divmod(int(self.elapsed), 60)
            hours, mins = divmod(mins, 60)
            msec = int((self.elapsed - int(self.elapsed)) * 100)
            self.stopwatch_label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}.{msec:02d}")
            self.after(10, self.update_stopwatch)

    def sw_reset(self):
        self.stopwatch_running = False
        self.elapsed = 0
        self.stopwatch_label.config(text="00:00:00.00")
        self.sw_start_btn.config(text="开始")
        self.lap_listbox.delete(0, tk.END)
        self.laps = []

    def record_lap(self):
        if self.stopwatch_running or self.elapsed > 0:
            lap_time = self.stopwatch_label.cget("text")
            self.laps.append(lap_time)
            self.lap_listbox.insert(tk.END, f"计次 {len(self.laps)}: {lap_time}")

if __name__ == "__main__":
    #root=tk.Tk()
    app = ZeroClocks()
    app.mainloop()
