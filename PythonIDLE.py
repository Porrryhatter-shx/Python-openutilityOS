import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import keyword
import re
import sys
import io
from traceback import format_exc

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python")
        self.root.geometry("1000x700")
        
        #创建菜单栏
        self.create_menu()
        
        #创建主界面
        self.create_interface()
        
        #配置语法高亮标签
        self.configure_tags()
        
        #绑定事件
        self.bind_events()
        
        self.current_file = None
        self.output_buffer = None
        self.original_stdout = None
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        #文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="打开", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="保存", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="另存为", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.exit_editor)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        #编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="撤销", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="重做", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="剪切", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="复制", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="粘贴", command=self.paste, accelerator="Ctrl+V")
        menubar.add_cascade(label="编辑", menu=edit_menu)
        
        #运行菜单
        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="运行", command=self.run_code, accelerator="F5")
        run_menu.add_command(label="检查语法", command=self.check_syntax)
        menubar.add_cascade(label="运行", menu=run_menu)
        
        self.root.config(menu=menubar)
    
    def create_interface(self):
        #创建主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        #创建编辑区域框架
        editor_frame = tk.Frame(main_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        #行号显示
        self.line_numbers = tk.Text(editor_frame, width=4, padx=5, pady=5, takefocus=0, 
                                  border=0, background='lightgrey', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        #文本编辑区域
        self.text_area = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.WORD, 
            undo=True,
            font=('Consolas', 12)  #使用等宽字体
        )
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        #创建输出区域框架
        output_frame = tk.LabelFrame(main_frame, text="输出", padx=5, pady=5)
        output_frame.pack(fill=tk.BOTH, expand=False, pady=(5, 0))
        
        #输出标签页
        self.output_notebook = ttk.Notebook(output_frame)
        self.output_notebook.pack(fill=tk.BOTH, expand=True)
        
        #控制台输出标签页
        self.console_output = scrolledtext.ScrolledText(
            self.output_notebook,
            wrap=tk.WORD,
            state='disabled',
            font=('Consolas', 10)
        )
        self.output_notebook.add(self.console_output, text="控制台")
        
        #错误输出标签页
        self.error_output = scrolledtext.ScrolledText(
            self.output_notebook,
            wrap=tk.WORD,
            state='disabled',
            font=('Consolas', 10),
            foreground='red'
        )
        self.output_notebook.add(self.error_output, text="错误")
        
        #状态栏
        self.status_bar = tk.Label(self.root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        #更新行号
        self.update_line_numbers()
    
    def configure_tags(self):
        #Python关键字
        self.text_area.tag_configure("keyword", foreground="blue", font=('Consolas', 12, 'bold'))
        #字符串
        self.text_area.tag_configure("string", foreground="green", font=('Consolas', 12))
        #注释
        self.text_area.tag_configure("comment", foreground="gray", font=('Consolas', 12))
        #数字
        self.text_area.tag_configure("number", foreground="orange", font=('Consolas', 12))
        #函数名
        self.text_area.tag_configure("function", foreground="purple", font=('Consolas', 12, 'bold'))
        #错误行
        self.text_area.tag_configure("error", background="red")
    
    def bind_events(self):
        #绑定快捷键
        self.root.bind_all("<Control-n>", lambda event: self.new_file())
        self.root.bind_all("<Control-o>", lambda event: self.open_file())
        self.root.bind_all("<Control-s>", lambda event: self.save_file())
        self.root.bind_all("<F5>", lambda event: self.run_code())
        
        #绑定文本修改事件
        self.text_area.bind("<KeyRelease>", self.on_key_release)
        self.text_area.bind("<Button-1>", self.update_line_numbers)
    
    def on_key_release(self, event=None):
        self.update_line_numbers()
        self.highlight_syntax()
    
    def update_line_numbers(self, event=None):
        #更新行号显示
        lines = self.text_area.get("1.0", tk.END).count("\n") + 1
        line_numbers_text = "\n".join(str(i) for i in range(1, lines + 1))
        
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state=tk.DISABLED)
    
    def highlight_syntax(self):
        #清除所有标签
        for tag in self.text_area.tag_names():
            if tag != "error":  # 保留错误标签
                self.text_area.tag_remove(tag, "1.0", tk.END)
        
        #获取文本内容
        text = self.text_area.get("1.0", tk.END)
        
        #高亮Python关键字
        for word in keyword.kwlist:
            self.highlight_pattern(r'\b%s\b' % word, "keyword")
        
        #高亮字符串
        self.highlight_pattern(r'"[^"]*"', "string")
        self.highlight_pattern(r"'[^']*'", "string")
        self.highlight_pattern(r'"""[^"]*"""', "string", flags=re.DOTALL)
        self.highlight_pattern(r"'''[^']*'''", "string", flags=re.DOTALL)
        
        #高亮注释
        self.highlight_pattern(r'#[^\n]*', "comment")
        
        #高亮数字
        self.highlight_pattern(r'\b\d+\b', "number")
        self.highlight_pattern(r'\b\d+\.\d+\b', "number")
        
        #高亮函数定义
        self.highlight_pattern(r'\bdef\s+(\w+)', "function", group=1)
        self.highlight_pattern(r'\bclass\s+(\w+)', "function", group=1)
    
    def highlight_pattern(self, pattern, tag, group=0, flags=0):
        text = self.text_area.get("1.0", tk.END)
        matches = re.finditer(pattern, text, flags)
        
        for match in matches:
            start = "1.0 + {} chars".format(match.start(group))
            end = "1.0 + {} chars".format(match.end(group))
            self.text_area.tag_add(tag, start, end)
    
    def clear_error_highlight(self):
        self.text_area.tag_remove("error", "1.0", tk.END)
        self.error_output.config(state=tk.NORMAL)
        self.error_output.delete("1.0", tk.END)
        self.error_output.config(state=tk.DISABLED)
    
    def highlight_error_line(self, line_number):
        self.clear_error_highlight()
        line_start = f"{line_number}.0"
        line_end = f"{line_number}.end"
        self.text_area.tag_add("error", line_start, line_end)
        self.text_area.see(line_start)
    
    def run_code(self):
        '''运行当前编辑器中的Python代码'''
        self.clear_error_highlight()
        self.clear_console()
        
        #获取代码
        code = self.text_area.get("1.0", tk.END)
        
        #重定向输出
        self.output_buffer = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.output_buffer
        
        try:
            #执行代码
            exec(code, {'__name__': '__main__'})
        except Exception as e:
            #捕获并显示错误
            error_msg = format_exc()
            self.show_error(error_msg)
            
            # 尝试提取错误行号
            match = re.search(r'File "<string>", line (\d+)', error_msg)
            if match:
                line_number = int(match.group(1))
                self.highlight_error_line(line_number)
        finally:
            #恢复标准输出
            sys.stdout = self.original_stdout
            self.original_stdout = None
            
            #显示输出内容
            output = self.output_buffer.getvalue()
            if output:
                self.show_output(output)
            self.output_buffer.close()
            self.output_buffer = None
    
    def check_syntax(self):
        #检查代码语法
        self.clear_error_highlight()
        code = self.text_area.get("1.0", tk.END)
        
        try:
            compile(code, "<string>", "exec")
            self.show_output("语法检查正确  无错误")
        except SyntaxError as e:
            error_msg = f"语法错误: {e.msg}\n在文件 {e.filename} 第 {e.lineno} 行"
            self.show_error(error_msg)
            self.highlight_error_line(e.lineno)
        except Exception as e:
            error_msg = f"错误: {str(e)}"
            self.show_error(error_msg)
    
    def clear_console(self):
        """清空控制台输出"""
        self.console_output.config(state=tk.NORMAL)
        self.console_output.delete("1.0", tk.END)
        self.console_output.config(state=tk.DISABLED)
    
    def show_output(self, text):
        """在控制台显示输出"""
        self.console_output.config(state=tk.NORMAL)
        self.console_output.insert(tk.END, text)
        self.console_output.config(state=tk.DISABLED)
        self.output_notebook.select(self.console_output)
    
    def show_error(self, text):
        """在错误窗口显示错误"""
        self.error_output.config(state=tk.NORMAL)
        self.error_output.insert(tk.END, text)
        self.error_output.config(state=tk.DISABLED)
        self.output_notebook.select(self.error_output)
    
    #文件操作函数
    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.current_file = None
        self.clear_error_highlight()
        self.clear_console()
        self.update_status("新建文件")
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python 文件", "*.py"), ("所有文件", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", content)
                    self.current_file = file_path
                    self.update_status(f"已打开{file_path}")
                    self.highlight_syntax()
                    self.clear_error_highlight()
                    self.clear_console()
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")
    
    def save_file(self):
        if self.current_file:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(self.current_file, "w") as file:
                    file.write(content)
                self.update_status(f"已保存: {self.current_file}")
            except Exception as e:
                messagebox.showerror("错误", f"无法保存文件:\n{str(e)}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", 
                                                filetypes=[("Python 文件", "*.py"), ("所有文件", "All")])
        if file_path:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(file_path, "w") as file:
                    file.write(content)
                self.current_file = file_path
                self.update_status(f"已保存: {file_path}")
            except Exception as e:
                messagebox.showerror("pythonIDLE", f"无法保存文件:\n{str(e)}")
    
    def exit_editor(self):
        if messagebox.askokcancel("PythonIDLE", "确定要退出吗？"):
            self.root.destroy()
    
    #编辑操作函数
    def undo(self):
        self.text_area.edit_undo()
    
    def redo(self):
        self.text_area.edit_redo()
    
    def cut(self):
        self.text_area.event_generate("<<Cut>>")
    
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
    
    def paste(self):
        self.text_area.event_generate("<<Paste>>")
    
    def update_status(self, message):
        self.status_bar.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()