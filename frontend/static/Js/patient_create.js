document.addEventListener("DOMContentLoaded", function () {
    
    const form = document.getElementById('patient-form');
    document.getElementById("next_button").addEventListener("click", function () {
        const next_button = document.getElementById ('next_button');
        next_button.classList.add('d-none');
        const phoneNumber = document.getElementById("phone-number").value;
        const accessToken = localStorage.getItem('access_token'); // Replace with actual token

        fetch("/api/check_patient/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`,
            },
            body: JSON.stringify({ phone_number: phoneNumber }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            let full_name = document.getElementById('full-name');
            full_name.removeAttribute('disabled');
            
            if (data.exists) {
                const patient = data.patient;

                // Fetch names from API instead of using static mapping
                Promise.all([
                    fetch(`/api/get_division_name/${patient.division}/`, {
                        headers: { 'Authorization': `Bearer ${accessToken}` }
                    }).then(res => res.json()),

                    fetch(`/api/get_district_name/${patient.district}/`, {
                        headers: { 'Authorization': `Bearer ${accessToken}` }
                    }).then(res => res.json()),
                
                    fetch(`/api/get_upazilla_name/${patient.upazilla}/`, {
                        headers: { 'Authorization': `Bearer ${accessToken}` }
                    }).then(res => res.json()),
                
                    fetch(`/api/get_union_name/${patient.union}/`, {
                        headers: { 'Authorization': `Bearer ${accessToken}` }
                    }).then(res => res.json()),
                
                    fetch(`/api/get_village_name/${patient.village}/`, {
                        headers: { 'Authorization': `Bearer ${accessToken}` }
                    }).then(res => res.json())
                ])
                .then(([division, district, upazilla, union, village]) => {
                    console.log(division, district, upazilla, union, village);

                    updateSelect("division", division.id, division.name);
                    updateSelect("district", district.id, district.name);
                    updateSelect("upazila", upazilla.id, upazilla.name);
                    updateSelect("union", union.id, union.name);
                    updateSelect("village", village.id, village.name);
                })
                .catch(error => console.error("Error fetching location names:", error));
                
                // Function to update select options
                function updateSelect(selectId, value, text) {
                    let selectElement = document.getElementById(selectId);
                    selectElement.innerHTML = `<option value="${value}">${text}</option>`;
                }
                
                console.log(document.getElementById("date-of-birth"));
                // Set other patient details
                document.getElementById("phone-number").value = patient.phone_number;
                document.getElementById("full-name").value = patient.full_name;
                document.getElementById("husband-name").value = patient.husband_name;
                document.getElementById("husband-phone").value = patient.husband_phone;
                // document.getElementById("couple-no").value = patient.couple_no;
                document.getElementById("nid-number").value = patient.nid_number;
                document.getElementById('date-of-birth').value = patient.date_of_birth;
                document.getElementById("blood-group").value = patient.blood_group;
                document.getElementById("husband-blood-group").value = patient.husband_blood_group;
                document.getElementById("husband-earning").value = patient.husband_earning;

                // Show patient info section
                document.getElementById("patient-info").classList.remove("d-none");
            } else {
                document.getElementById("patient-info").classList.remove("d-none");
                alert("Patient not found!");
            }
        })
        .catch(error => console.error("Error:", error));
    });



    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(form);
        const patientImage = document.querySelector('input[type="file"]');
        const accessToken = localStorage.getItem('access_token');

        if (!accessToken) {
            alert('Unauthorized: Please log in again.');
            return;
        }

        if (patientImage.files.length > 0) {
            formData.append('image', patientImage.files[0]);
        }

        // Append additional required fields for Patient and PregnancyRecord models
        formData.append('full_name', document.getElementById('full-name').value);
        formData.append('phone_number', document.getElementById('phone-number').value);
        formData.append('husband_name', document.getElementById('husband-name').value);
        formData.append('husband_phone', document.getElementById('husband-phone').value);
        // formData.append('couple_no', document.getElementById('couple-no').value);
        formData.append('nid_number', document.getElementById('nid-number').value);
        formData.append('date_of_birth', document.getElementById('date-of-birth').value);
        formData.append('village', document.getElementById('village').value);
        // formData.append('ward_number', document.getElementById('ward-number').value);
        formData.append('union', document.getElementById('union').value);
        formData.append('upazila', document.getElementById('upazila').value);
        formData.append('district', document.getElementById('district').value);
        formData.append('division', document.getElementById('division').value);
        formData.append('blood_group', document.getElementById('blood-group').value);
        formData.append('husband_blood_group', document.getElementById('husband-blood-group').value);
        formData.append('husband_earning', document.getElementById('husband-earning').value);

        // Pregnancy record fields
        formData.append('age', document.getElementById('age').value);
        formData.append('husband_age', document.getElementById('husband-age').value);
        // formData.append('pregnancy_count', document.getElementById('pregnancy-count').value);
        formData.append('menstruation_off_duration', document.getElementById('menstruation-off-duration').value);
        formData.append('womb_count', document.getElementById('womb-count').value);
        formData.append('living_children', document.getElementById('living-children').value);
        formData.append('last_child_age', document.getElementById('last-child-age').value);
        formData.append('normal_delivery_count', document.getElementById('normal-delivery-count').value);
        formData.append('c_section_count', document.getElementById('c-section-count').value);
        formData.append('d_and_c_count', document.getElementById('d-and-c-count').value);
        formData.append('preferred_delivery_place', document.getElementById('preferred-delivery-place').value);
        formData.append('tt_dose_count', document.getElementById('tt-dose-count').value);
        formData.append('family_planning_after_delivery', document.getElementById('family-planning-after-delivery').value);
        formData.append('physical_problem', document.getElementById('physical-problem').value);
        formData.append('last_period_date', document.getElementById('last-period-date').value);
        formData.append('expected_delivery_date', document.getElementById('expected-delivery-date').value);

        fetch('/api/create_patient_and_pregnancy/', {  // Updated API endpoint
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success!',
                    text: 'Form submitted successfully!',
                    confirmButtonColor: '#3085d6',
                    confirmButtonText: 'OK'
                }).then(() => {
                    form.reset();
                    window.location.reload();
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Error submitting form. Please try again.',
                    confirmButtonColor: '#d33'
                });
            }

        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        });
    });
});



document.addEventListener("DOMContentLoaded", function() {
    const divisionSelect = document.getElementById("division");
    const districtSelect = document.getElementById("district");
    const upazilaSelect = document.getElementById("upazila");
    const unionSelect = document.getElementById("union");
    const villageSelect = document.getElementById("village");

    // Get the access token from localStorage or sessionStorage
    const accessToken = localStorage.getItem("access_token") || sessionStorage.getItem("access_token");

    function fetchData(url, selectElement) {
        fetch(url, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Unauthorized or invalid token");
            }
            return response.json();
        })
        .then(data => {
            selectElement.innerHTML = '<option value="">Select</option>';
            data.forEach(item => {
                let option = document.createElement("option");
                option.value = item.id;
                option.textContent = item.name;
                selectElement.appendChild(option);
            });
        })
        .catch(error => console.error("Error:", error));
    }

    // Fetch divisions on page load
    fetchData('/api/divisions/', divisionSelect);

    divisionSelect.addEventListener("change", function() {
        let divisionId = this.value;
        districtSelect.innerHTML = '<option value="">Select District</option>';
        upazilaSelect.innerHTML = '<option value="">Select Upazila</option>';
        unionSelect.innerHTML = '<option value="">Select Union</option>';
        villageSelect.innerHTML = '<option value="">Select Village</option>';
        
        if (divisionId) {
            fetchData(`/api/districts/${divisionId}/`, districtSelect);
        }
    });

    districtSelect.addEventListener("change", function() {
        let districtId = this.value;
        upazilaSelect.innerHTML = '<option value="">Select Upazila</option>';
        unionSelect.innerHTML = '<option value="">Select Union</option>';
        villageSelect.innerHTML = '<option value="">Select Village</option>';

        if (districtId) {
            fetchData(`/api/upazilas/${districtId}/`, upazilaSelect);
        }
    });

    upazilaSelect.addEventListener("change", function() {
        let upazilaId = this.value;
        unionSelect.innerHTML = '<option value="">Select Union</option>';
        villageSelect.innerHTML = '<option value="">Select Village</option>';

        if (upazilaId) {
            fetchData(`/api/unions/${upazilaId}/`, unionSelect);
        }
    });

    unionSelect.addEventListener("change", function() {
        let unionId = this.value;
        villageSelect.innerHTML = '<option value="">Select Village</option>';

        if (unionId) {
            fetchData(`/api/villages/${unionId}/`, villageSelect);
        }
    });
});






