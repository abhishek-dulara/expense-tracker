import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 # Built-in library for Database
import datetime

# --- DATABASE SETUP ---
def init_db():
    # Connect to database file (it will create if not exists)
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    # Create a table to store data
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses 
                      (id INTEGER PRIMARY KEY, date TEXT, item TEXT, amount REAL)''')
    conn.commit()
    conn.close()

# --- FUNCTIONS ---

def add_expense():
    item = item_entry.get()
    amount = amount_entry.get()
    
    if item == "" or amount == "":
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    try:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Insert data into Database
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (date, item, amount) VALUES (?, ?, ?)", 
                       (date_str, item, float(amount)))
        conn.commit()
        conn.close()

        item_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        load_data()
        messagebox.showinfo("Success", "Expense added to Database!")
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")

def load_data(search_term=""):
    for row in tree.get_children():
        tree.delete(row)
        
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    # SQL query to search or get all data
    if search_term:
        cursor.execute("SELECT * FROM expenses WHERE item LIKE ?", ('%' + search_term + '%',))
    else:
        cursor.execute("SELECT * FROM expenses")
        
    rows = cursor.fetchall()
    for row in rows:
        # row[0] is ID, row[1] is Date, row[2] is Item, row[3] is Amount
        tree.insert("", tk.END, values=(row[1], row[2], row[3]))
    
    conn.close()

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a row to delete!")
        return
    
    # Get values of the selected row
    item_values = tree.item(selected)['values']
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    # Delete based on Date and Item (More professional to use ID)
    cursor.execute("DELETE FROM expenses WHERE date = ? AND item = ?", (item_values[0], item_values[1]))
    conn.commit()
    conn.close()
    
    load_data()
    messagebox.showinfo("Success", "Deleted from Database!")

# --- GUI SETUP ---
root = tk.Tk()
root.title("Database Expense Manager")
root.geometry("600x500")

# Database Initialization
init_db()

# Input UI
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Item:").grid(row=0, column=0)
item_entry = tk.Entry(frame)
item_entry.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Amount:").grid(row=0, column=2)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=0, column=3, padx=5)

tk.Button(frame, text="Add", command=add_expense, bg="green", fg="white").grid(row=0, column=4, padx=5)

# Search UI
search_var = tk.StringVar()
search_var.trace("w", lambda name, index, mode, sv=search_var: load_data(sv.get()))
tk.Label(root, text="Search Item:").pack()
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack(pady=5)

# Table UI
tree = ttk.Treeview(root, columns=("Date", "Item", "Amount"), show="headings")
tree.heading("Date", text="Date")
tree.heading("Item", text="Item")
tree.heading("Amount", text="Amount")
tree.pack(fill="both", expand=True, padx=20, pady=10)

tk.Button(root, text="Delete Selected", command=delete_selected, bg="red", fg="white").pack(pady=10)

load_data()
root.mainloop()



