import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------- DATABASE SETUP ----------
def connect_db():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            department TEXT,
            salary REAL
        )
    """)
    conn.commit()
    conn.close()

connect_db()

# ---------- FUNCTIONS ----------
def add_employee():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    dept = dept_entry.get()
    salary = salary_entry.get()

    if name == "" or age == "" or dept == "" or salary == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employee (name, age, gender, department, salary) VALUES (?, ?, ?, ?, ?)",
                   (name, age, gender, dept, salary))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Employee added successfully!")
    clear_entries()
    fetch_data()

def fetch_data():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee")
    rows = cursor.fetchall()
    employee_table.delete(*employee_table.get_children())
    for row in rows:
        employee_table.insert("", tk.END, values=row)
    conn.close()

def clear_entries():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    gender_var.set("")

def get_selected(event):
    selected = employee_table.focus()
    if not selected:
        return
    values = employee_table.item(selected, "values")
    clear_entries()
    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    gender_var.set(values[3])
    dept_entry.insert(0, values[4])
    salary_entry.insert(0, values[5])

def update_employee():
    selected = employee_table.focus()
    if not selected:
        messagebox.showerror("Error", "Please select an employee to update!")
        return
    emp_id = employee_table.item(selected, "values")[0]

    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employee SET name=?, age=?, gender=?, department=?, salary=?
        WHERE id=?
    """, (name_entry.get(), age_entry.get(), gender_var.get(),
          dept_entry.get(), salary_entry.get(), emp_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Updated", "Employee record updated successfully!")
    clear_entries()
    fetch_data()

def delete_employee():
    selected = employee_table.focus()
    if not selected:
        messagebox.showerror("Error", "Please select an employee to delete!")
        return
    emp_id = employee_table.item(selected, "values")[0]

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?")
    if confirm:
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employee WHERE id=?", (emp_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Employee deleted successfully!")
        fetch_data()

# ---------- GUI ----------
root = tk.Tk()
root.title("Employee Management System")
root.geometry("850x500")
root.resizable(False, False)

# Title
tk.Label(root, text="EMPLOYEE MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), bg="navy", fg="white", pady=10).pack(fill=tk.X)

# Frame for Input Fields
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=10)

tk.Label(frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
name_entry = tk.Entry(frame, width=30)
name_entry.grid(row=0, column=1, pady=5, padx=10)

tk.Label(frame, text="Age:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
age_entry = tk.Entry(frame, width=30)
age_entry.grid(row=1, column=1, pady=5, padx=10)

tk.Label(frame, text="Gender:", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
gender_var = tk.StringVar()
ttk.Combobox(frame, textvariable=gender_var, values=["Male", "Female", "Other"], width=28).grid(row=2, column=1, pady=5, padx=10)

tk.Label(frame, text="Department:", font=("Arial", 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
dept_entry = tk.Entry(frame, width=30)
dept_entry.grid(row=3, column=1, pady=5, padx=10)

tk.Label(frame, text="Salary:", font=("Arial", 12)).grid(row=4, column=0, sticky=tk.W, pady=5)
salary_entry = tk.Entry(frame, width=30)
salary_entry.grid(row=4, column=1, pady=5, padx=10)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", width=12, bg="green", fg="white", command=add_employee).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Update", width=12, bg="blue", fg="white", command=update_employee).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Delete", width=12, bg="red", fg="white", command=delete_employee).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Clear", width=12, bg="gray", fg="white", command=clear_entries).grid(row=0, column=3, padx=10)

# Table
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ("ID", "Name", "Age", "Gender", "Department", "Salary")
employee_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
for col in columns:
    employee_table.heading(col, text=col)
    employee_table.column(col, width=120)

employee_table.bind("<ButtonRelease-1>", get_selected)
employee_table.pack(fill=tk.X)

fetch_data()

root.mainloop()
