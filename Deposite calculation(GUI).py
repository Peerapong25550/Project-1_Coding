import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Function to check if the date is valid and ensure the correct format
def check_date_format(time_in, time_out):
    date_in = list(map(int, time_in.split("/")))
    date_out = list(map(int, time_out.split("/")))

    for i in range(2, 0, -1):
        if date_in[i] < date_out[i]:
            return True
        elif date_in[i] == date_out[i]:
            continue
        else:
            return False

# Function to check if a year is a leap year
def check_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

# Function to calculate the number of days between two dates
def calculate_days(date_in, date_out):
    month_day = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    day_count = 0

    # Check if the dates are within the same year
    if date_in[2] == date_out[2]:
        for i in range(date_in[1], date_out[1]):
            if check_leap_year(date_in[2]) and i == 2:
                day_count += 1
            day_count += month_day[i]
        day_count -= date_in[0]
        day_count += date_out[0]
    
    else:
        # Calculate days left in the start year
        for i in range(date_in[1], 13):
            day_count += month_day[i]
            if check_leap_year(date_in[2]) and i == 2:
                day_count += 1
        day_count -= date_in[0] - 1

        # Calculate days in the years between the start and end year
        for i in range(date_in[2] + 1, date_out[2]):
            for j in range(1, 13):
                if j == 2 and check_leap_year(i):
                    day_count += 1
                day_count += month_day[j]

        # Calculate days in the end year
        for i in range(1, date_out[1]):
            day_count += month_day[i]
            if check_leap_year(date_out[2]) and i == 2:
                day_count += 1
        day_count += date_out[0]

    return day_count

# Function to calculate the interest based on the capital and time period
def calculate_interest(capital, days):
    if capital <= 10000:
        interest_rate = 0.03
    elif capital <= 1000000:
        interest_rate = 0.015
    else:
        interest_rate = 0.0005
    
    return capital * interest_rate * (days / 365)

# Function to handle the calculation when the user presses the button
def calculate():
    try:
        capital = float(entry_capital.get().replace(",", ""))  # Remove commas before converting to float
        time_in = entry_time_in.get()
        time_out = entry_time_out.get()

        # Validate the date format and input
        if not check_date_format(time_in, time_out):
            messagebox.showerror("Invalid Input", "กรุณาเช็ควันเดือนปีให้ถูกต้อง และกรอกข้อมูลใหม่ ตามรูปแบบ วว/ดด/ปปปป")
            return

        # Convert the date string to lists of integers
        date_in = [int(time_in[0:2]), int(time_in[3:5]), int(time_in[6:10])]
        date_out = [int(time_out[0:2]), int(time_out[3:5]), int(time_out[6:10])]

        # Calculate the number of days between the dates
        days = calculate_days(date_in, date_out)

        # Calculate the interest earned
        total_amount = capital + calculate_interest(capital, days)

        # Format capital and result to include commas
        formatted_capital = "{:,.2f}".format(capital)
        formatted_result = "{:,.2f}".format(total_amount)

        # Show the result
        result_label.config(text=f"ยอดเงินทั้งหมด: {formatted_result} บาท")
        entry_capital.delete(0, tk.END)  # Clear the entry field after calculation
        entry_capital.insert(0, formatted_capital)  # Reinsert the formatted capital with commas

    except ValueError:
        messagebox.showerror("Invalid Input", "กรุณากรอกข้อมูลให้ถูกต้อง (เช่น จำนวนเงินต้องเป็นตัวเลข)")

# Create the main window
root = tk.Tk()
root.title("Deposite Calculation")
root.geometry("400x450")  # Set a fixed window size

# Styling with ttk
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
style.configure("TEntry", font=("Arial", 12), padding=5)

# Add a label for the program title at the top (centered)
title_label = ttk.Label(root, text="Deposite Calculation", style="TLabel")
title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=10)

# Add a label and entry for the capital amount
label_capital = ttk.Label(root, text="กรอกจำนวนเงิน (บาท):")
label_capital.grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_capital = ttk.Entry(root, style="TEntry")
entry_capital.grid(row=1, column=1, padx=10, pady=10)

# Add a label and entry for the 'time_in' date
label_time_in = ttk.Label(root, text="เวลาที่นำเงินเข้า (วว/ดด/ปปปป):")
label_time_in.grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_time_in = ttk.Entry(root, style="TEntry")
entry_time_in.grid(row=2, column=1, padx=10, pady=10)

# Add a label and entry for the 'time_out' date
label_time_out = ttk.Label(root, text="เวลาที่นำเงินออก (วว/ดด/ปปปป):")
label_time_out.grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_time_out = ttk.Entry(root, style="TEntry")
entry_time_out.grid(row=3, column=1, padx=10, pady=10)

# Add a button to trigger the calculation
calculate_button = ttk.Button(root, text="คำนวณ", command=calculate)
calculate_button.grid(row=4, column=0, columnspan=2, pady=20)

# Add a label to show the result
result_label = ttk.Label(root, text="ยอดเงินทั้งหมด: - บาท", style="TLabel")
result_label.grid(row=5, column=0, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()
