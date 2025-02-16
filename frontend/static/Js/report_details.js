document.addEventListener("DOMContentLoaded", function () {
    const reportContainer = document.querySelector(".card-body");
    const accessToken = localStorage.getItem("access_token"); // Retrieve JWT token from local storage

    if (!accessToken) {
        reportContainer.innerHTML = "<p class='text-danger'>Access Token is missing. Please login again.</p>";
        return;
    }

    const pathParts = window.location.pathname.split("/");
    const ancId = pathParts[pathParts.length - 2];

    if (!ancId || isNaN(ancId)) {
        reportContainer.innerHTML = "<p class='text-danger'>Invalid Checkup Report ID!</p>";
        return;
    }

    // Fetch Checkup Report Data (using POST request)
    axios.post("/api/show-report/", { id: ancId }, {
        headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        const report = response.data;
        const patient = report.patient;  // Extract the patient info
        console.log(report)
        document.querySelector(".card-header h4").innerText = `Checkup Report - ${patient.full_name}`;
        document.querySelector(".badge.bg-info").innerText = report.anc_checkup_number_display || "N/A";

        reportContainer.innerHTML = `
            <div class="row mb-3">
                <div class="col-md-6"><strong>Checked By:</strong> ${report.checked_by_name || "N/A"}</div>
                <div class="col-md-6"><strong>Hospital:</strong> ${report.hospital_name}</div>
            </div>

            <!-- Patient Info -->
            <h5 class="mt-4">👩‍⚕️ Patient Information</h5>
            <hr>
            <div class="row">
                <div class="col-md-4"><strong>Name:</strong> ${patient.full_name}</div>
                <div class="col-md-4"><strong>Phone Number:</strong> ${patient.phone_number}</div>
                <div class="col-md-4"><strong>Blood Group:</strong> ${patient.blood_group}</div>
                <div class="col-md-4"><strong>Husband's Name:</strong> ${patient.husband_name || "N/A"}</div>
                <div class="col-md-4"><strong>Husband's Blood Group:</strong> ${patient.husband_blood_group || "N/A"}</div>
                <div class="col-md-4"><strong>Husband's Phone:</strong> ${patient.husband_phone || "N/A"}</div>
            </div>

            <h5 class="mt-4">🩺 Vitals & Health Check</h5>
            <hr>
            <div class="row">
                <div class="col-md-4"><strong>Blood Pressure:</strong> ${report.bp}</div>
                <div class="col-md-4"><strong>RBS:</strong> ${report.rbs} mg/dL</div>
                <div class="col-md-4"><strong>Pulse:</strong> ${report.pulse} BPM</div>
            </div>

            <h5 class="mt-4">🧬 Health Conditions</h5>
            <hr>
            <div class="row">
                <div class="col-md-4">${report.ifa ? "✅ IFA Supplemented" : "❌ No IFA"}</div>
                <div class="col-md-4">${report.diabetes ? "✅ Diabetes" : "❌ No Diabetes"}</div>
                <div class="col-md-4">${report.thyroid_disease ? "✅ Thyroid Disease" : "❌ No Thyroid Issues"}</div>
                <div class="col-md-4">${report.heart_disease ? "✅ Heart Disease" : "❌ No Heart Disease"}</div>
                <div class="col-md-4">${report.bronchial_asthma ? "✅ Bronchial Asthma" : "❌ No Bronchial Asthma"}</div>
                <div class="col-md-4">${report.kidney_disease ? "✅ Kidney Disease" : "❌ No Kidney Disease"}</div>
                <div class="col-md-4">${report.epilepsy ? "✅ Epilepsy" : "❌ No Epilepsy"}</div>
            </div>

            <h5 class="mt-4">📍 Placenta Location</h5>
            <p class="fw-bold">${report.placenta_location}</p>

            <h5 class="mt-4">📝 Medical History</h5>
            <div class="row">
                <div class="col-md-4">${report.history_iud ? "✅ History of Intrauterine Death" : "❌ No History of IUD"}</div>
                <div class="col-md-4">${report.history_stillbirth ? "✅ History of Stillbirth" : "❌ No History of Stillbirth"}</div>
                <div class="col-md-4">${report.history_preclampsia ? "✅ History of Preclampsia" : "❌ No History of Preclampsia"}</div>
                <div class="col-md-4">${report.history_eclampsia ? "✅ History of Eclampsia" : "❌ No History of Eclampsia"}</div>
            </div>

            ${report.additional_notes ? `<h5 class="mt-4">🗒️ Additional Notes</h5><p>${report.additional_notes}</p>` : ""}
            
            <div class="text-muted mt-4">
                <small>Report Created: ${new Date(report.created_at).toLocaleString()}</small><br>
                <small>Last Updated: ${new Date(report.updated_at).toLocaleString()}</small>
            </div>
        `;
    })
    .catch(error => {
        reportContainer.innerHTML = `<p class="text-danger">Error fetching report: ${error.response?.data?.error || "Unknown error"}</p>`;
    });
});





