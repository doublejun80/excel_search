import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

class ExcelSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("엑셀 검색 도구")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        self.excel_file = None
        self.df = None
        self.results = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # 프레임 구성
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        middle_frame = ttk.Frame(self.root, padding="10")
        middle_frame.pack(fill=tk.BOTH, expand=True)
        
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # 파일 선택 영역
        ttk.Label(top_frame, text="엑셀 파일:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.file_path_var, width=50).grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        ttk.Button(top_frame, text="파일 선택", command=self.select_file).grid(row=0, column=2, padx=5)
        
        # 검색 영역
        ttk.Label(top_frame, text="검색어:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=10)
        
        self.search_var = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.search_var, width=50).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=10)
        
        ttk.Button(top_frame, text="검색", command=self.search).grid(row=1, column=2, padx=5, pady=10)
        
        top_frame.columnconfigure(1, weight=1)
        
        # 결과 트리뷰
        self.result_tree = ttk.Treeview(middle_frame, columns=("시트", "행", "열", "값"), show="headings")
        self.result_tree.heading("시트", text="시트")
        self.result_tree.heading("행", text="행")
        self.result_tree.heading("열", text="열")
        self.result_tree.heading("값", text="값")
        
        self.result_tree.column("시트", width=100)
        self.result_tree.column("행", width=60)
        self.result_tree.column("열", width=100)
        self.result_tree.column("값", width=500)
        
        scrollbar_y = ttk.Scrollbar(middle_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ttk.Scrollbar(middle_frame, orient=tk.HORIZONTAL, command=self.result_tree.xview)
        self.result_tree.configure(xscrollcommand=scrollbar_x.set)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 상태 표시줄
        self.status_var = tk.StringVar()
        self.status_var.set("준비됨")
        ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="엑셀 파일 선택",
            filetypes=[("Excel 파일", "*.xlsx *.xls")]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            self.excel_file = file_path
            self.status_var.set(f"파일 로드됨: {Path(file_path).name}")
            self.clear_results()
        
    def search(self):
        if not self.excel_file:
            messagebox.showerror("오류", "먼저 엑셀 파일을 선택해주세요.")
            return
        
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showerror("오류", "검색어를 입력해주세요.")
            return
        
        try:
            self.status_var.set("검색 중...")
            self.root.update_idletasks()
            self.clear_results()
            
            # 엑셀 파일의 모든 시트를 읽기
            xl = pd.ExcelFile(self.excel_file)
            sheet_names = xl.sheet_names
            
            for sheet in sheet_names:
                try:
                    df = pd.read_excel(self.excel_file, sheet_name=sheet)
                    
                    # 데이터프레임에서 검색
                    for row_idx, row in df.iterrows():
                        for col_idx, value in enumerate(row):
                            if pd.notna(value) and str(search_term).lower() in str(value).lower():
                                col_name = df.columns[col_idx]
                                self.results.append((sheet, row_idx + 2, col_name, value))
                except Exception as e:
                    messagebox.showwarning("경고", f"시트 '{sheet}' 읽는 중 오류 발생: {str(e)}")
            
            # 결과 표시
            for result in self.results:
                self.result_tree.insert("", tk.END, values=result)
            
            if not self.results:
                self.status_var.set(f"검색 결과 없음: '{search_term}'")
            else:
                self.status_var.set(f"총 {len(self.results)}개의 결과를 찾았습니다.")
                
        except Exception as e:
            messagebox.showerror("오류", f"검색 중 오류가 발생했습니다: {str(e)}")
            self.status_var.set("오류 발생")
    
    def clear_results(self):
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.results = []

def main():
    root = tk.Tk()
    app = ExcelSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 