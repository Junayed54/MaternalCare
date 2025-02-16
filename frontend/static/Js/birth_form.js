document.addEventListener("DOMContentLoaded", function() {
    const checkPatientBtn = document.getElementById("checkPatient");
    const patientPhoneInput = document.getElementById("patient_phone");
    const patientMessage = document.getElementById("patientMessage");
    const patientIdInput = document.getElementById("patient_id");
    const deliveryForm = document.getElementById("deliveryForm");
    const motherStatusSelect = document.getElementById("mother_status");
    const deathDetails = document.getElementById("deathDetails");

    checkPatientBtn.addEventListener("click", function() {
        const phone = patientPhoneInput.value.trim();
        const accessToken = localStorage.getItem('access_token'); // Replace with actual token
        
        if (!phone) {
            patientMessage.innerHTML = '<div class="alert alert-danger">Please enter a phone number.</div>';
            return;
        }

        fetch(`/api/check_patient/`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"phone_number": phone})
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                patientMessage.innerHTML = '<div class="alert alert-success">Patient found.</div>';
                patientIdInput.value = data.patient_id;
                deliveryForm.style.display = "block";
            } else {
                patientMessage.innerHTML = '<div class="alert alert-warning">Patient not found.</div>';
                deliveryForm.style.display = "none";
            }
        })
        .catch(() => {
            patientMessage.innerHTML = '<div class="alert alert-danger">Error checking patient.</div>';
        });
    });

    motherStatusSelect.addEventListener("change", function() {
        if (motherStatusSelect.value === "Deceased") {
            deathDetails.style.display = "block";
        } else {
            deathDetails.style.display = "none";
        }
    });
});