// document.addEventListener("DOMContentLoaded", function () {
//     document.getElementById("login-btn").addEventListener("click", login);
// });

// function login() {
//     let phone_number = document.getElementById("phone_number").value.trim();
//     let password = document.getElementById("password").value.trim();
    
//     let errorMessage = document.getElementById("error-message");
//     errorMessage.innerText = "";

//     fetch("/api/login/", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({ phone_number, password })
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error("Invalid credentials");
//         }
//         return response.json();
//     })
//     .then(data => {
//         if (data.access) {
//             console.log(data.access);
//             localStorage.setItem("access_token", data.access);
//             localStorage.setItem("refresh_token", data.refresh);
//             window.location.href = "/";
//         } else {
//             errorMessage.innerText = "Invalid credentials!";
//         }
//     })
//     .catch(error => {
//         errorMessage.innerText = "Error logging in. Try again later.";
//         console.error("Login error:", error);
//     });
// }



document.addEventListener("DOMContentLoaded", function () {
    // Get a reference to the form element
    const loginForm = document.querySelector('form'); // Or give your form an ID and use getElementById

    // Add an event listener to the form's 'submit' event
    // The event object is passed to the function
    loginForm.addEventListener("submit", function(event) {
        event.preventDefault(); // <--- THIS IS CRUCIAL: Prevents the default form submission

        login(); // Call your existing login function
    });

    // You no longer need this if you attach to form submit
    // document.getElementById("login-btn").addEventListener("click", login); 
    // However, if you want the click on the button to *only* trigger the JS
    // and rely on the form submit handler to prevent default, it's fine to leave.
    // If your form has other buttons, attaching to the form submit is cleaner.
});

// Your existing login function
function login() {
    let phone_number = document.getElementById("phone_number").value.trim();
    let password = document.getElementById("password").value.trim();
    
    let errorMessage = document.getElementById("error-message");
    errorMessage.innerText = "";

    fetch("/api/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            // If you're using Django's CSRF protection, you'll need to include the CSRF token:
            // "X-CSRFToken": getCookie("csrftoken") 
        },
        body: JSON.stringify({ phone_number, password })
    })
    .then(response => {
        if (!response.ok) {
            // Check for specific status codes if needed for more detailed error messages
            if (response.status === 400 || response.status === 401) {
                return response.json().then(err => { throw new Error(err.detail || "Invalid credentials"); });
            }
            throw new Error("Network response was not ok.");
        }
        return response.json();
    })
    .then(data => {
        if (data.access) {
            console.log(data.access);
            localStorage.setItem("access_token", data.access);
            localStorage.setItem("refresh_token", data.refresh);
            window.location.href = "/"; // Redirect on successful login
        } else {
            errorMessage.innerText = "Invalid credentials!"; // Fallback if API returns 200 but no access token
        }
    })
    .catch(error => {
        errorMessage.innerText = error.message || "Error logging in. Try again later.";
        console.error("Login error:", error);
    });
}

// Helper function to get CSRF token (if needed for Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add the password visibility toggle (from your HTML, assuming it's in the same JS file or linked)
document.addEventListener("DOMContentLoaded", function() {
    const passwordToggleButton = document.getElementById("button-addon2");
    if (passwordToggleButton) {
        passwordToggleButton.addEventListener("click", function() {
            const passwordField = document.getElementById("password");
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.querySelector('i').classList.toggle('ri-eye-off-line');
            this.querySelector('i').classList.toggle('ri-eye-line');
        });
    }
});