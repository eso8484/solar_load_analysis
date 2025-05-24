# Interactive Solar Load Analysis Script

def get_appliance_data():
    appliances = []
    print("\nEnter appliance details (type 'done' to finish):")

    while True:
        name = input("\nAppliance name: ")
        if name.lower() == "done":
            break
        try:
            power = float(input("Power rating in watts (W): "))
            quantity = int(input("Quantity: "))
            hours = float(input("Hours used per day: "))
            appliances.append({
                "name": name,
                "power": power,
                "quantity": quantity,
                "hours_per_day": hours
            })
        except ValueError:
            print("Invalid input. Please enter numeric values for power, quantity, and hours.")

    return appliances

def get_battery_voltage():
    while True:
        try:
            battery_voltage = int(input("Enter system voltage (12, 24 or 48): "))
            if battery_voltage in [12, 24, 48]:
                return battery_voltage
            else:
                print("Please enter 12, 24, or 48 only.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def load_analysis(appliances, battery_voltage, sun_hours=5, efficiency=0.7, DoD=0.5, autonomy_days=1):
    total_energy = 0

    print("\nAppliance Load Analysis:")
    for appliance in appliances:
        daily_energy = appliance["power"] * appliance["quantity"] * appliance["hours_per_day"]
        total_energy += daily_energy
        print(f"- {appliance['name']}: {daily_energy:.2f} Wh/day")

    # Solar panel size
    panel_size_watts = total_energy / (sun_hours * efficiency)

    # Battery size
    battery_capacity_ah = (total_energy * autonomy_days) / (battery_voltage * DoD)

    # Inverter sizing
    peak_load = sum([a["power"] * a["quantity"] for a in appliances])
    inverter_size = peak_load * 1.3  # 30% margin

    print("\n--- Summary ---")
    print(f"Total Daily Energy Demand: {total_energy:.2f} Wh")
    print(f"Recommended Solar Panel Size: {panel_size_watts:.2f} W")
    print(f"Recommended Battery Capacity: {battery_capacity_ah:.2f} Ah @ {battery_voltage}V")
    print(f"Suggested Inverter Size: {inverter_size:.2f} W")


# Main
print("SOLAR LOAD ANALYSIS TOOL")

appliances = get_appliance_data()
if appliances:
    voltage = get_battery_voltage()
    load_analysis(appliances, voltage)
else:
    print("No appliances entered. Exiting.")
