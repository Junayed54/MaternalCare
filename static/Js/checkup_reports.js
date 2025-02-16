// document.addEventListener("DOMContentLoaded", function () {
//     const checkPatientButton = document.getElementById("check-patient-btn");
//     const phoneInput = document.getElementById("phone_number");
//     const patientInfoDiv = document.getElementById("patient-info");
//     const checkupForm = document.getElementById("checkup-report-form");
//     const selected_anc = document.getElementById('selected-anc-info');
//     let selectedAncId = null; // Store selected ANC ID

//     // Fetch patient info when clicking "Check Patient"
//     checkPatientButton.addEventListener("click", function () {
//         const phoneNumber = phoneInput.value.trim();
//         const accessToken = localStorage.getItem("access_token");

//         if (!phoneNumber) {
//             alert("Please enter a phone number.");
//             return;
//         }

//         if (!accessToken) {
//             alert("Access token is missing. Please log in.");
//             return;
//         }

//         fetch("/api/check_patient/", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//                 "Authorization": `Bearer ${accessToken}`
//             },
//             body: JSON.stringify({ phone_number: phoneNumber })
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);

//             if (data.exists && data.patient) {
//                 patientInfoDiv.classList.remove("d-none");
//                 const patient = data.patient;
//                 const patientImage = patient.image 
//                     ? `<img src="${patient.image}" alt="Patient Image" class="rounded-circle img-fluid border border-secondary mb-3" style="width: 100px; height: 100px;">`
//                     : `<div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center text-white" style="width: 100px; height: 100px;">No Image</div>`;

//                 // Generate ANC Schedule List
//                 let ancScheduleHTML = `<h5 class="mb-3">ANC Schedules</h5>`;
//                 if (patient.anc_schedules && patient.anc_schedules.length > 0) {
//                     ancScheduleHTML += `<ul class="list-group">`;
//                     patient.anc_schedules.forEach(schedule => {
//                         let statusBadge = "secondary";
//                         let actionButton = "";

//                         if (schedule.status === "Scheduled") {
//                             statusBadge = "warning";
//                             actionButton = `<button class="btn btn-primary btn-sm create-checkup" 
//                                                 data-id="${schedule.id}" 
//                                                 data-anc-id="${schedule.id}"
//                                                 data-date="${schedule.anc_date}">
//                                             Create Checkup
//                                         </button>`;
//                         }
//                         if (schedule.status === "Completed") {
//                             statusBadge = "success";
//                             actionButton = `<a href="/show-report/${schedule.id}" class="btn btn-success btn-sm">Show Report</a>`;
//                         }
//                         if (schedule.status === "Missed") {
//                             statusBadge = "danger";
//                             actionButton = ""; // No button for missed checkups
//                         }

//                         ancScheduleHTML += `
//                             <li class="list-group-item d-flex justify-content-between align-items-center">
//                                 <strong>${schedule.anc_date || "No Date"}</strong>
//                                 <span class="badge bg-${statusBadge}">${schedule.status}</span>
//                                 ${actionButton}
//                             </li>`;
//                     });
//                     ancScheduleHTML += `</ul>`;
//                 } else {
//                     ancScheduleHTML += `<p class="text-muted">No ANC schedules found.</p>`;
//                 }

//                 // Render Patient Info + ANC Schedule
//                 patientInfoDiv.innerHTML = `
//                     <div class="row bg-light shadow-sm rounded p-4">
//                         <div class="col-md-6 text-center">
//                             ${patientImage}
//                             <h4 class="fw-bold">${patient.full_name || "N/A"}</h4>
//                             <p class="text-muted">Phone: ${patient.phone_number || "N/A"}</p>
//                         </div>
//                         <div class="col-md-6 border-start ps-4">
//                             ${ancScheduleHTML}
//                         </div>
//                     </div>
//                 `;
//             } else {
//                 checkupForm.classList.add("d-none");
                
//                 selected_anc.classList.add("d-none");
//                 patientInfoDiv.innerHTML = `<p class="text-danger text-center mt-2">No patient found with this phone number.</p>`;
//                 patientInfoDiv.classList.remove("d-none");
//             }
//         })
//         .catch(error => {
//             console.error("Error fetching patient data:", error);
//             patientInfoDiv.innerHTML = `<p class="text-danger">Failed to fetch patient details.</p>`;
//         });
//     });

//     // Handle "Create Checkup" button clicks (Event Delegation)
//     document.body.addEventListener("click", function (event) {
//         if (event.target.classList.contains("create-checkup")) {
//             selectedAncId = event.target.getAttribute("data-id");
//             const selectedANCDate = event.target.getAttribute("data-date");

//             // Display selected ANC info
//             const selectedANCInfoDiv = document.getElementById("selected-anc-info");
//             selectedANCInfoDiv.innerHTML = `<p class="text-primary fw-bold">Selected ANC: ${selectedANCDate}</p>`;
//             selectedANCInfoDiv.classList.remove("d-none");

//             checkupForm.classList.remove("d-none"); // Show checkup form
//         }
//     });

//     // Handle form submission
//     checkupForm.addEventListener("submit", function (event) {
//         event.preventDefault();
//         let formData = new FormData(this);
//         formData.append("anc_id", selectedAncId);

//         fetch("/submit-checkup/", { method: "POST", body: formData })
//         .then(response => response.json())
//         .then(data => {
//             alert(data.success ? "Checkup report submitted!" : "Error submitting checkup report.");
//             location.reload();
//         });
//     });
// });



document.addEventListener("DOMContentLoaded", function () {
    const checkPatientButton = document.getElementById("check-patient-btn");
    const phoneInput = document.getElementById("phone_number");
    const patientInfoDiv = document.getElementById("patient-info");
    const checkupForm = document.getElementById("checkup-report-form");
    const selected_anc = document.getElementById('selected-anc-info');
    let selectedAncId = null; // Store selected ANC ID
    let patientPhone = null; // Store patient phone number

    // Fetch patient info when clicking "Check Patient"
    checkPatientButton.addEventListener("click", function () {
        const phoneNumber = phoneInput.value.trim();
        const accessToken = localStorage.getItem("access_token");

        if (!phoneNumber) {
            alert("Please enter a phone number.");
            return;
        }

        if (!accessToken) {
            alert("Access token is missing. Please log in.");
            return;
        }

        fetch("/api/check_patient/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },
            body: JSON.stringify({ phone_number: phoneNumber })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);

            if (data.exists && data.patient) {
                patientPhone = phoneNumber; // Store patient phone
                patientInfoDiv.classList.remove("d-none");
                const patient = data.patient;
                const patientImage = patient.image 
                    ? `<img src="${patient.image}" alt="Patient Image" class="rounded-circle img-fluid border border-secondary mb-3" style="width: 100px; height: 100px;">`
                    : `<div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center text-white" style="width: 100px; height: 100px;">No Image</div>`;

                // Generate ANC Schedule List
                let ancScheduleHTML = `<h5 class="mb-3">ANC Schedules</h5>`;
                if (patient.anc_schedules && patient.anc_schedules.length > 0) {
                    ancScheduleHTML += `<ul class="list-group">`;
                    patient.anc_schedules.forEach(schedule => {
                        let statusBadge = "secondary";
                        let actionButton = "";

                        if (schedule.status === "Scheduled") {
                            statusBadge = "warning";
                            actionButton = `<button class="btn btn-primary btn-sm create-checkup" 
                                                data-id="${schedule.id}" 
                                                data-anc-id="${schedule.id}"
                                                data-date="${schedule.anc_date}">
                                            Create Checkup
                                        </button>`;
                        }
                        if (schedule.status === "Completed") {
                            statusBadge = "success";
                            actionButton = `<a href="/show_report/${schedule.id}" class="btn btn-success btn-sm">Show Report</a>`;
                        }
                        if (schedule.status === "Missed") {
                            statusBadge = "danger";
                            actionButton = ""; // No button for missed checkups
                        }

                        ancScheduleHTML += `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <strong>${schedule.anc_date || "No Date"}</strong>
                                <span class="badge bg-${statusBadge}">${schedule.status}</span>
                                ${actionButton}
                            </li>`;
                    });
                    ancScheduleHTML += `</ul>`;
                } else {
                    ancScheduleHTML += `<p class="text-muted">No ANC schedules found.</p>`;
                }

                // Render Patient Info + ANC Schedule
                patientInfoDiv.innerHTML = `
                    <div class="row bg-light shadow-sm rounded p-4">
                        <div class="col-md-6 text-center">
                            ${patientImage}
                            <h4 class="fw-bold">${patient.full_name || "N/A"}</h4>
                            <p class="text-muted">Phone: ${patient.phone_number || "N/A"}</p>
                        </div>
                        <div class="col-md-6 border-start ps-4">
                            ${ancScheduleHTML}
                        </div>
                    </div>
                `;
            } else {
                checkupForm.classList.add("d-none");
                selected_anc.classList.add("d-none");
                patientInfoDiv.innerHTML = `<p class="text-danger text-center mt-2">No patient found with this phone number.</p>`;
                patientInfoDiv.classList.remove("d-none");
            }
        })
        .catch(error => {
            console.error("Error fetching patient data:", error);
            patientInfoDiv.innerHTML = `<p class="text-danger">Failed to fetch patient details.</p>`;
        });
    });

    // Handle "Create Checkup" button clicks (Event Delegation)
    document.body.addEventListener("click", function (event) {
        if (event.target.classList.contains("create-checkup")) {
            selectedAncId = event.target.getAttribute("data-id");
            const selectedANCDate = event.target.getAttribute("data-date");

            // Display selected ANC info
            const selectedANCInfoDiv = document.getElementById("selected-anc-info");
            selectedANCInfoDiv.innerHTML = `<p class="text-primary fw-bold">Selected ANC: ${selectedANCDate}</p>`;
            selectedANCInfoDiv.classList.remove("d-none");

            checkupForm.classList.remove("d-none"); // Show checkup form
        }
    });

    // Handle form submission
    checkupForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const accessToken = localStorage.getItem("access_token");
        if (!accessToken) {
            alert("Access token is missing. Please log in.");
            return;
        }

        // Convert form data to JSON
        const formData = new FormData(this);
        console.log(selectedAncId)
        const jsonData = {
            patient_phone: patientPhone, // Use stored phone number
            anc: selectedAncId, // ANC ID
            bp: formData.get("bp"),
            anc_checkup_number:formData.get("anc_checkup_number"),
            rbs: formData.get("rbs"),
            pulse: formData.get("pulse"),
            ifa: formData.get("ifa") === "on", // Convert checkbox value
            diabetes: formData.get("diabetes") === "on",
            thyroid_disease: formData.get("thyroid_disease") === "on",
            heart_disease: formData.get("heart_disease") === "on",
            bronchial_asthma: formData.get("bronchial_asthma") === "on",
            kidney_disease: formData.get("kidney_disease") === "on",
            epilepsy: formData.get("epilepsy") === "on",
            placenta_location: formData.get("placenta_location"),
            history_iud: formData.get("history_iud") === "on",
            history_stillbirth: formData.get("history_stillbirth") === "on",
            history_preclampsia: formData.get("history_preclampsia") === "on",
            history_eclampsia: formData.get("history_eclampsia") === "on",
            additional_notes: formData.get("additional_notes")
        };

        fetch("/api/cre-checkup-report/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.success ? "Checkup report submitted!" : "Error submitting checkup report.");
            location.reload();
        })
        .catch(error => {
            console.log("Error submitting checkup report:", error);
            alert("Error submitting checkup report.");
        });
    });
});
