import os
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Checkbutton, IntVar
from pathlib import Path

class CSVSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV 검색 도구")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        
        self.csv_file = None
        self.results = []
        self.headers = []
        self.header_vars = []  # 체크박스 변수 저장
        self.found_rows = []  # 검색 결과 저장용
        self.selected_columns = []  # 선택된 열 저장용
        
        self.setup_ui()
        
    def setup_ui(self):
        # 전체 프레임 구성
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 왼쪽 패널 (파일 선택, 검색, 조건 선택)
        left_panel = ttk.Frame(main_frame, padding="10", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)  # 크기 고정
        
        # 오른쪽 패널 (결과 표시)
        right_panel = ttk.Frame(main_frame, padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 상태 표시줄
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # 파일 선택 영역
        file_frame = ttk.LabelFrame(left_panel, text="파일 선택", padding="5")
        file_frame.pack(fill=tk.X, pady=5)
        
        file_entry_frame = ttk.Frame(file_frame)
        file_entry_frame.pack(fill=tk.X, pady=5)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_entry_frame, textvariable=self.file_path_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(file_frame, text="파일 선택", command=self.select_file).pack(fill=tk.X, padx=5, pady=5)
        
        # 인코딩 선택
        encoding_frame = ttk.Frame(file_frame)
        encoding_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(encoding_frame, text="인코딩:").pack(side=tk.LEFT, padx=5)
        
        self.encoding_var = tk.StringVar(value="cp949")
        encodings = ttk.Combobox(encoding_frame, textvariable=self.encoding_var, width=15)
        encodings['values'] = ('cp949', 'utf-8', 'utf-8-sig', 'euc-kr')
        encodings.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(encoding_frame, text="적용", command=self.reload_headers).pack(side=tk.RIGHT, padx=5)
        
        # 검색어 입력 영역
        search_frame = ttk.LabelFrame(left_panel, text="검색", padding="5")
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="검색어:").pack(anchor=tk.W, padx=5, pady=2)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(fill=tk.X, padx=5, pady=2)
        
        # 검색 버튼
        search_buttons_frame = ttk.Frame(search_frame)
        search_buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(search_buttons_frame, text="검색", command=self.search).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(search_buttons_frame, text="클립보드에 복사", command=self.copy_to_clipboard).pack(side=tk.RIGHT, padx=2)
        
        # 출력할 열 선택 영역
        self.condition_frame = ttk.LabelFrame(left_panel, text="출력할 열 선택", padding="5")
        self.condition_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 전체 선택/해제 체크박스
        select_all_frame = ttk.Frame(self.condition_frame)
        select_all_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.select_all_var = IntVar(value=1)
        self.select_all_cb = Checkbutton(
            select_all_frame, 
            text="전체 선택/해제", 
            variable=self.select_all_var,
            command=self.toggle_all_headers
        )
        self.select_all_cb.pack(anchor=tk.W)
        
        # 헤더 체크박스를 위한 스크롤 영역
        header_scroll_frame = ttk.Frame(self.condition_frame)
        header_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(header_scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 캔버스와 내부 프레임
        self.canvas = tk.Canvas(header_scroll_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.header_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.header_frame, anchor="nw")
        
        # 스크롤바 연결
        scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=scrollbar.set)
        
        # 캔버스 크기 조정
        self.header_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # 결과 프레임 - 트리뷰를 포함할 프레임
        result_frame_container = ttk.LabelFrame(right_panel, text="검색 결과", padding="5")
        result_frame_container.pack(fill=tk.BOTH, expand=True)
        
        # 결과 탐색 버튼 (좌우 이동)
        nav_buttons_frame = ttk.Frame(result_frame_container)
        nav_buttons_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(nav_buttons_frame, text="◀ 왼쪽", command=lambda: self.scroll_horizontal(-1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_buttons_frame, text="오른쪽 ▶", command=lambda: self.scroll_horizontal(1)).pack(side=tk.RIGHT, padx=5)
        
        # 트리뷰를 담을 내부 프레임
        self.result_frame = ttk.Frame(result_frame_container)
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 결과 트리뷰는 검색 시 동적으로 생성
        self.result_tree = None
        self.h_scrollbar = None  # 수평 스크롤바 참조 저장용
        
        # 상태 표시줄
        self.status_var = tk.StringVar()
        self.status_var.set("준비됨")
        ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)
        
        # 단축키 바인딩
        self.root.bind("<Control-c>", lambda event: self.copy_to_clipboard())
        self.root.bind("<Return>", lambda event: self.search())
        self.root.bind("<Left>", lambda event: self.scroll_horizontal(-1))
        self.root.bind("<Right>", lambda event: self.scroll_horizontal(1))
    
    def scroll_horizontal(self, direction):
        """트리뷰 수평 스크롤 (방향: -1=왼쪽, 1=오른쪽)"""
        if self.h_scrollbar and self.result_tree:
            # 현재 스크롤 위치
            current = self.h_scrollbar.get()
            
            # 스크롤 단위: 각 방향으로 20% 이동
            move_unit = 0.2 * direction
            
            # 새 위치 계산 (0.0 ~ 1.0 범위 제한)
            new_position = max(0.0, min(1.0, current[0] + move_unit))
            
            # xview_moveto는 0~1 사이의 위치로 스크롤
            self.result_tree.xview_moveto(new_position)
            
            # 현재 보이는 열 인덱스 표시
            visible_columns = self.get_visible_columns()
            if visible_columns:
                start_col, end_col = visible_columns
                total_cols = len(self.result_tree["columns"])
                self.status_var.set(
                    f"열 보기: {start_col+1}-{end_col+1} / {total_cols} "
                    f"({self.result_tree.heading(self.result_tree['columns'][start_col])['text']} ~ "
                    f"{self.result_tree.heading(self.result_tree['columns'][end_col])['text']})"
                )
    
    def get_visible_columns(self):
        """현재 보이는 열의 범위 (인덱스)를 반환"""
        if not self.result_tree:
            return None
            
        # 스크롤바의 현재 위치
        scroll_pos = self.h_scrollbar.get()
        
        # 열 개수
        columns = self.result_tree["columns"]
        num_columns = len(columns)
        
        # 대략적인 보이는 열의 범위 추정
        start_idx = int(scroll_pos[0] * num_columns)
        end_idx = min(int(scroll_pos[1] * num_columns) + 1, num_columns - 1)
        
        # 최소 하나의 열 보장
        if start_idx == end_idx:
            end_idx = min(start_idx + 1, num_columns - 1)
            
        return (start_idx, end_idx)
    
    def on_frame_configure(self, event=None):
        """헤더 프레임 크기가 변경되면 캔버스 스크롤 영역 조정"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event=None):
        """캔버스 크기가 변경되면 내부 프레임 너비 조정"""
        if event:
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def try_open_with_encodings(self, file_path):
        """여러 인코딩을 시도하여 파일 열기"""
        encodings = ['cp949', 'utf-8', 'utf-8-sig', 'euc-kr']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    # 첫 줄을 읽어보아 문제가 없으면 해당 인코딩을 사용
                    f.readline()
                return encoding
            except UnicodeDecodeError:
                continue
        
        # 모든 인코딩이 실패하면 기본값 반환
        return 'cp949'
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="CSV 파일 선택",
            filetypes=[("CSV 파일", "*.csv"), ("모든 파일", "*.*")]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            self.csv_file = file_path
            
            # 인코딩 자동 탐지 시도
            try:
                best_encoding = self.try_open_with_encodings(file_path)
                self.encoding_var.set(best_encoding)
                self.status_var.set(f"파일 로드됨: {Path(file_path).name} (인코딩: {best_encoding})")
                self.load_headers()
            except Exception as e:
                messagebox.showerror("오류", f"파일 로드 중 오류 발생: {str(e)}")
                self.status_var.set("파일 로드 오류")
    
    def reload_headers(self):
        """선택한 인코딩으로 헤더 다시 로드"""
        if not self.csv_file:
            messagebox.showerror("오류", "먼저 CSV 파일을 선택해주세요.")
            return
        
        self.load_headers()
    
    def load_headers(self):
        """CSV 파일의 헤더(1행)를 로드하고 체크박스로 표시"""
        try:
            # 기존 체크박스 제거
            for widget in self.header_frame.winfo_children():
                widget.destroy()
            
            self.headers = []
            self.header_vars = []
            
            # CSV 파일에서 헤더 읽기 - 선택된 인코딩 사용
            encoding = self.encoding_var.get()
            with open(self.csv_file, 'r', encoding=encoding, errors='replace') as f:
                reader = csv.reader(f)
                headers = next(reader, [])  # 첫 번째 행 읽기
                self.headers = headers
            
            # 헤더가 없을 경우
            if not self.headers:
                self.status_var.set("헤더가 없거나 파일이 비어 있습니다.")
                return
            
            # 각 헤더에 대한 체크박스 생성 - 들여쓰기 적용
            for idx, header in enumerate(self.headers):
                # 각 헤더에 대한 프레임 생성 (들여쓰기 용)
                header_item_frame = ttk.Frame(self.header_frame)
                header_item_frame.pack(fill=tk.X, pady=1)
                
                # 들여쓰기를 위한 레이블 (빈 공간)
                ttk.Label(header_item_frame, text="", width=2).pack(side=tk.LEFT)
                
                var = IntVar(value=1)  # 기본적으로 체크된 상태
                cb = Checkbutton(
                    header_item_frame, 
                    text=f"{header}", 
                    variable=var,
                    onvalue=1,
                    offvalue=0
                )
                cb.pack(side=tk.LEFT, anchor=tk.W)
                self.header_vars.append(var)
            
            self.status_var.set(f"헤더 로드됨: {len(self.headers)}개 열")
            self.on_frame_configure()  # 스크롤 영역 업데이트
            
        except Exception as e:
            messagebox.showerror("오류", f"헤더 로드 중 오류가 발생했습니다: {str(e)}")
            self.status_var.set("헤더 로드 오류")
    
    def toggle_all_headers(self):
        """전체 선택/해제 체크박스에 따라 모든 헤더 체크박스 상태 변경"""
        value = self.select_all_var.get()
        for var in self.header_vars:
            var.set(value)
    
    def get_selected_columns(self):
        """선택된 열의 인덱스 목록 반환"""
        selected_columns = []
        for idx, var in enumerate(self.header_vars):
            if var.get() == 1:
                selected_columns.append(idx)
        return selected_columns
    
    def create_result_treeview(self, columns):
        """선택된 열에 맞게 결과 트리뷰 생성"""
        # 기존 트리뷰가 있으면 제거
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # 행 번호 + 선택된 열로 트리뷰 설정
        treeview_columns = ["행"] + [self.headers[idx] for idx in columns]
        
        # 트리뷰 생성
        self.result_tree = ttk.Treeview(self.result_frame, columns=treeview_columns, show="headings")
        
        # 헤딩 설정
        self.result_tree.heading("행", text="행")
        for col_idx in columns:
            header = self.headers[col_idx]
            self.result_tree.heading(header, text=header)
        
        # 열 너비 설정
        self.result_tree.column("행", width=60, minwidth=60)
        for col_idx in columns:
            header = self.headers[col_idx]
            self.result_tree.column(header, width=150, minwidth=100)
        
        # 수직 스크롤바 설정
        scrollbar_y = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar_y.set)
        
        # 수평 스크롤바 설정 (참조 저장)
        self.h_scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.HORIZONTAL, command=self.result_tree.xview)
        self.result_tree.configure(xscrollcommand=self.h_scrollbar.set)
        
        # 배치
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 키보드 바인딩
        self.result_tree.bind("<Left>", lambda event: self.scroll_horizontal(-1))
        self.result_tree.bind("<Right>", lambda event: self.scroll_horizontal(1))
        
        # 결과 트리뷰 컨텍스트 메뉴 (우클릭 메뉴)
        self.context_menu = tk.Menu(self.result_tree, tearoff=0)
        self.context_menu.add_command(label="클립보드에 복사", command=self.copy_to_clipboard)
        
        # 우클릭 메뉴 바인딩
        self.result_tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """트리뷰에서 우클릭 시 컨텍스트 메뉴 표시"""
        self.context_menu.post(event.x_root, event.y_root)
    
    def search(self):
        if not self.csv_file:
            messagebox.showerror("오류", "먼저 CSV 파일을 선택해주세요.")
            return
        
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showerror("오류", "검색어를 입력해주세요.")
            return
        
        # 출력할 열 목록
        self.selected_columns = self.get_selected_columns()
        if not self.selected_columns:
            messagebox.showwarning("경고", "출력할 열을 하나 이상 선택해주세요.")
            return
        
        try:
            self.status_var.set("검색 중...")
            self.root.update_idletasks()
            
            # 선택한 열에 맞게 트리뷰 재생성
            self.create_result_treeview(self.selected_columns)
            
            encoding = self.encoding_var.get()
            # 모든 행과 열에서 검색
            with open(self.csv_file, 'r', encoding=encoding, errors='replace') as f:
                reader = csv.reader(f)
                headers = next(reader)  # 헤더 행
                
                self.found_rows = []  # 찾은 행들 저장
                
                # 모든 데이터에서 검색어 찾기
                for row_idx, row in enumerate(reader, 2):  # 첫 번째 행은 헤더라서 2부터 시작
                    match_found = False
                    
                    # 모든 열에서 검색 (출력할 열 아님)
                    for col_idx, value in enumerate(row):
                        if col_idx < len(row) and search_term.lower() in str(value).lower():
                            match_found = True
                            break
                    
                    # 만약 행에서 검색어가 발견되면, 해당 행의 선택된 열 값을 결과에 추가
                    if match_found:
                        row_values = []
                        row_values.append(row_idx)  # 행 번호
                        
                        # 선택된 열의 값만 가져오기
                        for col_idx in self.selected_columns:
                            if col_idx < len(row):
                                row_values.append(row[col_idx])
                            else:
                                row_values.append("")
                        
                        self.found_rows.append(row_values)
                
                # 결과 표시
                for row_values in self.found_rows:
                    self.result_tree.insert("", tk.END, values=row_values)
            
            if not self.found_rows:
                self.status_var.set(f"검색 결과 없음: '{search_term}'")
            else:
                # 검색 결과가 있으면 자동으로 클립보드에 복사
                self.copy_to_clipboard(silent=True)
                
                # 상태 표시줄 업데이트 - 현재 보이는 열 정보 포함
                visible_columns = self.get_visible_columns()
                if visible_columns:
                    start_col, end_col = visible_columns
                    total_cols = len(self.result_tree["columns"])
                    self.status_var.set(
                        f"열 보기: {start_col+1}-{end_col+1} / {total_cols} "
                        f"({self.result_tree.heading(self.result_tree['columns'][start_col])['text']} ~ "
                        f"{self.result_tree.heading(self.result_tree['columns'][end_col])['text']})"
                    )
        except Exception as e:
            messagebox.showerror("오류", f"검색 중 오류 발생: {str(e)}")
            self.status_var.set("검색 중 오류")
    
    def copy_to_clipboard(self, silent=False):
        if not self.found_rows:
            if not silent:
                messagebox.showinfo("알림", "검색 결과가 없습니다.")
            return
        
        # 검색 결과를 클립보드에 복사
        result_text = "\n".join([",".join(map(str, row)) for row in self.found_rows])
        self.root.clipboard_clear()
        self.root.clipboard_append(result_text)
        self.root.update()
        
        if not silent:
            messagebox.showinfo("알림", "검색 결과가 클립보드에 복사되었습니다.")
