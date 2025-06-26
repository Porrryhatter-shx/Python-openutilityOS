# FileExplorer.py

import os
import tkinter as tk
from tkinter import ttk, messagebox

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("文件管理器")
        self.root.geometry("600x400")

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.heading("#0", text="文件夹", anchor='w')
        self.populate_tree()

        self.tree.bind("<Double-1>", self.on_item_double_click)

    def populate_tree(self, parent=''):
        """Populate the tree view with files and directories."""
        for item in os.listdir(parent):
            path = os.path.join(parent, item)
            if os.path.isdir(path):
                node = self.tree.insert(parent, 'end', text=item, open=False)
                self.populate_tree(path)  # Recursively add subdirectories
            else:
                self.tree.insert(parent, 'end', text=item)

    def on_item_double_click(self, event):
        """Handle double-click event on tree items."""
        selected_item = self.tree.selection()
        if selected_item:
            item_text = self.tree.item(selected_item, "text")
            messagebox.showinfo("文件信息", f"您双击了: {item_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorer(root)
    root.mainloop()