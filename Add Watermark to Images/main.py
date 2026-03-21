from tkinter import ttk, filedialog
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os


fonts_dict = {
    "Allura": "./custom_fonts/Allura-Regular.ttf",
    "Bellefair": "./custom_fonts/Bellefair-Regular.ttf",
    "Bitcount Grid Double Ink": "./custom_fonts/BitcountGridDoubleInk-VariableFont_CRSV,ELSH,ELXP,SZP1,SZP2,XPN1,XPN2,YPN1,YPN2,slnt,wght.ttf",
    "Cherry Cream Soda": "./custom_fonts/CherryCreamSoda-Regular.ttf",
    "Courier Prime": "./custom_fonts/CourierPrime-Regular.ttf",
    "EB Garamond": "./custom_fonts/EBGaramond-VariableFont_wght.ttf",
    "Inter": "./custom_fonts/Inter-VariableFont_opsz,wght.ttf",
    "Mentor 51": "./custom_fonts/Mentor51-Bold.ttf",
    "Montserrat": "./custom_fonts/Montserrat-VariableFont_wght.ttf",
    "Pinyon Script": "./custom_fonts/PinyonScript-Regular.ttf",
    "Roboto": "./custom_fonts/Roboto-VariableFont_wdth,wght.ttf",
}

position_code_dict = {
    "Top right": "TR",
    "Top left": "TL",
    "Bottom right": "BR",
    "Bottom left": "BL",
}

# Global variable to store original image dimensions
original_image = None
display_image_resized = None
original_width = 0
original_height = 0


def get_position(
    pos_code: str,
    img_width: int,
    img_height: int,
    text_width: int,
    text_height: int,
    font_size: int,
    margin=10,
):
    pos_code_1 = pos_code.upper()
    # Extra bottom padding based on font size
    extra_v_pad = int(font_size * 0.30)  # 30% of font size

    if pos_code_1 == "TL":  # Top Left
        return (margin, margin)
    elif pos_code_1 == "TR":
        return (img_width - text_width - margin, margin)
    elif pos_code_1 == "BL":
        return (margin, img_height - text_height - margin - extra_v_pad)
    elif pos_code_1 == "BR":
        return (
            img_width - text_width - margin,
            img_height - text_height - margin - extra_v_pad,
        )
    else:
        # Invalid position code set to default bottom-right
        return (
            img_width - text_width - margin,
            img_height - text_height - margin - extra_v_pad,
        )


def fit_image_to_area(pil_img, max_w, max_h):
    w, h = pil_img.size
    if w <= max_w and h <= max_h:
        return pil_img.copy()

    ratio = min(max_w / w, max_h / h)
    new_w = int(w * ratio)
    new_h = int(h * ratio)
    return pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)


def display_image(file_path):
    global original_image, display_image_resized
    global original_width, original_height

    # load the image
    try:
        original_image = Image.open(file_path)
        # original width, height
        original_width, original_height = original_image.size

        # resize image to fit in the window
        display_image_resized = fit_image_to_area(original_image, 800, 600)

        # convert the PIL img to tkinter photoimage
        photo = ImageTk.PhotoImage(display_image_resized)

        # update img_label
        img_label.config(image=photo)
        img_label.image = photo

        status_label.config(
            text=f"Loaded: {os.path.basename(file_path)} {original_width}x{original_height}"
        )
    except (FileNotFoundError, IOError, Exception) as e:
        print("Error in locating the image", e)


def preview():
    global original_image, original_width, original_height

    if original_image is None:
        status_label.config(text="No image is loaded.")
        return

    if original_image.size != (original_width, original_height):
        original_image = original_image.resize(
            (original_width, original_height), Image.Resampling.LANCZOS
        )

    working = original_image.copy()

    if working.mode != "RGB":
        working = working.convert("RGB")

    # define the text, position, and font
    text_to_add = txt_entry.get().strip() or "Watermark example"

    try:
        pos_code = position_code_dict[str(txt_position.get().strip())]
    except:
        pos_code = ""

    try:
        f_size = int(font_size_combo.get().strip())
    except (ValueError, Exception) as e:
        print("User didn't enter a valid number so set to default 50", e)
        f_size = 50

    try:
        font_path = fonts_dict[str(select_font_combo.get())]
        font = ImageFont.truetype(font_path, f_size)
    except (IOError, Exception):
        print("Font not found, using default font.")
        font = ImageFont.load_default()

    # white color (R, G, B) - (255, 255, 255)
    try:
        color = (int(r_value.get()), int(g_value.get()), int(b_value.get()))
    except Exception:
        color = (255, 255, 255)

    # create a drawing content
    draw = ImageDraw.Draw(working)

    # caluclate the text size
    bbox = draw.textbbox((0, 0), text_to_add, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = get_position(
        pos_code, original_width, original_height, text_width, text_height, f_size
    )

    # draw text
    draw.text(position, text_to_add, font=font, fill=color)
    working.show()
    original_image = working.copy()


def save_image():
    global original_image

    if original_image is None:
        status_label.config(text="No image loaded")
        return

    if original_image.size != (original_width, original_height):
        original_image = original_image.resize(
            (original_width, original_height), Image.Resampling.LANCZOS
        )

    working = original_image.copy()
    if working:
        file_path = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save Wartermarked Image",
            defaultextension=".jpg",
            filetypes=(
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*"),
            ),
        )

        if file_path:
            try:
                working.save(
                    file_path,
                    quality=92 if file_path.lower().endswith(".jpg") else None,
                )
                status_label.config(text=f"Saved: {os.path.basename(file_path)}")
                print(f"Successfully saved to {file_path}")
            except Exception as e:
                status_label.config(text=f"Save failed: {e}")
                print("Error saving image", e)
        else:
            status_label.config(text="No image to save.")


def open_image():
    # use filedialogue to prompt the user to select an image file
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select Image File",
        filetypes=(
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("All files", "*.*"),
        ),
    )
    if file_path:
        display_image(file_path)


root = tk.Tk()

# Enable true full screen
root.state("zoomed")
# app icon
root.iconbitmap("favicon.ico")
# title
root.title("Watermark App")

# title inside the window
title_label = tk.Label(
    root,
    text="Add Watermark to Images",
    font=("Garamond", 24, "bold"),
    justify="center",
)
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# btn for choose img
select_img_btn = tk.Button(root, text="Open image", command=open_image)
select_img_btn.grid(row=1, column=1, pady=10)

# label for text
txt_label = tk.Label(root, text="Enter text here: ")
txt_label.grid(row=2, column=0, pady=10)

# entry for text
txt_entry = tk.Entry(root)
txt_entry.grid(row=2, column=1, pady=10)

# label for font
font_label = tk.Label(root, text="Select font: ")
font_label.grid(row=3, column=0, pady=10)

# drop-down for font
select_font_combo = ttk.Combobox(
    root,
    values=list(fonts_dict.keys()),
    state="readonly",
)
select_font_combo.grid(row=3, column=1, pady=10)

# set default placeholder text
select_font_combo.set("-Select-")

# label for font size
font_size_label = tk.Label(root, text="Font size: ")
font_size_label.grid(row=4, column=0, pady=10)

# drop-down for font size
font_size_combo = ttk.Combobox(root, values=list(range(5, 501, 5)), state="readonly")
font_size_combo.grid(row=4, column=1, pady=10)
# set default placeholder text
font_size_combo.set("-Select-")

# label for position
position_label = tk.Label(root, text="Select position: ")
position_label.grid(row=5, column=0, pady=10)

# drop-down for position
txt_position = ttk.Combobox(
    root, values=list(position_code_dict.keys()), state="readonly"
)
txt_position.grid(row=5, column=1, pady=10)
# set default placeholder text
txt_position.set("-Select-")

# color label
color_label = tk.Label(root, text="Enter R, G, B values: ")
color_label.grid(row=6, column=1, pady=10)

# rgb values
r_label = tk.Label(root, text="Enter R value: ")
g_label = tk.Label(root, text="Enter G value: ")
b_label = tk.Label(root, text="Enter B value: ")

r_label.grid(row=7, column=0, pady=10)
g_label.grid(row=8, column=0, pady=10)
b_label.grid(row=9, column=0, pady=10)

r_value = ttk.Combobox(root, values=list(range(0, 256)), state="readonly")
g_value = ttk.Combobox(root, values=list(range(0, 256)), state="readonly")
b_value = ttk.Combobox(root, values=list(range(0, 256)), state="readonly")

r_value.grid(row=7, column=1, pady=10)
g_value.grid(row=8, column=1, pady=10)
b_value.grid(row=9, column=1, pady=10)

r_value.set("-Select-")
g_value.set("-Select-")
b_value.set("-Select-")

# preview btn
preview_btn = tk.Button(root, text="Preview image", command=preview)
preview_btn.grid(row=10, column=1, pady=10)

# save btn
save_btn = tk.Button(root, text="Save image", command=save_image)
save_btn.grid(row=11, column=1, pady=10)

# img label
img_label = tk.Label(root)
img_label.grid(row=2, column=2, padx=10, pady=10, rowspan=20)

# status label
status_label = tk.Label(
    root, text="No image loaded", bd=1, relief=tk.SUNKEN, anchor=tk.W
)
status_label.grid(row=1, column=2, padx=10, pady=10)

root.mainloop()
