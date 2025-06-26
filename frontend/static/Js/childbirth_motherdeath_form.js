function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            const trimmed = cookie.trim();
            if (trimmed.startsWith('csrftoken=')) {
                cookieValue = trimmed.split('=')[1];
            }
        });
    }
    return cookieValue;
}

// Childbirth Form Submission
document.getElementById("childbirth-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    fetch("/api/childbirth/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            patient: document.getElementById("child_patient").value,
            full_name: document.getElementById("child_name").value,
            date_of_birth: document.getElementById("child_dob").value,
            gender: document.getElementById("child_gender").value,
            status: document.getElementById("child_status").value
        })
    })
    .then(response => response.json())
    .then(data => {
        Swal.fire({
            icon: 'success',
            title: 'Success!',
            text: 'Childbirth record added successfully!',
            confirmButtonColor: '#3085d6'
        });
    })
    .catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'Submission Failed',
            text: 'Error submitting childbirth record.',
            confirmButtonColor: '#d33'
        });
    });

});

// Mother Death Form Submission
document.getElementById("motherdeath-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    fetch("/api/motherdeath/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            patient: document.getElementById("mother_patient").value,
            date_of_death: document.getElementById("mother_dod").value,
            cause_of_death: document.getElementById("mother_cause").value
        })
    })
    .then(response => response.json())
    .then(data => {
        Swal.fire({
            icon: 'success',
            title: 'Success!',
            text: 'Mother record added successfully!',
            confirmButtonColor: '#3085d6'
        });

        // Optional inline message
        const msg = document.getElementById("response-message");
        msg.textContent = "✅ Mother record added successfully!";
        msg.className = "text-green-600 font-semibold mt-2";
    })
    .catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'Error!',
            text: 'Error submitting mother record.',
            confirmButtonColor: '#d33'
        });

        const msg = document.getElementById("response-message");
        msg.textContent = "❌ Error submitting mother record.";
        msg.className = "text-red-600 font-semibold mt-2";
    });

});
