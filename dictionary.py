import requests
import tkinter as tk
from tkinter import ttk

# -----------------------------------------------------------
# Querying through API
# -----------------------------------------------------------
error_handling = "Could not find word!"
def search(search_word):
    try:
        response = requests.get(f"https://freedictionaryapi.com/api/v1/entries/en/{search_word}")
        content = response.json()
        return(content["entries"][0]["senses"][0]["definition"])
    except:
        return(error_handling)

# -----------------------------------------------------------
# Gettin a random word
# -----------------------------------------------------------

def get_random_word():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word")
        word = response.json()[0]
        return word
    except:
        return None

# -----------------------------------------------------------
# GUI App
# -----------------------------------------------------------
root = tk.Tk()
root.title("Dictionary")
root.geometry("900x500")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# ------------------ HISTORY SIDEBAR ON LEFT ------------------

history_frame = tk.Frame(main_frame, width=200)
history_frame.pack(side="left", fill="y", padx=5, pady=5)
tk.Label(history_frame, text="History").pack()
history_list = tk.Listbox(history_frame)
history_list.pack(fill="both", expand=True)

def clear_history():
    history_list.delete(0, tk.END)

clear_btn = ttk.Button(history_frame, text="Clear History", command=clear_history)
clear_btn.pack(pady=5)

# ------------------ CONTENT AREA ON RIGHT ------------------

content_frame = tk.Frame(main_frame)
content_frame.pack(side="right", fill="both", expand=True)

# ------------------ SEARCH TAB IN CONTENT AREA ------------------

search_frame = ttk.Frame(content_frame)
search_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(search_frame, text="Search for a word: ").grid(row=0, column=0)
search_var = tk.StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var, width = 50)
search_entry.grid(row=0, column=1, padx=5)

# ------------------ RESULT TAB IN CONTENT AREA------------------

result_frame = tk.Frame(content_frame)
result_frame.pack(fill="both", expand=True, padx=10, pady=5)
result_label = ttk.Label(result_frame, text="", wraplength=600, justify="left")
result_label.grid(row=1, column=0, sticky="w")

# ------------------------------------------------------------------------------------
# Searching, diaplaying meaning + Adding to history + Redisplay meaning on clicking
# ------------------------------------------------------------------------------------

def add_to_history(word):
    words = history_list.get(0, tk.END)
    if word not in words:
        history_list.insert(tk.END, word)

def perform_search(word=None):
    if word is None:
        word = search_var.get().strip()

    if not word:
        return
    
    search_var.set(word)

    result = search(word)
    result_label.config(text=result)

    if result != error_handling:
        add_to_history(word)

def on_history_click(event):
    try:
        index = history_list.curselection()[0]
        word = history_list.get(index)
        perform_search(word)
    except:
        pass

history_list.bind("<<ListboxSelect>>", on_history_click)

ttk.Button(search_frame, text="Search", command=perform_search).grid(row=0, column=2, padx=5)

# -----------------------------------------------------------
# Word Of The Day (Pop-up)
# -----------------------------------------------------------

def show_word_of_the_day():
    word = get_random_word()
    if not word:
        return
    meaning = search(word)
    if meaning != error_handling:
        add_to_history(word)

    # ------------------ POP-UP WINDOW ------------------

    root.update_idletasks()
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    position_x = root_x + (root_width // 2) - (250 // 2)
    position_y = root_y + (root_height // 2) - (200 // 2)

    popup = tk.Toplevel(root)
    popup.title("Word of the Day")
    popup.geometry(f"{250}x{200}+{position_x}+{position_y}")
    popup.transient(root)   # keeps popup on top

    tk.Label(popup, text="Word of the Day", font=("bold")).pack(pady=10)
    tk.Label(popup, text=word, font=("bold")).pack(pady=5)

    meaning_label = tk.Label(popup, text=meaning, wraplength=350, justify="left")
    meaning_label.pack(padx=10, pady=10)

    ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

root.after(200, show_word_of_the_day)

root.mainloop()

