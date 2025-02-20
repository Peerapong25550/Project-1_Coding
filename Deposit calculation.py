def check_date(time_in, time_out):
    date_in = list(map(int, time_in.split("/")))
    date_out = list(map(int, time_out.split("/")))

    for i in range(2, 0, -1):
        if date_in[i] < date_out[i]:
            return True
        elif date_in[i] == date_out[i]:
            continue
        else:
            return False

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

while(1):
    capital = int(input("กรอกจำนวนเงิน : "))
    time_in = input("เวลาที่นำเงินเข้า(วว/ดด/ปปปป(ค.ศ.)) : ")
    time_out = input("เวลาที่นำเงินออก(วว/ดด/ปปปป(ค.ศ.)) : ")
    if check_date(time_in, time_out):
        break
    else :
        print("กรุณาเช็ควันเดือนปีให้ถูกต้อง และกรอกข้อมูลใหม่ ตามรูปแบบ วว/ดด/ปปปป\nเช่น 01/02/2020")

date_in = list(map(int, time_in.split("/")))
date_out = list(map(int, time_out.split("/")))

month_day = {
    1 : 31,
    2 : 28,
    3 : 31,
    4 : 30,
    5 : 31,
    6 : 30,
    7 : 31,
    8 : 31,
    9 : 30,
    10 : 31,
    11 : 30,
    12 : 31,
}

day = 0
if date_in[2] == date_out[2]:
    for i in range(date_in[1], date_out[1]):
        if check_leap_year(date_in[2]) and i == 2:
            day += 1
        day += month_day[i]
    day -= date_in[0]
    day += date_out[0]

else:
    for i in range(date_in[1], 13):
        day += month_day[i]
        if check_leap_year(date_in[2]) and i == 2:
            day += 1
    day -= date_in[0] - 1

    for i in range(date_in[2] + 1, date_out[2]):
        for j in range(1, 13):
            if j == 2 and check_leap_year(i):
                day += 1
            day += month_day[j]
    
    for i in range(1, date_out[1]):
        day += month_day[i]
        if check_leap_year(date_in[2]) and i == 2:
            day += 1
    day += date_out[0]

if capital <= 10000:
    interest = 0.03
elif capital <= 1000000:
    interest = 0.015
else:
    interest = 0.0005

capital += capital * interest * (day / 365)
print(f"หากคุณนำเงินเข้ามาในวันที่ {time_in} และนำออกในวันที่ {time_out} คุณจะมีเงินรวมทั้งสิ้น {capital:.2f} บาท")