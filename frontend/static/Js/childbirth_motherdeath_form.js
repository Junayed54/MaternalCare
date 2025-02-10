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
        document.getElementById("response-message").textContent = "✅ Childbirth record added successfully!";
        document.getElementById("response-message").classList.add("text-green-600");
    })
    .catch(error => {
        document.getElementById("response-message").textContent = "❌ Error submitting childbirth record.";
        document.getElementById("response-message").classList.add("text-red-600");
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
        document.getElementById("response-message").textContent = "✅ Mother death record added successfully!";
        document.getElementById("response-message").classList.add("text-green-600");
    })
    .catch(error => {
        document.getElementById("response-message").textContent = "❌ Error submitting mother death record.";
        document.getElementById("response-message").classList.add("text-red-600");
    });
});
