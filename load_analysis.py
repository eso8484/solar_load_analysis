# Solar Load Analysis Script

# Sample appliance data (you can modify this)
appliances = [
    {"name": "LED Bulb", "power": 10, "quantity": 4, "hours_per_day": 5},
    {"name": "TV", "power": 100, "quantity": 1, "hours_per_day": 4},
    {"name": "Fridge", "power": 150, "quantity": 1, "hours_per_day": 24},
    {"name": "Fan", "power": 60, "quantity": 2, "hours_per_day": 8},
]

# Constants
sun_hours = 5            # Average daily peak sun hours
system_efficiency = 0.7  # 70% efficiency
battery_voltage = 12     # 12V battery
DoD = 0.5                # 50% Depth of Discharge
autonomy_days = 1        # Days of backup

# Step 1: Calculate energy consumption per appliance
total_energy = 0

print("Appliance Load Analysis:\n")
for appliance in appliances:
    daily_energy = appliance["power"] * appliance["quantity"] * appliance["hours_per_day"]
    total_energy += daily_energy
    print(f"{appliance['name']}: {daily_energy} Wh/day")

# Step 2: Solar Panel Sizing
panel_size_watts = total_energy / (sun_hours * system_efficiency)

# Step 3: Battery Sizing
battery_capacity_ah = (total_energy * autonomy_days) / (battery_voltage * DoD)

# Step 4: Inverter Sizing (Peak Load)
peak_load = sum([appliance["power"] * appliance["quantity"] for appliance in appliances])
inverter_size = peak_load * 1.3  # Add 30% margin

# Results
print("\n--- Summary ---")
print(f"Total Daily Load: {total_energy:.2f} Wh")
print(f"Recommended Solar Panel Size: {panel_size_watts:.2f} W")
print(f"Recommended Battery Capacity: {battery_capacity_ah:.2f} Ah at {battery_voltage}V")
print(f"Suggested Inverter Size: {inverter_size:.2f} W")
