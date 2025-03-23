import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from openpyxl import load_workbook
import pandas as pd
import os
from tkinter import filedialog

# 전역 변수
excel_path = None
checkbox_vars = {}

def select_excel_file():
    global excel_path, df, checkbox_vars

    path = filedialog.askopenfilename(filetypes=[("Excel 파일", "*.xlsx")])
    if not path:
        return

    excel_path = path
    entry_path.delete(0, tk.END)
    entry_path.insert(0, path)

    try:
        # pandas로 A열 로드
        df = pd.read_excel(path)
        if df.empty or df.columns[0] is None:
            messagebox.showerror("오류", "엑셀의 첫 번째 열을 인식할 수 없습니다.")
            return

        values = df.iloc[:, 0].dropna().unique().tolist()
        values.sort()
        checkbox_vars.clear()

        for widget in value_frame.winfo_children():
            widget.destroy()

        for val in values:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(value_frame, text=str(val), variable=var, anchor="w")
            cb.pack(fill="x", anchor="w")
            checkbox_vars[val] = var

    except Exception as e:
        messagebox.showerror("오류", f"엑셀 불러오기 실패: {e}")

def extract_selected_rows():
    if not excel_path:
        messagebox.showwarning("파일 없음", "엑셀 파일을 먼저 선택하세요.")
        return

    selected_values = [val for val, var in checkbox_vars.items() if var.get()]
    if not selected_values:
        messagebox.showwarning("선택 없음", "A열 값 중 하나 이상을 선택해주세요.")
        return

    try:
        filtered_df = df[df.iloc[:, 0].isin(selected_values)]
        if filtered_df.empty:
            messagebox.showinfo("결과 없음", "조건에 맞는 데이터가 없습니다.")
            return

        # ✅ 사용자에게 저장 경로를 직접 선택받기
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="A열_필터결과.xlsx",
            title="저장할 파일 경로와 이름을 선택하세요"
        )
        if not save_path:
            return  # 저장 취소 시 중단

        filtered_df.to_excel(save_path, index=False)
        messagebox.showinfo("저장 완료", f"{len(filtered_df)}개의 행이 저장되었습니다:\n{save_path}")

    except Exception as e:
        messagebox.showerror("오류", str(e))


# GUI 시작
root = tk.Tk()
root.title("Excel Master v1.0")
root.geometry("600x700")

# 파일 선택
frame_file = tk.Frame(root)
frame_file.pack(pady=10)
entry_path = tk.Entry(frame_file, width=55)
entry_path.pack(side="left", padx=5)
tk.Button(frame_file, text="엑셀 파일 열기", command=select_excel_file).pack(side="left")

# 안내 문구
tk.Label(root, text="A열에 포함된 값들 중 필터링할 항목을 선택하세요").pack()

# 스크롤 가능한 프레임
canvas = tk.Canvas(root, height=450)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
value_frame = tk.Frame(canvas)

value_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=value_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 실행 버튼
tk.Button(root, text="선택 항목만 추출 및 저장", command=extract_selected_rows,
          bg="#4CAF50", fg="white", height=2).pack(pady=20)

root.mainloop()
