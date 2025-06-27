import tkinter as tk
from tkinter import ttk
from urllib.parse import urlparse, urlunparse
import socket

# 安装 tkinterweb 库：pip install tkinterweb
from tkinterweb import HtmlFrame

class SimpleBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("浏览器")
        self.root.geometry("800x600")
        
        self.history = []
        self.current_index = -1
        
        self.create_widgets()
        
    def create_widgets(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.back_button = ttk.Button(toolbar, text="←", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=2)
        
        self.forward_button = ttk.Button(toolbar, text="→", command=self.go_forward)
        self.forward_button.pack(side=tk.LEFT, padx=2)
        
        self.refresh_button = ttk.Button(toolbar, text="刷新", command=self.refresh)
        self.refresh_button.pack(side=tk.LEFT, padx=2)
        
        self.home_button = ttk.Button(toolbar, text="主页", command=self.go_home)
        self.home_button.pack(side=tk.LEFT, padx=2)
        
        self.address_bar = ttk.Entry(toolbar, width=50)
        self.address_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.address_bar.bind("<Return>", self.navigate)
        
        self.go_button = ttk.Button(toolbar, text="Go", command=self.navigate)
        self.go_button.pack(side=tk.LEFT, padx=2)
        
        # 使用 HtmlFrame 替代 Text 组件来显示网页
        self.content_area = HtmlFrame(self.root)
        self.content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.home_url = "https://www.bing.com"
        self.address_bar.insert(0, self.home_url)
        
    def navigate(self, event=None):
        url = self.address_bar.get()
        if not self.is_valid_url(url):
            search_engine = "https://www.bing.com/search?q="
            url = search_engine + url.replace(" ", "+")
        
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index+1]
        self.history.append(url)
        self.current_index += 1
        
        self.load_url(url)
        
    def load_url(self, url):
        self.address_bar.delete(0, tk.END)
        self.address_bar.insert(0, url)
        self.content_area.load_url(url)  # 使用 HtmlFrame 加载网页
        
    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            url = self.history[self.current_index]
            self.load_url(url)
            
    def go_forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            url = self.history[self.current_index]
            self.load_url(url)
            
    def refresh(self):
        if self.current_index >= 0 and len(self.history) > 0:
            url = self.history[self.current_index]
            self.load_url(url)
            
    def go_home(self):
        self.load_url(self.home_url)
        
    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleBrowser(root)
    root.mainloop()
