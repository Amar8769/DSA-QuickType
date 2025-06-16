import os
import tkinter as tk
import pyautogui
import time
import threading
import pyperclip
from fuzzywuzzy import process

root = tk.Tk()
root.title("DSA Snippet Viewer")

text = tk.Text(root, height=10)
text.pack()

entry = tk.Entry(root)
entry.pack()

status = tk.Label(root, text="")
status.pack()

animated = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Animated Typing", variable=animated).pack()

delay_label = tk.Label(root, text="Delay (seconds):")
delay_label.pack()

delay_slider = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
delay_slider.set(2)
delay_slider.pack()

def type_snippet(snippet):
    delay = delay_slider.get()
    status.config(text=f"Waiting {delay} seconds before typing...")
    time.sleep(delay)

    if animated.get():
        status.config(text="Typing with animation...")
        for char in snippet:
            pyautogui.write(char)
            time.sleep(0.05)
    else:
        status.config(text="Pasting instantly...")
        pyperclip.copy(snippet)
        pyautogui.hotkey("ctrl", "v")

    status.config(text="Typing finished.")

def get_input():
    text.delete(1.0, tk.END)
    content = ""
    userInput = entry.get().replace(' ', '_').lower().strip()
    folder = ".dsa_snippets"

    files = [f[:-4] for f in os.listdir(folder) if f.endswith(".txt")]
    best_match, score = process.extractOne(userInput, files)

    if score < 60:
        content = f"No good match found for '{userInput}'"
    else:
        filename = os.path.join(folder, f"{best_match}.txt")

        try:
            with open(filename, 'r') as file:
                content = file.read()

            threading.Thread(target=type_snippet, args=(content,), daemon=True).start()
            status.config(text="Preparing to type..." if animated.get() else "Preparing to insert...")

        except FileNotFoundError:
            content = f"File '{filename}' not found. Please check the filename and try again."

    text.insert(tk.END, content)
    entry.delete(0, tk.END)

root.bind("<Return>", lambda event: get_input())
root.bind("<Escape>", lambda event: root.destroy())

tk.Button(root, text="Get Input", command=get_input).pack()

root.mainloop()
