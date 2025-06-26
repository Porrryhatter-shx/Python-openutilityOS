import tkinter as tk
from tkinter import filedialog, messagebox, font
from tkinter.ttk import Frame, Button, Separator,Style
import tkinter.colorchooser
import os

class zerocgb:
    def __init__(self, root):
        self.root = root
        self.root.title('Zero 草稿')
        self.root.geometry('800x600')
        
        # 当前打开的文件
        self.current_file = None
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.status_bar = tk.Label(root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建文本编辑区域
        self.text_area = tk.Text(root, wrap="word", undo=True, maxundo=-1)
        self.text_area.pack(expand=True, fill="both")

        # 添加滚动条
        scroll_bar = tk.Scrollbar(self.text_area)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_bar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scroll_bar.set)
        
        # 绑定快捷键
        self.bind_shortcuts()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="打开", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="保存", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="另存为", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.exit_app)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="撤销", command=self.undo_text, accelerator="Ctrl+Z")
        edit_menu.add_command(label="重做", command=self.redo_text, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="剪切", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="复制", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="粘贴", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="全选", command=self.select_all, accelerator="Ctrl+A")
        menubar.add_cascade(label="编辑", menu=edit_menu)
        
        # 格式菜单
        format_menu = tk.Menu(menubar, tearoff=0)
        format_menu.add_command(label="字体", command=self.change_font)
        format_menu.add_command(label="颜色", command=self.change_color)
        menubar.add_cascade(label="格式", menu=format_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_toolbar(self):
        # 创建主工具栏容器
        toolbar_container = tk.Frame(self.root, bg='#3498db')  # 蓝色背景
        toolbar_container.pack(side=tk.TOP, fill=tk.X)
    
        # 创建实际工具栏（在容器内部）
        toolbar = Frame(toolbar_container, style='Toolbar.TFrame')
        toolbar.pack(pady=5)  # 添加一些内边距
    
        
    
        #文件操作按钮
        buttons = [
            ("新建", self.new_file),
            ("打开", self.open_file),
            ("保存", self.save_file),
            ("|", None),  #分隔线
            ("撤销", self.undo_text),
            ("重做", self.redo_text),
            ("|", None),
            ("剪切", self.cut_text),
            ("复制", self.copy_text),
            ("粘贴", self.paste_text),
            ("|", None),
            ("字体", self.change_font),
            ("颜色", self.change_color)
        ]
    #配置透明样式
        style = Style()
        style.configure('Toolbar.TFrame', background='#3498db')
        style.configure('Transparent.TButton', 
                       background='#3498db',   #与背景完全相同的蓝色
                       foreground='white',    #白色文字
                       borderwidth=0,        #无边框
                       relief=tk.FLAT,       #扁平样式
                       padding=2,
                       font=('Microsoft YaHei', 10))

        #移除悬停效果，保持颜色始终一致
        style.map('Transparent.TButton',
                  background=[('active', '#3498db')],    #悬停时保持相同颜色
                  foreground=[('active', 'white')])
    

        for text, command in buttons:
            if text == "|":
                Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=4, fill=tk.Y)
            else:
                btn = Button(toolbar, text=text, command=command, 
                        style='Transparent.TButton', width=4)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def bind_shortcuts(self):
        self.root.bind('<Control-z>', lambda event: self.undo_text())
        self.root.bind('<Control-y>', lambda event: self.redo_text())
        self.root.bind('<Control-n>', lambda event: self.new_file())
        self.root.bind('<Control-o>', lambda event: self.open_file())
        self.root.bind('<Control-s>', lambda event: self.save_file())
        self.root.bind('<Control-x>', lambda event: self.cut_text())
        self.root.bind('<Control-c>', lambda event: self.copy_text())
        self.root.bind('<Control-v>', lambda event: self.paste_text())
        self.root.bind('<Control-a>', lambda event: self.select_all())
    
    def undo_text(self):
        try:
            self.text_area.edit_undo()
            self.status_bar.config(text="撤销操作")
        except tk.TclError:
            self.status_bar.config(text="没有可撤销的操作", fg="red")
    
    def redo_text(self):
        try:
            self.text_area.edit_redo()
            self.status_bar.config(text="重做操作")
        except tk.TclError:
            self.status_bar.config(text="没有可重做的操作", fg="red")
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("简易Word处理器 - 未命名")
        self.status_bar.config(text="新建文件")
    
    def open_file(self):
    # 弹出文件选择对话框，限制文件类型（可扩展）
        file_path = filedialog.askopenfilename(
            title="选择要打开的文件",
            defaultextension=".txt",
            filetypes=[
                ("文本文档", "*.txt"),
                ("Markdown", "*.md"),
                ("Python文件", "*.py"),
                ("配置文件", "*.ini *.conf"),
                ("所有文件", "*.*")
            ],
            initialdir=os.path.expanduser("~\\Documents")  # 默认打开用户文档目录
        )
    
        if not file_path:  # 用户取消选择
            return
        
        try:
            # 自动检测文件编码（防止中文乱码）
            with open(file_path, "r", encoding=self.detect_encoding(file_path)) as file:
                content = file.read()
            
            # 清空并插入新内容（保留撤销历史）
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            
            # 更新状态
            self.current_file = file_path
            
            self.status_bar.config(text=f'已打开:{file_path}', fg="green")
        
            # 添加到最近打开文件列表
            
        
        except PermissionError:
            messagebox.showerror("错误", f'没有权限读取文件:\n{file_path}')
        except UnicodeDecodeError:
            messagebox.showerror("错误", "文件编码不兼容，请尝试其他编码")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件:\n{file_path}\n\n错误类型: {type(e).__name__}\n详细信息: {str(e)}")

    def detect_encoding(self, file_path):
        """尝试自动检测文件编码"""
        encodings = ['utf-8', 'gbk', 'gb18030', 'big5', 'latin1']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    f.read(1024)  # 只读取前1KB测试
                return enc
            except UnicodeDecodeError:
                continue
        return 'utf-8'  # 默认回退
    
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.status_bar.config(text=f"已保存: {self.current_file}")
            except Exception as e:
                messagebox.showerror("错误", f"无法保存文件:\n{str(e)}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文档", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.current_file = file_path
                self.root.title(f"简易Word处理器 - {os.path.basename(file_path)}")
                self.status_bar.config(text=f"已保存: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"无法保存文件:\n{str(e)}")
    
    def exit_app(self):
        if messagebox.askokcancel("退出", "确定要退出吗？"):
            self.root.destroy()
    
    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")
        self.status_bar.config(text="已剪切文本")
    
    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")
        self.status_bar.config(text="已复制文本")
    
    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")
        self.status_bar.config(text="已粘贴文本")
    
    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        self.status_bar.config(text="已全选")
    
    def change_font(self):
        # 获取当前字体设置
        current_font = font.Font(font=self.text_area['font'])
        
        # 创建字体选择对话框
        font_window = tk.Toplevel(self.root)
        font_window.title("字体设置")
        font_window.geometry("300x200")
        
        # 字体家族选择
        tk.Label(font_window, text="字体:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        font_family = tk.StringVar(value=current_font.actual()['family'])
        font_family_entry = tk.Entry(font_window, textvariable=font_family)
        font_family_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 字体大小选择
        tk.Label(font_window, text="大小:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        font_size = tk.IntVar(value=current_font.actual()['size'])
        font_size_entry = tk.Entry(font_window, textvariable=font_size)
        font_size_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 字体样式选择
        tk.Label(font_window, text="样式:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        font_weight = tk.StringVar(value=current_font.actual()['weight'])
        font_slant = tk.StringVar(value=current_font.actual()['slant'])
        
        bold_check = tk.Checkbutton(font_window, text="粗体", variable=font_weight, 
                                   onvalue="bold", offvalue="normal")
        bold_check.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        italic_check = tk.Checkbutton(font_window, text="斜体", variable=font_slant, 
                                     onvalue="italic", offvalue="roman")
        italic_check.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 应用按钮
        def apply_font():
            new_font = font.Font(
                family=font_family.get(),
                size=font_size.get(),
                weight=font_weight.get(),
                slant=font_slant.get()
            )
            self.text_area.configure(font=new_font)
            font_window.destroy()
            self.status_bar.config(text="字体已更改")
        
        apply_btn = tk.Button(font_window, text="应用", command=apply_font)
        apply_btn.grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)
    
    def change_color(self):
        """修改文本颜色，支持记忆上次选择的颜色"""
        try:
            # 获取当前文本颜色作为默认值
            current_color = self.text_area.cget('fg')
        
        # 弹出颜色选择对话框（记忆上次选择）
            
            color = tk.colorchooser.askcolor(
                title="选择文本颜色",
                initialcolor=current_color,  # 默认显示当前颜色
                parent=self.root  # 确保对话框在主窗口上方
            )
        
            if color[1]:  # 用户选择了颜色
            # 应用新颜色
                self.text_area.configure(fg=color[1])
            
            # 更新状态栏（显示十六进制和RGB值）
                rgb = tuple(int(x) for x in color[0])
                status_text = f"文本颜色: {color[1]} (RGB: {rgb[0]}, {rgb[1]}, {rgb[2]})"
                self.status_bar.config(text=status_text, fg=color[1])
            
            # 记录最近使用的颜色（可用于实现颜色历史）
                self.last_used_color = color[1]
            
        except Exception as e:
            messagebox.showerror("颜色错误", f"无法更改颜色:\n{str(e)}")
            self.status_bar.config(text="颜色更改失败", fg="red")
    
    def show_about(self):
        messagebox.showinfo("关于", "简易Word处理器\n版本 1.0\n使用Python Tkinter创建")

if __name__ == "__main__":
    root = tk.Tk()
    app = zerocgb(root)
    root.mainloop()
