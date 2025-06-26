'''
name 应用名称
version 版本
developer 开发者
description 简介
installed 安装情况
command 定义函数-打开


'''
import tkinter as tk
from tkinter import messagebox

class ZeroStore:
    def __init__(self, root, add_app_callback=None):
        self.root = root
        self.add_app_callback = add_app_callback  # 用于回调添加应用到桌面
        self.root.title("ZeroStore")
        self.root.geometry("800x600")

        # 应用数据
        self.apps = [
            {"name": "支付宝", "version": "5.1", "developer": "maker", 
             "description": "这是一个测试支付宝Ailpay (makerpay)应用", 
             "installed": False, "command": self.open_alipay},
            
            {"name": "Python IDE", "version": "Python3.10", 
             "developer": "Zero", 
             "description": "适用于Zero OS的简洁PythonIDE", 
             "installed": False, "command": self.open_python_ide},
            
            {"name": "WiFi管理", "version": "1.0", "developer": "other", 
             "description": "无线网络管理工具", "installed": False, "command": self.open_wifi},
        ]

        self.create_widgets()

    def create_widgets(self):
        #创建应用列表框
        self.listbox = tk.Listbox(self.root, width=60, height=15)
        self.listbox.pack(pady=20)

        #将应用信息插入到列表框中
        for app in self.apps:
            self.listbox.insert(tk.END, f"{app['name']} - {app['version']} - {app['developer']}")

        #创建应用详细信息标签
        self.detail_frame = tk.LabelFrame(self.root, text="应用详细信息", padx=10, pady=10)
        self.detail_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.name_label = tk.Label(self.detail_frame, text="名称: ")
        self.name_label.grid(row=0, column=0, sticky="w")
        self.name_value = tk.Label(self.detail_frame, text="")
        self.name_value.grid(row=0, column=1, sticky="w")

        self.version_label = tk.Label(self.detail_frame, text="版本: ")
        self.version_label.grid(row=1, column=0, sticky="w")
        self.version_value = tk.Label(self.detail_frame, text="")
        self.version_value.grid(row=1, column=1, sticky="w")

        self.developer_label = tk.Label(self.detail_frame, text="开发者: ")
        self.developer_label.grid(row=2, column=0, sticky="w")
        self.developer_value = tk.Label(self.detail_frame, text="")
        self.developer_value.grid(row=2, column=1, sticky="w")

        self.description_label = tk.Label(self.detail_frame, text="描述: ")
        self.description_label.grid(row=3, column=0, sticky="w")
        self.description_value = tk.Label(self.detail_frame, text="", wraplength=400)
        self.description_value.grid(row=3, column=1, sticky="w")

        #创建安装.卸载按钮
        self.install_button = tk.Button(self.root, text="安装", command=self.install_app)
        self.install_button.pack(side=tk.LEFT, padx=20)

        self.uninstall_button = tk.Button(self.root, text="卸载", command=self.uninstall_app)
        self.uninstall_button.pack(side=tk.RIGHT, padx=20)

        #绑定列表框的选择事件
        self.listbox.bind("<<ListboxSelect>>", self.update_details)

    def update_details(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            app = self.apps[index]

            self.name_value.config(text=app["name"])
            self.version_value.config(text=app["version"])
            self.developer_value.config(text=app["developer"])
            self.description_value.config(text=app["description"])

    def install_app(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            app = self.apps[index]
            if not app["installed"]:
                app["installed"] = True
                messagebox.showinfo("Zero system", f"{app['name']} 已安装")
                
                #调用回调函数将应用添加到桌面
                if self.add_app_callback:
                    self.add_app_callback(app["name"], app["command"])
            else:
                messagebox.showwarning("ZeroStore", f"{app['name']} 已安装")

    def uninstall_app(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            app = self.apps[index]
            if app["installed"]:
                app["installed"] = False
                messagebox.showinfo("Zero system", f"{app['name']} 已卸载")
            else:
                messagebox.showwarning("ZeroStore", f"{app['name']} 未安装，无法卸载")

    #应用打开方法
    def open_alipay(self):
        from ailpaytk import AlipayApp
        
    def open_python_ide(self):
        messagebox.showinfo("Python IDLE", "准备Python...")
        from PythonIDLE import CodeEditor

    def open_wifi(self):
        messagebox.showinfo("WiFi管理", "WiFi   ")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZeroStore(root)
    root.mainloop()
    
    
    
    
    
    
#2025331