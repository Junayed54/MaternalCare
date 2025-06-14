
// document.addEventListener("DOMContentLoaded", function() {
//     const accessToken = localStorage.getItem('access_token');  // Replace with actual token
//     const apiUrl = "/api/statistics/";  // Replace with actual API URL

//     axios.get(apiUrl, {
//         headers: {
//             Authorization: `Bearer ${accessToken}`
//         }
//     })
//     .then(response => {
//         const data = response.data;

//         // Example: Updating the number of pregnant patients this month
//         document.querySelector("#pregnant-patients").innerText = data.pregnant_patients;
//         document.querySelector("#total-deliveries").innerText = data.total_deliveries;
//         document.querySelector("#high-risk-pregnancies").innerText = data.high_risk_pregnancies;
//         document.querySelector("#total-births").innerText = data.total_births;
//         document.querySelector("#expected-births").innerText = data.expected_births;

//         // Update chart data dynamically
//         updateCharts(data);
//     })
//     .catch(error => {
//         console.error("Error fetching data:", error);
//     });

//     function updateCharts(data) {
//         var deliveryTypeOptions = {
//             series: [data.normal_deliveries, data.cesarean_deliveries],
//             chart: { type: 'pie', height: 300 },
//             labels: ['Normal', 'Cesarean'],
//             colors: ['#63993D', '#F5921B']
//         };
//         var deliveryTypeChart = new ApexCharts(document.querySelector("#deliveryTypeChart"), deliveryTypeOptions);
//         deliveryTypeChart.render();

//         var birthOutcomesOptions = {
//             series: [data.stillbirths, data.live_births],
//             chart: { type: 'donut', height: 300 },
//             labels: ['Stillbirths', 'Live Births'],
//             colors: ['#EC6B56', '#47B39C']
//         };
//         var birthOutcomesChart = new ApexCharts(document.querySelector("#birthOutcomesChart"), birthOutcomesOptions);
//         birthOutcomesChart.render();
//     }
// });



document.addEventListener("DOMContentLoaded", function () {
    const accessToken = localStorage.getItem('access_token');
    const apiUrl = "/api/statistics/";

    axios.get(apiUrl, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    })
    .then(response => {
        const data = response.data;

        // Set simple stats
        document.querySelector("#pregnant-patients").innerText = data.new_pregnant_patients_this_month;
        document.querySelector("#total-deliveries").innerText = data.deliveries_last_month;
        document.querySelector("#expected-births").innerText = data.expected_deliveries_next_month;
        document.querySelector("#total-births").innerText = data.newborns_last_month;
        document.querySelector("#underage-pregnancies").innerText = data.underage_pregnancies;
        document.querySelector("#dsc-procedures").innerText = data.completed_dsc_last_month;

        // Parse delivery type breakdown (Normal / Cesarean)
        let normalDeliveries = 0;
        let cesareanDeliveries = 0;
        data.delivery_type_breakdown.forEach(item => {
            if (item.preferred_delivery_place.toLowerCase().includes("normal")) {
                normalDeliveries = item.count;
            } else if (item.preferred_delivery_place.toLowerCase().includes("cesarean")) {
                cesareanDeliveries = item.count;
            }
        });

        // Parse birth outcome breakdown (Live / Stillbirth)
        let liveBirths = 0;
        let stillbirths = 0;
        data.birth_status_breakdown.forEach(item => {
            if (item.baby_status === "live") liveBirths = item.count;
            if (item.baby_status === "stillbirth") stillbirths = item.count;
        });

        // Update chart
        updateCharts(normalDeliveries, cesareanDeliveries, liveBirths, stillbirths);
    })
    .catch(error => {
        console.error("Error fetching dashboard data:", error);
    });

    function updateCharts(normal, cesarean, live, stillbirth) {
        // Delivery type pie
        const deliveryTypeChart = new ApexCharts(document.querySelector("#deliveryTypeChart"), {
            series: [normal, cesarean],
            chart: { type: 'pie', height: 300 },
            labels: ['Normal', 'Cesarean'],
            colors: ['#63993D', '#F5921B']
        });
        deliveryTypeChart.render();

        // Birth outcome donut
        const birthOutcomesChart = new ApexCharts(document.querySelector("#birthOutcomesChart"), {
            series: [stillbirth, live],
            chart: { type: 'donut', height: 300 },
            labels: ['Stillbirths', 'Live Births'],
            colors: ['#EC6B56', '#47B39C']
        });
        birthOutcomesChart.render();
    }
});
