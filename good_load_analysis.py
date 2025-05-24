import tkinter as tk
from tkinter import ttk, messagebox

appliances = []

def add_appliance():
    name = entry_name.get()
    try:
        power = float(entry_power.get())
        quantity = int(entry_quantity.get())
        hours = float(entry_hours.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter numeric values for Power, Quantity, and Hours.")
        return

    if not name:
        messagebox.showerror("Input Error", "Appliance name cannot be empty.")
        return

    appliances.append({
        "name": name,
        "power": power,
        "quantity": quantity,
        "hours_per_day": hours
    })

    tree.insert('', tk.END, values=(name, power, quantity, hours))
    entry_name.delete(0, tk.END)
    entry_power.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_hours.delete(0, tk.END)

def calculate_load():
    if not appliances:
        messagebox.showinfo("No Data", "Please add appliances first.")
        return

    total_energy = 0
    for app in appliances:
        daily_energy = app["power"] * app["quantity"] * app["hours_per_day"]
        total_energy += daily_energy

    sun_hours = 5
    efficiency = 0.7
    battery_voltage = 12
    DoD = 0.5
    autonomy_days = 1

    panel_size = total_energy / (sun_hours * efficiency)
    battery_ah = (total_energy * autonomy_days) / (battery_voltage * DoD)
    peak_load = sum(app["power"] * app["quantity"] for app in appliances)
    inverter_size = peak_load * 1.3

    result = f"""\
Total Daily Load: {total_energy:.2f} Wh
Recommended Solar Panel Size: {panel_size:.2f} W
Recommended Battery Capacity: {battery_ah:.2f} Ah at {battery_voltage}V
Suggested Inverter Size: {inverter_size:.2f} W"""

    messagebox.showinfo("Load Analysis Result", result)

# GUI
root = tk.Tk()
root.title("Solar Load Analysis Tool")
root.geometry("600x500")

# Input Frame
frame_input = tk.LabelFrame(root, text="Enter Appliance Details", padx=10, pady=10)
frame_input.pack(padx=10, pady=10, fill="x")

tk.Label(frame_input, text="Name").grid(row=0, column=0)
tk.Label(frame_input, text="Power (W)").grid(row=0, column=1)
tk.Label(frame_input, text="Qty").grid(row=0, column=2)
tk.Label(frame_input, text="Hours/Day").grid(row=0, column=3)

entry_name = tk.Entry(frame_input)
entry_power = tk.Entry(frame_input)
entry_quantity = tk.Entry(frame_input)
entry_hours = tk.Entry(frame_input)

entry_name.grid(row=1, column=0)
entry_power.grid(row=1, column=1)
entry_quantity.grid(row=1, column=2)
entry_hours.grid(row=1, column=3)

btn_add = tk.Button(frame_input, text="Add Appliance", command=add_appliance)
btn_add.grid(row=1, column=4, padx=10)

# Appliance Table
frame_table = tk.LabelFrame(root, text="Appliances Added")
frame_table.pack(padx=10, pady=10, fill="both", expand=True)

tree = ttk.Treeview(frame_table, columns=("Name", "Power", "Qty", "Hours"), show="headings")
for col in ("Name", "Power", "Qty", "Hours"):
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)
tree.pack(fill="both", expand=True)

# Calculate Button
btn_calc = tk.Button(root, text="Calculate Load Analysis", command=calculate_load, bg="green", fg="white")
btn_calc.pack(pady=10)

root.mainloop()
