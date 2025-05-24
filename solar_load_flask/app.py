from flask import Flask, render_template, request, jsonify, send_file
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# In-memory storage for appliances
appliances = []

@app.route('/')
def index():
    return render_template('index.html', appliances=appliances)

@app.route('/add_appliance', methods=['POST'])
def add_appliance():
    try:
        data = request.form
        name = data.get('name')
        power = float(data.get('power'))
        quantity = int(data.get('quantity'))
        hours = float(data.get('hours'))

        if not name:
            return jsonify({'error': 'Appliance name is required'}), 400

        appliance = {
            'name': name,
            'power': power,
            'quantity': quantity,
            'hours_per_day': hours
        }

        idx = data.get('index')
        if idx and idx.isdigit():
            appliances[int(idx)] = appliance
        else:
            appliances.append(appliance)

        return jsonify({'appliances': appliances})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/remove_appliance/<int:index>', methods=['DELETE'])
def remove_appliance(index):
    if 0 <= index < len(appliances):
        appliances.pop(index)
        return jsonify({'appliances': appliances})
    return jsonify({'error': 'Invalid index'}), 400

@app.route('/get_appliance/<int:index>', methods=['GET'])
def get_appliance(index):
    if 0 <= index < len(appliances):
        return jsonify(appliances[index])
    return jsonify({'error': 'Invalid index'}), 400

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.form
        battery_voltage = float(data.get('battery_voltage'))
        sun_hours = float(data.get('sun_hours'))
        efficiency = float(data.get('efficiency'))
        dod = float(data.get('dod'))
        autonomy = float(data.get('autonomy'))

        if not appliances:
            return jsonify({'error': 'No appliances added'}), 400

        total_energy = sum(a['power'] * a['quantity'] * a['hours_per_day'] for a in appliances)
        peak_load = sum(a['power'] * a['quantity'] for a in appliances)
        panel_size = total_energy / (sun_hours * efficiency)
        battery_capacity = (total_energy * autonomy) / (battery_voltage * dod)
        inverter_size = peak_load * 1.3

        summary = {
            'total_energy': round(total_energy, 2),
            'panel_size': round(panel_size, 2),
            'battery_capacity': round(battery_capacity, 2),
            'inverter_size': round(inverter_size, 2),
            'battery_voltage': battery_voltage
        }
        return jsonify(summary)
    except ValueError as e:
        return jsonify({'error': 'Invalid system parameters'}), 400

@app.route('/export_csv', methods=['GET'])
def export_csv():
    if not appliances:
        return jsonify({'error': 'No appliances to export'}), 400

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Power (W)', 'Quantity', 'Hours/Day'])
    for a in appliances:
        writer.writerow([a['name'], a['power'], a['quantity'], a['hours_per_day']])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='appliances.csv'
    )

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    if not appliances:
        return jsonify({'error': 'No appliances to export'}), 400

    try:
        battery_voltage = float(request.form.get('battery_voltage'))
        sun_hours = float(request.form.get('sun_hours'))
        efficiency = float(request.form.get('efficiency'))
        dod = float(request.form.get('dod'))
        autonomy = float(request.form.get('autonomy'))

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
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
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='solar_analysis.pdf'
        )
    except ValueError as e:
        return jsonify({'error': 'Invalid system parameters'}), 400

if __name__ == '__main__':
    app.run(debug=True)