import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime

class ZeroCalendar:
    def __init__(self, root):
        self.root = root
        self.root.title("ZeroCalendar")
        self.root.geometry("400x400")
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        self.setup_ui()
        self.update_calendar()
    
    def setup_ui(self):
        # 顶部控制面板
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.prev_button = ttk.Button(
            control_frame, text="<", width=5, command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.month_year_label = ttk.Label(
            control_frame, text="", font=('Arial', 12))
        self.month_year_label.pack(side=tk.LEFT, expand=True)
        
        self.next_button = ttk.Button(
            control_frame, text=">", width=5, command=self.next_month)
        self.next_button.pack(side=tk.RIGHT, padx=5)
        
        # 日历显示区域
        self.calendar_frame = ttk.Frame(self.root)
        self.calendar_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 添加星期标题
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(weekdays):
            label = ttk.Label(self.calendar_frame, text=day, 
                             font=('Arial', 10, 'bold'), anchor="center")
            label.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
            self.calendar_frame.grid_columnconfigure(i, weight=1)
    
    def update_calendar(self):
        # 更新月份和年份显示
        month_name = calendar.month_name[self.current_month]
        self.month_year_label.config(text=f"{month_name} {self.current_year}")
        
        # 清除旧的日历日期
        for widget in self.calendar_frame.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()
        
        # 获取当月日历数据
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        # 显示日期
        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day != 0:  # 0表示非当月日期
                    day_label = ttk.Label(
                        self.calendar_frame, 
                        text=str(day), 
                        relief=tk.RIDGE,
                        anchor="center"
                    )
                    
                    # 如果是今天，高亮显示
                    today = datetime.now()
                    if (day == today.day and 
                        self.current_month == today.month and 
                        self.current_year == today.year):
                        day_label.config(background="#b3e6ff")
                    
                    day_label.grid(
                        row=week_num, 
                        column=day_num, 
                        sticky="nsew", 
                        padx=2, 
                        pady=2
                    )
        
        # 配置行权重
        for i in range(1, len(cal)+1):
            self.calendar_frame.grid_rowconfigure(i, weight=1)
    
    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()
    
    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = ZeroCalendar(root)
    root.mainloop()