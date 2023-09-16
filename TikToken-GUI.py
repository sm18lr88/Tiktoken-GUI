import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD
import tiktoken

def count_tokens(text, model_name):
    model_to_encoding = {
        "gpt-4": "cl100k_base",
        "gpt-3.5-turbo": "cl100k_base",
        "gpt-35-turbo": "cl100k_base",
        "text-davinci-003": "p50k_base",
        "text-davinci-002": "p50k_base",
        "text-davinci-001": "r50k_base",
        "text-curie-001": "r50k_base",
        "text-babbage-001": "r50k_base",
        "text-ada-001": "r50k_base",
        "davinci": "r50k_base",
        "curie": "r50k_base",
        "babbage": "r50k_base",
        "ada": "r50k_base"
    }
    encoding = model_to_encoding[model_name]
    enc = tiktoken.get_encoding(encoding)
    tokens = enc.encode(text)
    token_count = len(tokens)
    return token_count

def count_tokens_file(file_path, model_name):
    with open(file_path, 'r') as file:
        text = file.read()
    return count_tokens(text, model_name)

def count_chars_words(text):
    chars = len(text)
    words = len(text.split())
    return chars, words

def calculate_difference(limit, count):
    difference = count - limit
    if difference < 0:
        return f'{abs(difference)} remaining'
    else:
        return f'Exceeds by {difference}'

def begin_count():
    text = text_box.get("1.0", 'end-1c')
    token_count = count_tokens(text, model.get())
    chars, words = count_chars_words(text)
    
    token_difference = calculate_difference(4096, token_count)  # GPT-4 limit
    char_difference = calculate_difference(160, chars)  # Twitter limit

    report = (f'Token count: {token_count}\n'
              f'ChatGPT Plus: {token_difference}\n'
              f'Character count: {chars}\n'
              f'Twitter post: {char_difference}\n'
              f'Word count: {words}')

    messagebox.showinfo("Count", report)

root = TkinterDnD.Tk()
root.minsize(300, 450)
root.title('TikToken')

text_box = tk.Text(root)
text_box.pack(fill='both', expand=True)

begin_count_button = tk.Button(root, text="Begin Count", command=begin_count)
begin_count_button.pack(side='left')

model_list = ["gpt-4", "gpt-3.5-turbo", "gpt-35-turbo", "text-davinci-003", "text-davinci-002", "text-davinci-001",
              "text-curie-001", "text-babbage-001", "text-ada-001", "davinci", "curie", "babbage", "ada"]
model = tk.StringVar()
model.set(model_list[0])  # set default value as GPT-4

model_select_menu = ttk.Combobox(root, textvariable=model, values=model_list)
model_select_menu.pack(side='left')

root.mainloop()
