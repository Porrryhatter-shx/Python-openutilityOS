import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
from PIL import Image, ImageTk
import threading
import fnmatch
#pip install pillow



class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero文件资源管理器")
        self.root.geometry("1000x600")

        # 创建菜单栏
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # 文件菜单
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="打开文件夹", command=self.open_directory)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

        # 操作菜单
        action_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="操作", menu=action_menu)
        action_menu.add_command(label="复制", command=self.copy_item)
        action_menu.add_command(label="移动", command=self.move_item)
        action_menu.add_command(label="删除", command=self.delete_item)
        action_menu.add_command(label="搜索", command=self.search_files)
        action_menu.add_command(label="预览", command=self.preview_file)

        # 创建列表框显示文件和文件夹
        self.listbox = tk.Listbox(self.root, width=100, height=20)
        self.listbox.pack(pady=20, fill=tk.BOTH, expand=True)

        # 绑定双击事件
        self.listbox.bind("<Double-1>", self.on_double_click)

        # 当前路径
        self.current_path = os.getcwd()
        self.update_listbox()

        # 搜索功能相关
        self.search_frame = None
        self.search_entry = None
        self.search_results = []

    def update_listbox(self):
        """更新列表框内容"""
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, "..")  # 添加返回上级目录的选项
        for item in os.listdir(self.current_path):
            self.listbox.insert(tk.END, item)

    def open_directory(self):
        """打开一个文件夹"""
        path = filedialog.askdirectory()
        if path:
            self.current_path = path
            self.update_listbox()

    def on_double_click(self, event):
        """处理双击事件"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            selected_item = self.listbox.get(index)
            if selected_item == "..":
                self.current_path = os.path.dirname(self.current_path)
            else:
                new_path = os.path.join(self.current_path, selected_item)
                if os.path.isdir(new_path):
                    self.current_path = new_path
                else:
                    messagebox.showinfo("文件信息", f"文件路径: {new_path}")
            self.update_listbox()

    def copy_item(self):
        """复制文件或文件夹"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            selected_item = self.listbox.get(index)
            if selected_item == "..":
                messagebox.showwarning("警告", "不能复制上级目录")
                return
            source_path = os.path.join(self.current_path, selected_item)
            target_path = filedialog.askdirectory(title="选择目标文件夹")
            if target_path:
                try:
                    if os.path.isdir(source_path):
                        shutil.copytree(source_path, os.path.join(target_path, selected_item))
                    else:
                        shutil.copy2(source_path, target_path)
                    messagebox.showinfo("成功", "复制完成")
                except Exception as e:
                    messagebox.showerror("错误", f"复制失败: {e}")

    def move_item(self):
        """移动文件或文件夹"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            selected_item = self.listbox.get(index)
            if selected_item == "..":
                messagebox.showwarning("警告", "不能移动上级目录")
                return
            source_path = os.path.join(self.current_path, selected_item)
            target_path = filedialog.askdirectory(title="选择目标文件夹")
            if target_path:
                try:
                    shutil.move(source_path, target_path)
                    messagebox.showinfo("成功", "移动完成")
                    self.update_listbox()
                except Exception as e:
                    messagebox.showerror("错误", f"移动失败: {e}")

    def delete_item(self):
        """删除文件或文件夹"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            selected_item = self.listbox.get(index)
            if selected_item == "..":
                messagebox.showwarning("警告", "不能删除上级目录")
                return
            item_path = os.path.join(self.current_path, selected_item)
            if os.path.isdir(item_path):
                response = messagebox.askyesno("确认", f"是否删除文件夹 '{selected_item}' 及其内容？")
                if response:
                    try:
                        shutil.rmtree(item_path)
                        messagebox.showinfo("成功", "文件夹删除成功")
                        self.update_listbox()
                    except Exception as e:
                        messagebox.showerror("错误", f"删除文件夹失败: {e}")
            else:
                response = messagebox.askyesno("确认", f"是否删除文件 '{selected_item}'？")
                if response:
                    try:
                        os.remove(item_path)
                        messagebox.showinfo("成功", "文件删除成功")
                        self.update_listbox()
                    except Exception as e:
                        messagebox.showerror("错误", f"删除文件失败: {e}")

    def search_files(self):
        """搜索文件"""
        if self.search_frame:
            self.search_frame.destroy()
        self.search_frame = tk.Toplevel(self.root)
        self.search_frame.title("搜索文件")
        self.search_frame.geometry("400x300")

        tk.Label(self.search_frame, text="搜索关键词:").pack(pady=10)
        self.search_entry = tk.Entry(self.search_frame, width=40)
        self.search_entry.pack(pady=10)
        tk.Button(self.search_frame, text="开始搜索", command=self.start_search).pack(pady=10)

        self.search_results = tk.Listbox(self.search_frame, width=60, height=10)
        self.search_results.pack(pady=10)

    def start_search(self):
        """开始搜索"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("警告", "请输入搜索关键词")
            return

        self.search_results.delete(0, tk.END)
        threading.Thread(target=self.perform_search, args=(keyword,), daemon=True).start()

    def perform_search(self, keyword):
        """执行搜索"""
        for root, dirs, files in os.walk(self.current_path):
            for file in files:
                if fnmatch.fnmatch(file.lower(), f"*{keyword.lower()}*"):
                    self.search_results.insert(tk.END, os.path.join(root, file))

    def preview_file(self):
        """预览文件"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            selected_item = self.listbox.get(index)
            if selected_item == "..":
                messagebox.showwarning("警告", "不能预览上级目录")
                return
            file_path = os.path.join(self.current_path, selected_item)
            if os.path.isfile(file_path):
                self.show_file_preview(file_path)
            else:
                messagebox.showwarning("警告", "不能预览文件夹")

    def show_file_preview(self, file_path):
        """显示文件预览"""
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in ['.txt', '.log', '.py', '.java', '.cpp', '.h']:
            self.preview_text_file(file_path)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            self.preview_image_file(file_path)
        else:
            messagebox.showwarning("警告", "不支持的文件类型")

    def preview_text_file(self, file_path):
        """预览文本文件"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            preview_window = tk.Toplevel(self.root)
            preview_window.title(f"预览: {os.path.basename(file_path)}")
            preview_window.geometry("600x400")
            text_area = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD)
            text_area.pack(fill=tk.BOTH, expand=True)
            text_area.insert(tk.INSERT, content)
            text_area.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件: {e}")

    def preview_image_file(self, file_path):
        """预览图片文件"""
        try:
            image = Image.open(file_path)
            image.thumbnail((600, 400))  # 缩放图片
            photo = ImageTk.PhotoImage(image)
            preview_window = tk.Toplevel(self.root)
            preview_window.title(f"预览: {os.path.basename(file_path)}")
            label = tk.Label(preview_window, image=photo)
            label.image = photo  # 保存对PhotoImage的引用
            label.pack()
        except Exception as e:
            messagebox.showerror("错误", f"无法打开图片: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorer(root)
    root.mainloop()

