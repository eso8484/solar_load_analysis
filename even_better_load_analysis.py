import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
appliances = []

def add_appliance():
    try:
        name = name_entry.get()
        power = float(power_entry.get())
        quantity = int(quantity_entry.get())
        hours = float(hours_entry.get())

        if not name:
            raise ValueError("Appliance name is required.")

        selected = appliance_listbox.curselection()
        if selected:
            idx = selected[0]
            appliances[idx] = {"name": name, "power": power, "quantity": quantity, "hours_per_day": hours}
        else:
            appliances.append({"name": name, "power": power, "quantity": quantity, "hours_per_day": hours})

        refresh_appliance_list()
        clear_fields()

    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))

def remove_appliance():
    selected = appliance_listbox.curselection()
    if selected:
        idx = selected[0]
        del appliances[idx]
        refresh_appliance_list()
        clear_fields()

def edit_appliance():
    selected = appliance_listbox.curselection()
    if selected:
        idx = selected[0]
        appliance = appliances[idx]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, appliance["name"])
        power_entry.delete(0, tk.END)
        power_entry.insert(0, appliance["power"])
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, appliance["quantity"])
        hours_entry.delete(0, tk.END)
        hours_entry.insert(0, appliance["hours_per_day"])

def clear_fields():
    name_entry.delete(0, tk.END)
    power_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    hours_entry.delete(0, tk.END)
    appliance_listbox.selection_clear(0, tk.END)

def refresh_appliance_list():
    appliance_listbox.delete(0, tk.END)
    for a in appliances:
        item = f"{a['name']} - {a['power']}W x {a['quantity']} for {a['hours_per_day']}h/day"
        appliance_listbox.insert(tk.END, item)

def run_analysis():
    if not appliances:
        messagebox.showwarning("No appliances", "Please add at least one appliance.")
        return

    try:
        battery_voltage = float(battery_voltage_entry.get())
        sun_hours = float(sun_hours_entry.get())
        efficiency = float(efficiency_entry.get())
        dod = float(dod_entry.get())
        autonomy = float(autonomy_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid system parameters.")
        return

    total_energy = 0
    peak_load = 0

    for appliance in appliances:
        energy = appliance["power"] * appliance["quantity"] * appliance["hours_per_day"]
        total_energy += energy
        peak_load += appliance["power"] * appliance["quantity"]

    panel_size = total_energy / (sun_hours * efficiency)
    battery_capacity = (total_energy * autonomy) / (battery_voltage * dod)
    inverter_size = peak_load * 1.3

    summary = (
        f"--- Summary ---\n"
        f"Total Daily Energy Demand: {total_energy:.2f} Wh\n"
        f"Recommended Solar Panel Size: {panel_size:.2f} W\n"
        f"Recommended Battery Capacity: {battery_capacity:.2f} Ah @ {battery_voltage}V\n"
        f"Suggested Inverter Size: {inverter_size:.2f} W"
    )

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, summary)

def export_to_pdf():
    if not appliances:
        messagebox.showwarning("No data", "No appliances to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 50

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Solar Load Analysis Report")
        y -= 30

        c.setFont("Helvetica", 12)
        c.drawString(50, y, "Appliance List:")
        y -= 20

        for a in appliances:
            line = f"{a['name']} - {a['power']}W x {a['quantity']} for {a['hours_per_day']}h/day"
            c.drawString(60, y, line)
            y -= 18
            if y < 100:
                c.showPage()
                y = height - 50

        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "System Analysis Summary:")
        y -= 20

        # Recalculate values for summary
        try:
            battery_voltage = float(battery_voltage_entry.get())
            sun_hours = float(sun_hours_entry.get())
            efficiency = float(efficiency_entry.get())
            dod = float(dod_entry.get())
            autonomy = float(autonomy_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid system parameters.")
            return

        total_energy = sum(a['power'] * a['quantity'] * a['hours_per_day'] for a in appliances)
        peak_load = sum(a['power'] * a['quantity'] for a in appliances)
        panel_size = total_energy / (sun_hours * efficiency)
        battery_capacity = (total_energy * autonomy) / (battery_voltage * dod)
        inverter_size = peak_load * 1.3

        summary_lines = [
            f"Total Daily Energy Demand: {total_energy:.2f} Wh",
            f"Recommended Solar Panel Size: {panel_size:.2f} W",
            f"Recommended Battery Capacity: {battery_capacity:.2f} Ah @ {battery_voltage}V",
            f"Suggested Inverter Size: {inverter_size:.2f} W"
        ]

        c.setFont("Helvetica", 11)
        for line in summary_lines:
            c.drawString(60, y, line)
            y -= 18
            if y < 100:
                c.showPage()
                y = height - 50

        c.save()
        messagebox.showinfo("PDF Exported", "PDF file created successfully.")

def export_to_csv():
    if not appliances:
        messagebox.showwarning("No data", "No appliances to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Power (W)", "Quantity", "Hours/Day"])
            for a in appliances:
                writer.writerow([a["name"], a["power"], a["quantity"], a["hours_per_day"]])
        messagebox.showinfo("Success", "Data exported successfully!")

# GUI Setup
root = tk.Tk()
root.title("Solar Load Analysis Tool")

# Appliance inputs
tk.Label(root, text="Appliance Name").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Power (W)").grid(row=1, column=0)
power_entry = tk.Entry(root)
power_entry.grid(row=1, column=1)

tk.Label(root, text="Quantity").grid(row=2, column=0)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=2, column=1)

tk.Label(root, text="Hours/Day").grid(row=3, column=0)
hours_entry = tk.Entry(root)
hours_entry.grid(row=3, column=1)

tk.Button(root, text="Add/Update", command=add_appliance).grid(row=4, column=0, columnspan=2, pady=5)
tk.Button(root, text="Edit Selected", command=edit_appliance).grid(row=5, column=0)
tk.Button(root, text="Remove Selected", command=remove_appliance).grid(row=5, column=1)

# Appliance list
appliance_listbox = tk.Listbox(root, width=50)
appliance_listbox.grid(row=6, column=0, columnspan=2, pady=10)

# System parameters
tk.Label(root, text="Battery Voltage (V):").grid(row=7, column=0)
battery_voltage_entry = tk.Entry(root)
battery_voltage_entry.insert(0, "48")
battery_voltage_entry.grid(row=7, column=1)

tk.Label(root, text="Sun Hours:").grid(row=8, column=0)
sun_hours_entry = tk.Entry(root)
sun_hours_entry.insert(0, "5")
sun_hours_entry.grid(row=8, column=1)

tk.Label(root, text="System Efficiency (0.7):").grid(row=9, column=0)
efficiency_entry = tk.Entry(root)
efficiency_entry.insert(0, "0.7")
efficiency_entry.grid(row=9, column=1)

tk.Label(root, text="Battery DoD (0.95):").grid(row=10, column=0)
dod_entry = tk.Entry(root)
dod_entry.insert(0, "0.95")
dod_entry.grid(row=10, column=1)

tk.Label(root, text="Autonomy Days:").grid(row=11, column=0)
autonomy_entry = tk.Entry(root)
autonomy_entry.insert(0, "1")
autonomy_entry.grid(row=11, column=1)

# Results & Actions
tk.Button(root, text="Run Load Analysis", command=run_analysis).grid(row=12, column=0, columnspan=2, pady=5)
tk.Button(root, text="Export to CSV", command=export_to_csv).grid(row=13, column=0, columnspan=2)
tk.Button(root, text="Export to PDF", command=export_to_pdf).grid(row=13, column=1)

result_text = tk.Text(root, height=8, width=60)
result_text.grid(row=14, column=0, columnspan=2, pady=10)

root.mainloop()
