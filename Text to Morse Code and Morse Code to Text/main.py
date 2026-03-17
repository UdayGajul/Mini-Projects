# Heading
print("Welcome! Convert text to Morse Code and Morse Code to text.")

# First take the user input
choice = int(
    input(
        "Choose any one option\n1. Text to Morse Code\n2. Morse Code to Text: \nEnter your choice: "
    )
)

# morse code dictionary, contains every character
text_to_morse_code_dict = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    ":": "---...",
    ";": "-.-.-.",
    "'": ".----.",
    "-": "-....-",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    '"': ".-..-.",
    "@": ".--.-.",
    "=": "-...-",
    "!": "-.-.--",
}

morse_code_to_text_dict = {value: key for key, value in text_to_morse_code_dict.items()}

final_list = []

# converting str to morse code
def text_to_morse_code(text):
    for e in text:
        # replace " " with "/"
        if e == " ":
            final_list.append("/")

        # replace the letter to code
        if e in text_to_morse_code_dict:
            final_list.append(text_to_morse_code_dict[e])

    # print the final output
    print("Morse code output:", *final_list)

# converting morse code to str
def morse_code_to_text(morse_code):
    morse_code_li = morse_code.split(" ")
    for e in morse_code_li:
        if e == "/":
            final_list.append(" ")
        if e in morse_code_to_text_dict:
            final_list.append(morse_code_to_text_dict[e])

    print("Text output:", ''.join(final_list))

if choice == 1:
    ui = input("Enter Text: ").upper()
    text_to_morse_code(ui)
if choice == 2:
    ui = input("Enter Morse code: ")
    morse_code_to_text(ui)
