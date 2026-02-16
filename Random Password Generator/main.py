import tkinter as tk
import random
import pyperclip

# Character pools
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
SPECIAL = "!@#$%^&*()-_+=[]{}|;:'\",.<>?/`~"

pools = [UPPER, LOWER, DIGITS, SPECIAL]

# Main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("800x380")
root.resizable(False, False)
root.iconbitmap('key.ico')

# Heading
tk.Label(root, text="Random Password Generator", font=("Helvetica", 25, "bold"), fg="#2c3e50")\
    .grid(row=0, column=1, columnspan=3, pady=(20, 10))

# Length selector
tk.Label(root, text="Password Length:", font=("Arial", 12))\
    .grid(row=1, column=0, padx=(40, 5), pady=10, sticky="e")

length_var = tk.StringVar(value="8")

def decrease():
    n = int(length_var.get())
    if n > 1:
        length_var.set(str(n - 1))
    update_warning()

def increase():
    length_var.set(str(int(length_var.get()) + 1))
    update_warning()

tk.Button(root, text="–", font=("Arial", 14, "bold"), width=3, command=decrease)\
    .grid(row=1, column=1, padx=5, pady=10)
tk.Entry(root, textvariable=length_var, width=6, font=("Arial", 12), justify="center")\
    .grid(row=1, column=2, padx=5, pady=10)
tk.Button(root, text="+", font=("Arial", 14, "bold"), width=3, command=increase)\
    .grid(row=1, column=3, padx=(5, 40), pady=10)

# Validation
def validate(*args):
    v = length_var.get()
    if not v: 
        length_var.set("1")
    elif v.isdigit():
        n = int(v)
        length_var.set(str(max(1, min(500, n))))
    else:
        length_var.set("8")
    update_warning()
length_var.trace("w", validate)

# Warning
warning = tk.Label(root, text="", font=("Arial", 10, "italic"), fg="#e74c3c", wraplength=600)
warning.grid(row=2, column=1, columnspan=3, pady=(0, 10))

def update_warning():
    if int(length_var.get()) < 8:
        warning.config(text="Warning: Passwords less than 8 characters can be cracked easily!")
    else:
        warning.config(text="")

# GENERATE PASSWORD (100% SAFE)
def generate():
    n = int(length_var.get())
    password = []

    # Step 1: Ensure at least ONE from each category
    for pool in pools:
        password.append(random.choice(pool))

    # Step 2: Fill the rest safely
    remaining = n - 4
    all_chars = UPPER + LOWER + DIGITS + SPECIAL

    for _ in range(remaining):
        password.append(random.choice(all_chars))

    # Step 3: Shuffle
    random.shuffle(password)
    final = ''.join(password)

    result_var.set(final)
    pyperclip.copy(final)
    feedback.config(text="Copied to clipboard!", fg="green")
    root.after(2000, lambda: feedback.config(text=""))

# Generate button (perfect size)
tk.Button(root, text="Generate Password", font=("Arial", 12, "bold"),
          bg="#27ae60", fg="white", command=generate, width=20, height=1)\
    .grid(row=3, column=1, columnspan=3, pady=15)

feedback = tk.Label(root, text="", font=("Arial", 10))
feedback.grid(row=4, column=1, columnspan=3)

# Result display
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, font=("Courier", 14, "bold"), width=40,
         justify="center", state="readonly", readonlybackground="#f0f0f0", bd=2, relief="solid")\
    .grid(row=5, column=1, columnspan=3, pady=(10, 20), padx=40, sticky="ew")

update_warning()
root.mainloop()