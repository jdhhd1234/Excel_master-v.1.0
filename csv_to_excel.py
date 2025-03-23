from pathlib import Path

# 재생성 (세션 초기화됨)
project_dir = Path("/mnt/data/Excel_master-v1.0")
project_dir.mkdir(parents=True, exist_ok=True)

csv2excel_code = """\
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def convert_csv_to_excel():
    path = filedialog.askopenfilename(filetypes=[("CSV 파일", "*.csv")])
    if not path:
        return

    try:
        df = pd.read_csv(path, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(path, encoding='cp949')
        except Exception as e:
            messagebox.showerror("오류", f"CSV 파일을 읽는 중 오류 발생: {e}")
            return

    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel 파일", "*.xlsx")],
                                             initialfile=os.path.splitext(os.path.basename(path))[0] + ".xlsx",
                                             title="엑셀 파일로 저장")
    if not save_path:
        return

    try:
        df.to_excel(save_path, index=False)
        messagebox.showinfo("성공", f"엑셀 파일로 저장 완료:\n{save_path}")
    except Exception as e:
        messagebox.showerror("오류", f"엑셀 파일 저장 중 오류 발생: {e}")

# GUI 실행
root = tk.Tk()
root.withdraw()  # 메인 창 숨기기
convert_csv_to_excel()
"""

# 파일 저장
csv2excel_path = project_dir / "csv_to_excel.py"
with open(csv2excel_path, "w", encoding="utf-8") as f:
    f.write(csv2excel_code)

csv2excel_path
