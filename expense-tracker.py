import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# --- FUNCTIONS ---

def save_to_file():
    item = item_entry.get()
    amount = amount_entry.get()
    if item == "" or amount == "":
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("expenses.txt", "a") as file:
            file.write(f"{current_time}|{item}|{amount}\n")
        item_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        load_data() 
    except Exception as e:
        messagebox.showerror("Error", f"Could not save: {e}")

def load_data(search_term=""):
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open("expenses.txt", "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    # Search Logic
                    if search_term.lower() in parts[1].lower():
                        tree.insert("", tk.END, values=(parts[0], parts[1], parts[2]))
    except FileNotFoundError:
        pass

def delete_expense():
    selected_item = tree.selection() # Select Table rows
    if not selected_item:
        messagebox.showwarning("Delete Error", "Please select a row to delete!")
        return
    
    # Get data of row
    values = tree.item(selected_item)['values']
    line_to_delete = f"{values[0]}|{values[1]}|{values[2]}\n"
    
    # Read files and write back except the line to delete
    with open("expenses.txt", "r") as file:
        lines = file.readlines()
    
    with open("expenses.txt", "w") as file:
        for line in lines:
            if line != line_to_delete:
                file.write(line)
    
    load_data()
    messagebox.showinfo("Success", "Expense deleted!")

def on_search(event):
    # Search box and update table as user types
    load_data(search_entry.get())

# --- GUI SETUP ---
root = tk.Tk()
root.title("Advanced Expense Manager")
root.geometry("650x550")

# --- Input Section ---
input_frame = tk.LabelFrame(root, text="Add New Expense", padx=10, pady=10)
input_frame.pack(pady=10, fill="x", padx=20)

tk.Label(input_frame, text="Item:").grid(row=0, column=0)
item_entry = tk.Entry(input_frame)
item_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Amount:").grid(row=0, column=2)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=0, column=3, padx=5)

add_btn = tk.Button(input_frame, text="Add", command=save_to_file, bg="green", fg="white", width=10)
add_btn.grid(row=0, column=4, padx=5)

# --- Search Section ---
search_frame = tk.Frame(root)
search_frame.pack(pady=10, fill="x", padx=20)

tk.Label(search_frame, text="Search by Item Name:").pack(side="left")
search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", padx=10, fill="x", expand=True)
search_entry.bind("<KeyRelease>", on_search) # Key release event to trigger search as user types

# --- Table Section ---
tree = ttk.Treeview(root, columns=("date", "item", "amount"), show="headings")
tree.heading("date", text="Date & Time")
tree.heading("item", text="Item Name")
tree.heading("amount", text="Cost (Rs)")
tree.pack(pady=10, fill="both", expand=True, padx=20)

# --- Action Section ---
delete_btn = tk.Button(root, text="Delete Selected Expense", command=delete_expense, bg="red", fg="white")
delete_btn.pack(pady=10)

load_data()
root.mainloop()