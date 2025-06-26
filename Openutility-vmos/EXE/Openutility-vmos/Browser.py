# Browser.py

import tkinter as tk
from tkinter import ttk
import webbrowser

class SimpleBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Browser")
        self.root.geometry("800x600")

        self.url_entry = ttk.Entry(self.root, width=70)
        self.url_entry.pack(pady=10)

        self.go_button = ttk.Button(self.root, text="Go", command=self.open_url)
        self.go_button.pack(pady=5)

        self.text_area = tk.Text(self.root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)

    def open_url(self):
        url = self.url_entry.get()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleBrowser(root)
    root.mainloop()