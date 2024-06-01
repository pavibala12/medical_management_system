document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('patient-form');
    const patientList = document.getElementById('patients-list');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        const patientData = {};
        formData.forEach((value, key) => {
            patientData[key] = value;
        });

        fetch('/add_patient', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(patientData),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayPatients();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function displayPatients() {
        fetch('/patients')
        .then(response => response.json())
        .then(data => {
            patientList.innerHTML = '';
            data.forEach(patient => {
                const patientItem = document.createElement('div');
                patientItem.innerHTML = `
                    <p><strong>Name:</strong> ${patient.name}</p>
                    <p><strong>Age:</strong> ${patient.age}</p>
                    <p><strong>Medical History:</strong> ${patient.medical_history}</p>
                    <button onclick="deletePatient('${patient._id}')">Delete</button>
                `;
                patientList.appendChild(patientItem);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    window.deletePatient = function(patientId) {
        fetch(`/delete_patient/${patientId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayPatients();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    displayPatients();
});

