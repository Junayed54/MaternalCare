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
  <div class="card shadow-sm p-4 mb-4">
    <div class="row mb-3">
      <div class="col-md-6 mb-2 mb-md-0">
        <strong>Checked By:</strong> <span class="text-primary">${report.checked_by_name || "N/A"}</span>
      </div>
      <div class="col-md-6">
        <strong>Hospital:</strong> <span class="text-primary">${report.hospital_name || "N/A"}</span>
      </div>
    </div>

    <!-- Patient Info -->
    <h5 class="mt-4 mb-3 text-secondary fw-bold">
      <i class="bi bi-person-circle me-2"></i>Patient Information
    </h5>
    <hr>
    <div class="row g-3">
      <div class="col-12 col-md-4"><strong>Name:</strong> ${patient.full_name}</div>
      <div class="col-12 col-md-4"><strong>Phone Number:</strong> ${patient.phone_number}</div>
      <div class="col-12 col-md-4"><strong>Blood Group:</strong> ${patient.blood_group || "N/A"}</div>
      <div class="col-12 col-md-4"><strong>Husband's Name:</strong> ${patient.husband_name || "N/A"}</div>
      <div class="col-12 col-md-4"><strong>Husband's Blood Group:</strong> ${patient.husband_blood_group || "N/A"}</div>
      <div class="col-12 col-md-4"><strong>Husband's Phone:</strong> ${patient.husband_phone || "N/A"}</div>
    </div>

    <h5 class="mt-5 mb-3 text-secondary fw-bold">
      <i class="bi bi-heart-pulse me-2"></i>Vitals & Health Check
    </h5>
    <hr>
    <div class="row g-3">
      <div class="col-12 col-md-4"><strong>Blood Pressure:</strong> ${report.bp}</div>
      <div class="col-12 col-md-4"><strong>RBS:</strong> ${report.rbs} mg/dL</div>
      <div class="col-12 col-md-4"><strong>Pulse:</strong> ${report.pulse} BPM</div>
    </div>

    <h5 class="mt-5 mb-3 text-secondary fw-bold">
      <i class="bi bi-activity me-2"></i>Health Conditions
    </h5>
    <hr>
    <div class="row g-3">
    ${[
        { label: "IFA Supplemented", val: report.ifa },
        { label: "Diabetes", val: report.diabetes },
        { label: "Thyroid Disease", val: report.thyroid_disease },
        { label: "Heart Disease", val: report.heart_disease },
        { label: "Bronchial Asthma", val: report.bronchial_asthma },
        { label: "Kidney Disease", val: report.kidney_disease },
        { label: "Epilepsy", val: report.epilepsy },
    ].map(cond => `
        <div class="col-6 col-md-4">
        <span class="badge ${cond.val ? "bg-danger" : "bg-success"}">
            ${cond.val ? "⚠️" : "✔️"} ${cond.label}
        </span>
        </div>
    `).join('')}
    </div>

    <h5 class="mt-5 mb-3 text-secondary fw-bold">
      <i class="bi bi-geo-alt-fill me-2"></i>Placenta Location
    </h5>
    <p class="fw-semibold fs-5">${report.placenta_location.toUpperCase() || "N/A"}</p>

    <h5 class="mt-5 mb-3 text-secondary fw-bold">
      <i class="bi bi-journal-medical me-2"></i>Medical History
    </h5>
    <div class="row g-3">
    ${[
        { label: "History of Intrauterine Death", val: report.history_iud },
        { label: "History of Stillbirth", val: report.history_stillbirth },
        { label: "History of Preclampsia", val: report.history_preclampsia },
        { label: "History of Eclampsia", val: report.history_eclampsia },
    ].map(hist => `
        <div class="col-6 col-md-3">
        <span class="badge ${hist.val ? "bg-danger" : "bg-success"}">
            ${hist.val ? "⚠️" : "✔️"} ${hist.label}
        </span>
        </div>
    `).join('')}
    </div>


    ${report.additional_notes ? `
      <h5 class="mt-5 mb-3 text-secondary fw-bold">
        <i class="bi bi-pencil-square me-2"></i>Additional Notes
      </h5>
      <p class="fst-italic">${report.additional_notes}</p>
    ` : ""}

    <div class="text-muted mt-5 fs-7 text-center d-flex justify-content-between">
      <small>Report Created: ${new Date(report.created_at).toLocaleString()}</small><br>
      <small>Last Updated: ${new Date(report.updated_at).toLocaleString()}</small>
    </div>
  </div>
`;

    })
    .catch(error => {
        reportContainer.innerHTML = `<p class="text-danger">Error fetching report: ${error.response?.data?.error || "Unknown error"}</p>`;
    });
});





