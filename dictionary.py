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
# GUI App
# -----------------------------------------------------------
root = tk.Tk()
root.title("Dictionary")
root.geometry("900x500")

# ------------------ SEARCH TAB ------------------

search_frame = ttk.Frame(root)
search_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(search_frame, text="Search for a word: ").grid(row=0, column=0)
search_var = tk.StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var, width = 50)
search_entry.grid(row=0, column=1, padx=5)

# ------------------ RESULT TAB ------------------

results_frame = tk.Frame(root)
results_frame.pack(fill="both", expand=True, padx=10, pady=5)
result_label = ttk.Label(results_frame, text="")
result_label.grid(row=1, column=0, sticky="w")


def perform_search():
    query = search_var.get().strip()
    if not query:
        return
    
    result = search(query)
    result_label.config(text=result)

ttk.Button(search_frame, text="Search", command=perform_search).grid(row=0, column=2, padx=5)

root.mainloop()