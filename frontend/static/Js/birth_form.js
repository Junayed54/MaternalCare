document.addEventListener("DOMContentLoaded", function () {
    const checkPatientBtn = document.getElementById("searchPatientBtn");
    const patientPhoneInput = document.getElementById("patient_phone");
    const patientIdInput = document.getElementById("patient_id");
    const deliveryForm = document.getElementById("delivery-form");
    const motherStatusSelect = document.getElementById("mother_status");
    const deathDetails = document.getElementById("deathDetails");
    const submitDeliveryBtn = document.getElementById("submitDelivery");

    // Step 1: Check patient existence by phone
    checkPatientBtn.addEventListener("click", function () {
        const phone = patientPhoneInput.value.trim();
        const accessToken = localStorage.getItem("access_token");

        if (!phone) {
            Swal.fire("Warning", "Please enter a phone number.", "warning");
            return;
        }

        fetch(`/api/check_patient/`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ phone_number: phone })
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                Swal.fire("✅ Success", "Patient found.", "success");
                patientIdInput.value = data.patient_id;
                deliveryForm.style.display = "block";
            } else {
                Swal.fire("⚠️ Not Found", "Patient not found.", "warning");
                deliveryForm.style.display = "none";
            }
        })
        .catch(() => {
            Swal.fire("❌ Error", "Failed to fetch patient data.", "error");
        });
    });

    // Step 2: Show death details if mother is deceased
    motherStatusSelect.addEventListener("change", function () {
        deathDetails.style.display = (this.value === "Deceased") ? "block" : "none";
    });

    // Step 3: Submit the delivery form
    submitDeliveryBtn.addEventListener("click", function (e) {
        e.preventDefault();
        const accessToken = localStorage.getItem("access_token");
        const formData = new FormData(deliveryForm);
        formData.append('phone_number', document.getElementById('patient_phone').value);
        fetch("/api/delivery-record/create/", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            },
            body: formData,
        })
        .then(response => {
            if (response.ok) return response.json();
            throw new Error("Failed");
        })
        .then(data => {
            Swal.fire("✅ Success", "Delivery record submitted successfully!", "success");
            deliveryForm.reset();
            deliveryForm.style.display = "none";
        })
        .catch(() => {
            Swal.fire("❌ Error", "Failed to submit delivery record.", "error");
        });
    });
});