document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("login-btn").addEventListener("click", login);
});

function login() {
    let phone_number = document.getElementById("phone_number").value.trim();
    let password = document.getElementById("password").value.trim();
    
    let errorMessage = document.getElementById("error-message");
    errorMessage.innerText = "";

    fetch("/api/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ phone_number, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Invalid credentials");
        }
        return response.json();
    })
    .then(data => {
        if (data.access) {
            console.log(data.access);
            localStorage.setItem("access_token", data.access);
            localStorage.setItem("refresh_token", data.refresh);
            window.location.href = "/";
        } else {
            errorMessage.innerText = "Invalid credentials!";
        }
    })
    .catch(error => {
        errorMessage.innerText = "Error logging in. Try again later.";
        console.error("Login error:", error);
    });
}
