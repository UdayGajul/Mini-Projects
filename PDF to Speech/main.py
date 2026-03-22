import tkinter as tk
from tkinter import filedialog
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
from google.genai import types
import wave

load_dotenv()

file_path = None
full_text = ""


# Extract text from PDF
def extract_text_from_pdf():
    global full_text
    reader = PdfReader(file_path)

    for page in reader.pages:
        full_text += page.extract_text()
    print(full_text)


def select_pdf():
    global file_path
    try:
        file_path = filedialog.askopenfilename(  # initialdir="/",
            title="Select PDF File", filetypes=(("PDF file", "*.pdf"),)
        )

        if file_path:
            status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
            extract_text_from_pdf()
    except Exception as e:
        file_path = ""
        print("Error - ", e)


# Google AI Studio TTS
def convert_and_save_locally():
    global full_text
    if full_text != "":
        # Set up the wave file to save the output:
        client = genai.Client(api_key=os.getenv("GOOGLE_AI_STUDIO_TTS_API_KEY"))

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=full_text,  # text goes here
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Orus",
                        )
                    )
                ),
            ),
        )

        file_path_new = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=(("Wave file", "*.wav"), ("All files", "*.*")),
            title="Save your speech file",
        )

        if file_path_new:
            data = response.candidates[0].content.parts[0].inline_data.data

            with wave.open(file_path_new, "wb") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(24000)
                f.writeframes(data)
            print(f"File successfully saved to: {file_path_new}")
        else:
            print("Save operation cancelled.")


root = tk.Tk()

# maximized
root.state("zoomed")
# title
root.title("PDF to Speech Converter")
# app icon
root.iconbitmap("favicon.ico")

# title inside the window
tk.Label(
    root, text="Convert text inside PDF to Audio", font=("Garamond", 40, "bold")
).grid(row=0, column=0, padx=20, pady=20)

# open pdf file
open_pdf_file_btn = tk.Button(root, text="Open PDF file", command=select_pdf)
open_pdf_file_btn.grid(row=1, column=0, pady=10)

# status label
status_label = tk.Label(
    root, text="No PDF file loaded", bd=1, relief=tk.SUNKEN, anchor=tk.W
)
status_label.grid(row=2, column=0, pady=10)

# convert and save btn
convert_save_btn = tk.Button(
    root, text="Convert to Speech and Save", command=convert_and_save_locally
)
convert_save_btn.grid(row=3, column=0, pady=10)

# wait msg
tk.Label(
    root, text="Wait for few minutes after clicking on 'Covnert to Speech and Save'"
).grid(row=4, column=0, pady=10)

root.mainloop()
