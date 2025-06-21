document.addEventListener("DOMContentLoaded", function () {
    const accessToken = localStorage.getItem("access_token");

    // Redirect to login if no token found
    if (!accessToken) {
        window.location.href = "/login/";
        return; // stop further execution
    }

    // Fetch user role
    fetch("/api/user/role/", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json"
        }
    })
    .then(res => {
        if (!res.ok) {
            // Handle token expiry or unauthorized access
            throw new Error("Unauthorized");
        }
        return res.json();
    })
    .then(data => {
        console.log("User Role:", data.role);
        console.log(data);
        if (data.role === "UHFPO") {
            console.log("heloo");
            const uhfpo = document.getElementById('uhfpo');
            
            uhfpo.classList.remove('d-none');
            console.log(uhfpo);
        } else if (data.role === "FS") {
            
            const field_assistant = document.getElementById('field_assistant');
            if (field_assistant) field_assistant.classList.remove('d-none');
        } else if (data.role === "MIDWIFE") {
            const midwifeElements = document.querySelectorAll('.midwife');
            midwifeElements.forEach(el => {
                el.classList.remove('d-none');
            });

        }
    })
    .catch(error => {
        console.error("Error fetching user role:", error);
        // Redirect to login on failure
        window.location.href = "/login/";
    });

    // Logout button event
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function () {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            window.location.href = "/login/";
        });
    }
});
