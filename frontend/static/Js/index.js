document.addEventListener("DOMContentLoaded", function () {
    const accessToken = localStorage.getItem("access_token");
    
    if (!accessToken) {
        window.location.href = "/login/";
    }

    document.getElementById("logout-btn").addEventListener("click", function () {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "login.html";
    });
});