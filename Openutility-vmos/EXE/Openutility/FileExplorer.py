# FileExplorer.py

import tkinter as tk
from tkinter import ttk, messagebox
import os

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("文件管理器")
        self.root.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.heading("#0", text="文件夹和文件", anchor='w')

        self.populate_tree()

        self.tree.bind("<Double-1>", self.on_item_double_click)

    def populate_tree(self, path="."):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                self.tree.insert("", "end", item_path, text=item, open=False)
            else:
                self.tree.insert("", "end", item_path, text=item)

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_path = selected_item[0]
            if os.path.isdir(item_path):
                self.tree.delete(*self.tree.get_children(item_path))
                self.populate_tree(item_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorer(root)
    root.mainloop()