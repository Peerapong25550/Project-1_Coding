import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# คลาสสำหรับสร้าง Entry ที่มีกรอบขอบมน สีขาว โดยไม่มีเส้นสีดำ
class RainbowRoundedEntry(tk.Frame):
    def __init__(self, parent, width=300, height=70, corner_radius=15, **kwargs):
        tk.Frame.__init__(self, parent, bg=parent['bg'])
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        # Canvas ที่มีพื้นหลังสีขาวและไม่มีเส้นขอบ
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white", highlightthickness=0, bd=0)
        self.canvas.pack()
        self.draw_white_border(width, height, corner_radius)
        # สร้าง Entry โดยไม่มี border และ relief="flat"
        self.entry = tk.Entry(self, bd=0, relief="flat", font=("ไทยสารบัญ", 18), bg="white", fg="black", **kwargs)
        self.canvas.create_window(corner_radius, corner_radius, anchor="nw", 
                                  window=self.entry, width=width - 2*corner_radius, height=height - 2*corner_radius)
    
    def draw_white_border(self, width, height, radius):
        # วาดกรอบขอบมนโดยใช้ความหนาของเส้นเป็น 1 px
        self.round_rect(self.canvas, 0, 0, width, height, radius, outline="white", width=1, fill="white")
    
    def round_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

# คลาสสำหรับสร้าง Combobox ที่มีกรอบขอบมน สีขาว โดยไม่มีเส้นสีดำ
class RainbowRoundedCombobox(tk.Frame):
    def __init__(self, parent, values, width=100, height=70, corner_radius=15, **kwargs):
        tk.Frame.__init__(self, parent, bg=parent['bg'])
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        # Canvas ที่มีพื้นหลังสีขาวและไม่มีเส้นขอบ
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white", highlightthickness=0, bd=0)
        self.canvas.pack()
        self.draw_white_border(width, height, corner_radius)
        self.combobox = ttk.Combobox(self, values=values, font=("ไทยสารบัญ", 18), state="readonly", **kwargs)
        self.canvas.create_window(corner_radius, corner_radius, anchor="nw", 
                                  window=self.combobox, width=width - 2*corner_radius, height=height - 2*corner_radius)
    
    def draw_white_border(self, width, height, radius):
        self.round_rect(self.canvas, 0, 0, width, height, radius, outline="white", width=1, fill="white")
    
    def round_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def update_day_options(day_widget, month_widget, year_widget):
    try:
        month = int(month_widget.combobox.get())
        year = int(year_widget.combobox.get())
    except ValueError:
        return
    if month in [1, 3, 5, 7, 8, 10, 12]:
        days = 31
    elif month in [4, 6, 9, 11]:
        days = 30
    elif month == 2:
        days = 29 if is_leap(year) else 28
    else:
        days = 31
    day_values = [str(i) for i in range(1, days + 1)]
    day_widget.combobox['values'] = day_values
    try:
        current_day = int(day_widget.combobox.get())
    except ValueError:
        current_day = 1
    if current_day > days:
        day_widget.combobox.set(str(days))

def update_day_in(event=None):
    update_day_options(day_in_widget, month_in_widget, year_in_widget)

def update_day_out(event=None):
    update_day_options(day_out_widget, month_out_widget, year_out_widget)

def calculate_interest():
    try:
        capital = float(rainbow_entry_capital.entry.get())
    except ValueError:
        messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกจำนวนเงินเป็นตัวเลข")
        return

    try:
        d_in = int(day_in_widget.combobox.get())
        m_in = int(month_in_widget.combobox.get())
        y_in = int(year_in_widget.combobox.get())
        date_in = datetime(y_in, m_in, d_in)
    except ValueError:
        messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกวันที่นำเงินเข้าให้ถูกต้อง")
        return

    try:
        d_out = int(day_out_widget.combobox.get())
        m_out = int(month_out_widget.combobox.get())
        y_out = int(year_out_widget.combobox.get())
        date_out = datetime(y_out, m_out, d_out)
    except ValueError:
        messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกวันที่นำเงินออกให้ถูกต้อง")
        return

    if date_out <= date_in:
        messagebox.showerror("ข้อผิดพลาด", "วันที่นำออกต้องมากกว่าวันที่นำเข้า")
        return

    day_diff = (date_out - date_in).days

    if capital <= 10000:
        interest = 0.03
    elif capital <= 1000000:
        interest = 0.015
    else:
        interest = 0.0005

    final_amount = capital + (capital * interest * (day_diff / 365))
    result_label.config(text=f"คุณจะมีเงินรวมทั้งสิ้น {final_amount:.2f} บาท")

# ซ่อนหน้าต่างหลักก่อนสร้าง UI
root = tk.Tk()
root.withdraw()

root.title("คำนวณดอกเบี้ยเงินฝาก")
root.geometry("650x500")
root.configure(bg="black")

main_frame = tk.Frame(root, bg="black")
main_frame.pack(padx=40, pady=40, expand=True)

# ช่องกรอกจำนวนเงินต้น (ใช้ RainbowRoundedEntry)
label_capital = tk.Label(main_frame, text="จำนวนเงินต้น (บาท):", bg="black", fg="white", font=("ไทยสารบัญ", 18))
label_capital.grid(row=0, column=0, pady=10, sticky="w")
rainbow_entry_capital = RainbowRoundedEntry(main_frame, width=250, height=50, corner_radius=15)
rainbow_entry_capital.grid(row=0, column=1, pady=10, sticky="w", padx=10)

# ช่องเลือกวันที่นำเงินเข้า (ใช้ RainbowRoundedCombobox สำหรับวัน, เดือน, ปี)
label_date_in = tk.Label(main_frame, text="วันที่นำเงินเข้า:", bg="black", fg="white", font=("ไทยสารบัญ", 18))
label_date_in.grid(row=1, column=0, pady=10, sticky="w")
frame_date_in = tk.Frame(main_frame, bg="black")
frame_date_in.grid(row=1, column=1, pady=10, sticky="w", padx=10)

day_in_widget = RainbowRoundedCombobox(frame_date_in, values=[str(i) for i in range(1, 32)], width=80, height=60, corner_radius=15)
day_in_widget.grid(row=0, column=0, padx=5)
month_in_widget = RainbowRoundedCombobox(frame_date_in, values=[str(i) for i in range(1, 13)], width=80, height=60, corner_radius=15)
month_in_widget.grid(row=0, column=1, padx=5)
year_in_widget = RainbowRoundedCombobox(frame_date_in, values=[str(i) for i in range(1900, 2101)], width=130, height=60, corner_radius=15)
year_in_widget.grid(row=0, column=2, padx=5)

# ช่องเลือกวันที่นำเงินออก (ใช้ RainbowRoundedCombobox สำหรับวัน, เดือน, ปี)
label_date_out = tk.Label(main_frame, text="วันที่นำเงินออก:", bg="black", fg="white", font=("ไทยสารบัญ", 18))
label_date_out.grid(row=2, column=0, pady=10, sticky="w")
frame_date_out = tk.Frame(main_frame, bg="black")
frame_date_out.grid(row=2, column=1, pady=10, sticky="w", padx=10)

day_out_widget = RainbowRoundedCombobox(frame_date_out, values=[str(i) for i in range(1, 32)], width=80, height=60, corner_radius=15)
day_out_widget.grid(row=0, column=0, padx=5)
month_out_widget = RainbowRoundedCombobox(frame_date_out, values=[str(i) for i in range(1, 13)], width=80, height=60, corner_radius=15)
month_out_widget.grid(row=0, column=1, padx=5)
year_out_widget = RainbowRoundedCombobox(frame_date_out, values=[str(i) for i in range(1900, 2101)], width=130, height=60, corner_radius=15)
year_out_widget.grid(row=0, column=2, padx=5)

# กำหนดค่าเริ่มต้นเป็นวันที่ปัจจุบัน
now = datetime.now()
day_in_widget.combobox.set(str(now.day))
month_in_widget.combobox.set(str(now.month))
year_in_widget.combobox.set(str(now.year))
day_out_widget.combobox.set(str(now.day))
month_out_widget.combobox.set(str(now.month))
year_out_widget.combobox.set(str(now.year))

update_day_options(day_in_widget, month_in_widget, year_in_widget)
update_day_options(day_out_widget, month_out_widget, year_out_widget)

# Bind event เมื่อมีการเลือกเดือนหรือปี
month_in_widget.combobox.bind("<<ComboboxSelected>>", update_day_in)
year_in_widget.combobox.bind("<<ComboboxSelected>>", update_day_in)
month_out_widget.combobox.bind("<<ComboboxSelected>>", update_day_out)
year_out_widget.combobox.bind("<<ComboboxSelected>>", update_day_out)

# ปุ่มคำนวณ (ใช้ frame ที่มีความกว้างคงที่ 400px)
calc_frame = tk.Frame(main_frame, width=400, bg="black")
calc_frame.grid(row=3, column=0, columnspan=2, pady=20)
calc_frame.grid_propagate(False)
calc_button = tk.Button(calc_frame, text="คำนวณ", command=calculate_interest,
                        bg="#4CAF50", fg="white", font=("ไทยสารบัญ", 18), relief="raised")
calc_button.pack(expand=True, fill="both")

# แสดงผลลัพธ์
result_label = tk.Label(main_frame, text="", bg="black", fg="white", font=("ไทยสารบัญ", 18))
result_label.grid(row=4, column=0, columnspan=2, pady=20)

# แสดงหน้าต่างหลักหลังจากสร้าง UI เสร็จ
root.deiconify()
root.mainloop()
