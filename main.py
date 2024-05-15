from tkinter import *
from datetime import datetime, timedelta

root = Tk()
root.title("Digital Clock")
root.configure(bg='white')

tz_offsets = {
    "Asia/Tokyo": timedelta(hours=9),
    "America/New_York": timedelta(hours=-5)  # 標準時間はUTC-5
}

# 初期タイムゾーン
current_tz = "Asia/Tokyo"

def is_dst(dt, tz):
    if tz == "America/New_York":
        # アメリカのDSTは3月第2日曜日から11月第1日曜日まで
        dst_start = datetime(dt.year, 3, (14 - (datetime(dt.year, 3, 1).weekday() + 1) % 7)).replace(hour=2)
        dst_end = datetime(dt.year, 11, (7 - (datetime(dt.year, 11, 1).weekday() + 1) % 7)).replace(hour=2)
        return dst_start <= dt < dst_end
    return False

def update_time():
    now = datetime.utcnow()
    timezone_offset = tz_offsets[current_tz]
    local_time = now + timezone_offset

    if is_dst(local_time, current_tz):
        local_time += timedelta(hours=1)

    current_year = local_time.year
    is_leap = isleap(current_year)
    date_string = format_time("%y%b%d%a", local_time) + ("  うるう年" if is_leap else "")
    time_string = format_time("%H:%M:%S %p", local_time)

    date_label.config(text=date_string)
    time_label.config(text=time_string)
    time_label.after(1000, update_time)

def change_background():
    global button_frame
    current_bg = root.cget('bg')
    if current_bg == 'white':
        root.configure(bg='black')
        date_label.configure(bg='black', fg='white')
        time_label.configure(bg='black', fg='white')
        button_frame.configure(bg='black')
    else:
        root.configure(bg='white')
        date_label.configure(bg='white', fg='black')
        time_label.configure(bg='white', fg='black')
        button_frame.configure(bg='white')


def isleap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def format_time(fmt, current_time):
    year, month, day = current_time.year, current_time.month, current_time.day
    hour, minute, second = current_time.hour, current_time.minute, current_time.second
    weekday = current_time.weekday()

    weekday_names = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
    year_names = [f'{i}年' for i in range(1, 3001)]
    month_names = [f'{i}月' for i in range(1, 13)]
    day_names = [f'{i}日' for i in range(1, 32)]
    hour_names = [f'{i}時' for i in range(0, 24)]
    minute_names = [f'{i}分' for i in range(0, 60)]
    second_names = [f'{i}秒' for i in range(0, 60)]

    replacements = {
        '%Y': str(year),
        '%B': zfill(str(month), 2),
        '%D': zfill(str(day), 2),
        '%H': zfill(str(hour), 2),
        '%M': zfill(str(minute), 2),
        '%S': zfill(str(second), 2),
        '%d': day_names[day - 1],
        '%a': weekday_names[weekday],
        '%y': year_names[year - 1],
        '%b': month_names[month - 1],
        '%h': hour_names[hour],
        '%m': minute_names[minute],
        '%s': second_names[second],
        '%p': 'AM' if hour < 12 else 'PM',
    }

    result_format = fmt
    for key, value in replacements.items():
        result_format = result_format.replace(key, value)

    return result_format

def zfill(s, width):
    is_negative = s.startswith('-')
    num_str = s[1:] if is_negative else s

    filled_str = num_str.rjust(width, '0')

    if is_negative:
        filled_str = '-' + filled_str

    return filled_str

def change_time_zone(new_tz_name):
    global current_tz
    if new_tz_name in tz_offsets:
        current_tz = new_tz_name
        update_time()
    else:
        print("Invalid time zone")

if __name__ == "__main__":

    date_label = Label(root, font=("Helvetica", 20, "normal"), bg="white", fg="black")
    date_label.grid(row=0, column=0, sticky="W")

    button = Button(root, text="Change Color", command=change_background, bg='green', fg='white')
    button.grid(row=0, column=1)

    time_label = Label(root, font=("Impact", 80, "bold"), bg="white", fg="black")
    time_label.grid(row=1, column=0, columnspan=3)

    button_frame = Frame(root, bg="white")
    button_frame.grid(row=2, column=0, columnspan=2, pady=5)

    tokyo_button = Button(button_frame, text="Tokyo Time", command=lambda: change_time_zone("Asia/Tokyo"), bg='green', fg='white')
    tokyo_button.pack(side=LEFT, padx=5)

    ny_button = Button(button_frame, text="New York Time", command=lambda: change_time_zone("America/New_York"), bg='green', fg='white')
    ny_button.pack(side=LEFT, padx=5)

    update_time()
    root.mainloop()

