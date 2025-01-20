import customtkinter as ctk
import requests
import json
import time
import random
from threading import Thread
from datetime import datetime
import csv
from tkinter import messagebox, filedialog
from config_manager import ConfigManager

class GoogleSearchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 初始化配置管理器
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()
        
        # 添加停止标志
        self.stop_search = False

        # 配置窗口
        self.title("Google URL采集器 ")
        self.geometry("800x600")
        
        # 设置主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_widgets()
        self.load_saved_config()

    def create_widgets(self):
        # 创建主框架
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # API配置区域
        api_frame = ctk.CTkFrame(main_frame)
        api_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(api_frame, text="API Key:").pack(side="left", padx=5)
        self.api_key_entry = ctk.CTkEntry(api_frame, width=200)
        self.api_key_entry.pack(side="left", padx=5)

        ctk.CTkLabel(api_frame, text="Search Engine ID:").pack(side="left", padx=5)
        self.cx_entry = ctk.CTkEntry(api_frame, width=200)
        self.cx_entry.pack(side="left", padx=5)

        # 搜索配置区域
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(search_frame, text="关键词:").pack(side="left", padx=5)
        self.keyword_entry = ctk.CTkEntry(search_frame, width=200)
        self.keyword_entry.pack(side="left", padx=5)

        ctk.CTkLabel(search_frame, text="起始页:").pack(side="left", padx=5)
        self.start_page = ctk.CTkEntry(search_frame, width=50)
        self.start_page.pack(side="left", padx=5)

        ctk.CTkLabel(search_frame, text="结束页:").pack(side="left", padx=5)
        self.end_page = ctk.CTkEntry(search_frame, width=50)
        self.end_page.pack(side="left", padx=5)

        # 按钮区域
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(padx=10, pady=10, fill="x")

        self.search_button = ctk.CTkButton(button_frame, text="开始搜索", command=self.start_search)
        self.search_button.pack(side="left", padx=5)

        self.stop_button = ctk.CTkButton(button_frame, text="停止采集", command=self.stop_search_process)
        self.stop_button.pack(side="left", padx=5)
        self.stop_button.configure(state="disabled")

        self.clear_button = ctk.CTkButton(button_frame, text="清空结果", command=self.clear_results)
        self.clear_button.pack(side="left", padx=5)

        self.export_button = ctk.CTkButton(button_frame, text="导出结果", command=self.export_results)
        self.export_button.pack(side="left", padx=5)
        self.export_button.configure(state="disabled")

        # 进度条
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(padx=10, pady=10, fill="x")
        self.progress_bar.set(0)

        # 结果显示区域
        self.result_text = ctk.CTkTextbox(main_frame, height=300)
        self.result_text.pack(padx=10, pady=10, fill="both", expand=True)

        # 存储结果
        self.results = []

    def load_saved_config(self):
        # 加载保存的配置
        self.api_key_entry.insert(0, self.config.get("api_key", ""))
        self.cx_entry.insert(0, self.config.get("cx", ""))
        self.keyword_entry.insert(0, self.config.get("last_keyword", ""))
        self.start_page.insert(0, self.config.get("start_page", "1"))
        self.end_page.insert(0, self.config.get("end_page", "1"))

    def save_current_config(self):
        # 保存当前配置
        self.config_manager.update_config(
            api_key=self.api_key_entry.get(),
            cx=self.cx_entry.get(),
            last_keyword=self.keyword_entry.get(),
            start_page=self.start_page.get(),
            end_page=self.end_page.get()
        )

    def clear_results(self):
        self.result_text.delete("0.0", "end")
        self.results = []
        self.progress_bar.set(0)
        self.export_button.configure(state="disabled")

    def stop_search_process(self):
        self.stop_search = True
        self.stop_button.configure(state="disabled")
        self.result_text.insert("end", "\n搜索已停止...\n")

    def search_worker(self):
        self.results = []
        keyword = self.keyword_entry.get()
        start_page = int(self.start_page.get())
        end_page = int(self.end_page.get())
        api_key = self.api_key_entry.get()
        cx = self.cx_entry.get()

        # 重置停止标志
        self.stop_search = False

        # 保存当前配置
        self.save_current_config()

        total_pages = end_page - start_page + 1
        current_page = 0

        for page_num in range(start_page, end_page + 1):
            if self.stop_search:
                break

            start = (page_num - 1) * 10 + 1
            url = f"https://www.googleapis.com/customsearch/v1"
            params = {
                "key": api_key,
                "cx": cx,
                "q": keyword,
                "start": start,
                "num": 10
            }

            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    for item in items:
                        link = item["link"]
                        self.results.append(link)
                        self.result_text.insert("end", f"{link}\n")
                else:
                    self.result_text.insert("end", f"请求失败，状态码：{response.status_code}\n")
            except Exception as e:
                self.result_text.insert("end", f"错误：{str(e)}\n")

            current_page += 1
            progress = current_page / total_pages
            self.progress_bar.set(progress)
            time.sleep(random.uniform(1, 2))

        self.search_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.export_button.configure(state="normal")
        
        if not self.stop_search:
            messagebox.showinfo("完成", "搜索完成！")
        self.stop_search = False

    def start_search(self):
        self.result_text.delete("0.0", "end")
        self.search_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.export_button.configure(state="disabled")
        Thread(target=self.search_worker, daemon=True).start()

    def export_results(self):
        if not self.results:
            messagebox.showwarning("警告", "没有可导出的结果！")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"google_search_results_{timestamp}"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            initialfile=default_filename
        )
        
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['URL'])
                for url in self.results:
                    writer.writerow([url])
            messagebox.showinfo("成功", "结果已成功导出！")

if __name__ == "__main__":
    app = GoogleSearchApp()
    app.mainloop()