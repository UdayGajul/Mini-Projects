from tkinter import *
import math
from tkinter import messagebox

# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
reps = 0
timer = None
pending_break = None
pending_work = None
first_work_done = False

# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
    
    global timer, pending_break, pending_work, reps, first_work_done
    
    if timer:
        root.after_cancel(timer)
        timer= None
    # Reset timer to 00:00
    canvas.itemconfig(timer_text, text='00:00')
    # Reset title_label to Timer
    title_label.config(text='Timer')
    # Reset the check mark
    check_label.config(text='')
    # Reset the reps to 0
    reps = 0
    pending_break = None
    pending_work = None
    first_work_done = False

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps, pending_break, pending_work, first_work_done
    
    reps += 1
    
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    
    if reps % 8 == 0:
        pending_break = ('Long break', RED, long_break_sec)
        ask_before_break()
    elif reps % 2 == 0:
        pending_break = ('Short break', PINK, short_break_sec)
        ask_before_break()
    else:
        if reps == 1:
            title_label.config(text='Work')
            count_down(work_sec)
        else:
            pending_work = work_sec
            ask_before_work()

# ---------------------------- ASK BEFORE BREAK ------------------------------- # 

def ask_before_break():
    """Shows a Yes/No dialog. If user clicks Yes → start the break."""
    name, color, seconds = pending_break
    
    # make the dialog box top most
    popup = Toplevel(root)
    popup.withdraw()
    popup.attributes('-topmost', True)
    
    answer = messagebox.askyesno(
        "Break time?", 
        f"Work finished!\nDo you want to start {name}?", 
        parent=popup
    )
    
    popup.destroy()
    
    if answer:
        title_label.config(text=name, fg=color)
        count_down(seconds)
    else:
        reset_timer()

# ---------------------------- ASK BEFORE WORK ------------------------------- # 

def ask_before_work():
    """Ask user if the user want to start the next work session."""
    popup = Toplevel(root)
    popup.withdraw()
    popup.attributes('-topmost', True)
    
    answer = messagebox.askyesno(
        "Work time?",
        "Break finished!\nDo you want to start the Work?",
        parent=popup
    )
    popup.destroy()
    
    if answer:
        global first_work_done
        first_work_done = True
        title_label.config(text='Work')
        count_down(pending_work)
    else:
        reset_timer()

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def count_down(count):
    global timer
    
    count_min = math.floor(count / 60)
    count_sec = count % 60
    
    # Dynamic typing
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    
    if count_min < 10:
        count_min = f"0{count_min}"
    
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0 :
        timer = root.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ''
        work_session = math.floor(reps/2)
        for _ in range(work_session):
            marks += '✅'
        
        check_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #

root = Tk()

root.title("Pomodoro App")
root.config(padx=100, pady=50, bg=YELLOW)
root.iconbitmap('tomato_icon.ico')

# Creating a canvas
canvas = Canvas(width=201, height=224)

# Title Lable
title_label = Label(text='Timer', fg=GREEN, font=(FONT_NAME, 40, 'bold'), bg=YELLOW)
title_label .grid(row=0, column=1)

# Tomato image
tomato_img = PhotoImage(file='tomato.png')
canvas.config(bg=YELLOW)
canvas.create_image(103, 112, image=tomato_img)
timer_text = canvas.create_text(103, 130, text=f"00:00", fill='white', font=(FONT_NAME, 25, 'bold'))
canvas.grid(row=1, column=1)

# Buttons start and restart
start_button = Button(text='Start', bg=YELLOW, font=(FONT_NAME, 15), fg=RED, command=start_timer)
start_button.grid(row=2, column=0)
reset_button = Button(text='Reset', bg=YELLOW, font=(FONT_NAME, 15), fg=RED, command=reset_timer)
reset_button.grid(row=2, column=2)

# Checkbox on the screen 
check_label = Label(fg=GREEN, font=(FONT_NAME, 25, 'bold'), bg=YELLOW)
check_label.grid(row=3, column=1)

root.mainloop()

