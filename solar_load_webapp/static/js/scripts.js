function clearForm() {
    document.getElementById('appliance-form').reset();
    document.getElementById('edit-index').value = '';
}

function updateApplianceList(appliances) {
    const list = document.getElementById('appliance-list');
    list.innerHTML = '';
    appliances.forEach((appliance, idx) => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            ${appliance.name} - ${appliance.power}W x ${appliance.quantity} for ${appliance.hours_per_day}h/day
            <div>
                <button class="btn btn-sm btn-warning" onclick="editAppliance(${idx})">Edit</button>
                <button class="btn btn-sm btn-danger" onclick="removeAppliance(${idx})">Remove</button>
            </div>
        `;
        list.appendChild(li);
    });
}

document.getElementById('appliance-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        const response = await fetch('/add_appliance', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            updateApplianceList(data.appliances);
            clearForm();
        } else {
            alert(data.error);
        }
    } catch (err) {
        alert('Error adding appliance');
    }
});

async function removeAppliance(index) {
    try {
        const response = await fetch(`/remove_appliance/${index}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        if (response.ok) {
            updateApplianceList(data.appliances);
            clearForm();
        } else {
            alert(data.error);
        }
    } catch (err) {
        alert('Error removing appliance');
    }
}

async function editAppliance(index) {
    try {
        const response = await fetch(`/get_appliance/${index}`);
        const appliance = await response.json();
        if (response.ok) {
            document.getElementById('edit-index').value = index;
            document.getElementById('name').value = appliance.name;
            document.getElementById('power').value = appliance.power;
            document.getElementById('quantity').value = appliance.quantity;
            document.getElementById('hours').value = appliance.hours_per_day;
        } else {
            alert(appliance.error);
        }
    } catch (err) {
        alert('Error fetching appliance');
    }
}

document.getElementById('analysis-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            const results = `
--- Summary ---
Total Daily Energy Demand: ${data.total_energy} Wh
Recommended Solar Panel Size: ${data.panel_size} W
Recommended Battery Capacity: ${data.battery_capacity} Ah @ ${data.battery_voltage}V
Suggested Inverter Size: ${data.inverter_size} W
            `;
            document.getElementById('results').textContent = results;
        } else {
            alert(data.error);
        }
    } catch (err) {
        alert('Error running analysis');
    }
});

function exportCSV() {
    window.location.href = '/export_csv';
}

async function exportPDF() {
    const formData = new FormData(document.getElementById('analysis-form'));
    try {
        const response = await fetch('/export_pdf', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'solar_analysis.pdf';
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            const data = await response.json();
            alert(data.error);
        }
    } catch (err) {
        alert('Error exporting PDF');
    }
}