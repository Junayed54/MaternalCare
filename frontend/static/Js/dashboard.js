
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



// document.addEventListener("DOMContentLoaded", function () {
//     const accessToken = localStorage.getItem('access_token');
//     const apiUrl = "/api/dashboard/statics/";

//     fetch(apiUrl, {
//         method: "GET",
//         headers: {
//             "Authorization": `Bearer ${accessToken}`,
//             "Content-Type": "application/json"
//         }
//     })
//     .then(response => {
//         if (!response.ok) throw new Error("Network response was not ok");
//         return response.json();
//     })
//     .then(data => {
//         console.log(data);

//         // Set simple stats
//         document.querySelector("#pregnant-patients").innerText = data.new_pregnant_patients_this_month;
//         document.querySelector("#total-deliveries").innerText = data.deliveries_last_month;
//         document.querySelector("#expected-births").innerText = data.expected_deliveries_next_month;
//         document.querySelector("#total-births").innerText = data.newborns_last_month;
//         document.querySelector("#underage-pregnancies").innerText = data.underage_pregnancies;
//         document.querySelector("#dsc-procedures").innerText = data.completed_dsc_last_month;

//         // Delivery type breakdown
//         let normalDeliveries = 0;
//         let cesareanDeliveries = 0;

//         data.delivery_type_breakdown.forEach(item => {
//             if (item.preferred_delivery_place.toLowerCase().includes("normal")) {
//                 normalDeliveries = item.count;
//             } else if (item.preferred_delivery_place.toLowerCase().includes("cesarean")) {
//                 cesareanDeliveries = item.count;
//             }
//         });

//         // Birth outcome breakdown
//         let liveBirths = 0;
//         let stillbirths = 0;

//         data.birth_status_breakdown.forEach(item => {
//             if (item.baby_status.toLowerCase() === "live") liveBirths = item.count;
//             if (item.baby_status.toLowerCase() === "stillbirth") stillbirths = item.count;
//         });

//         // Render charts
//         updateCharts(normalDeliveries, cesareanDeliveries, liveBirths, stillbirths);
//     })
//     .catch(error => {
//         console.error("Error fetching dashboard data:", error);
//     });

//     function updateCharts(normal, cesarean, live, stillbirth) {
//         // Delivery Type Pie Chart
//         const deliveryTypeChart = new ApexCharts(document.querySelector("#deliveryTypeChart"), {
//             series: [normal, cesarean],
//             chart: { type: 'pie', height: 300 },
//             labels: ['Normal', 'Cesarean'],
//             colors: ['#63993D', '#F5921B']
//         });
//         deliveryTypeChart.render();

//         // Birth Outcomes Donut Chart
//         const birthOutcomesChart = new ApexCharts(document.querySelector("#birthOutcomesChart"), {
//             series: [stillbirth, live],
//             chart: { type: 'donut', height: 300 },
//             labels: ['Stillbirths', 'Live Births'],
//             colors: ['#EC6B56', '#47B39C']
//         });
//         birthOutcomesChart.render();
//     }
// });




// document.addEventListener("DOMContentLoaded", function() {
//             var deliveryTypeOptions = {
//                 series: [1700, 1190], // Normal and Cesarean deliveries
//                 chart: { type: 'pie', height: 300 },
//                 labels: ['Normal', 'Cesarean'],
//                 colors: ['#63993D', '#F5921B']
//             };
//             var deliveryTypeChart = new ApexCharts(document.querySelector("#deliveryTypeChart"), deliveryTypeOptions);
//             deliveryTypeChart.render();
        
//             var birthOutcomesOptions = {
//                 series: [120, 2770], // Stillbirths and Live Births
//                 chart: { type: 'donut', height: 300 },
//                 labels: ['Stillbirths', 'Live Births'],
//                 colors: ['#EC6B56', '#47B39C']
//             };
//             var birthOutcomesChart = new ApexCharts(document.querySelector("#birthOutcomesChart"), birthOutcomesOptions);
//             birthOutcomesChart.render();
//         });
//         document.addEventListener("DOMContentLoaded", function() {
//             var pregnancyTrendOptions = {
//                 series: [{
//                     name: "Pregnancies",
//                     data: [3200, 2800, 3100, 3500, 3700, 3900] // Example data for last 6 months
//                 }],
//                 chart: {
//                     type: 'line',
//                     height: 300
//                 },
//                 xaxis: {
//                     categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], // Months
//                     title: {
//                         text: "Months"
//                     }
//                 },
//                 yaxis: {
//                     title: {
//                         text: "Number of Pregnancies"
//                     }
//                 },
//                 stroke: {
//                     curve: 'smooth'
//                 },
//                 colors: ['#008FFB']
//             };
        
//             var pregnancyTrendChart = new ApexCharts(document.querySelector("#pregnancyTrendChart"), pregnancyTrendOptions);
//             pregnancyTrendChart.render();
//         });
        

//     </script>
//     <script>
//         document.addEventListener("DOMContentLoaded", function() {
//             // API URL
//             const apiUrl = "https://your-api.com/high-risk-pregnancies";
//             const accessToken = "your_access_token_here";  // Replace with actual token
        
//             // Default Data (For Initial Load or API Failure)
//             const defaultCategories = ["Union A", "Union B", "Union C", "Union D", "Union E"];
//             const defaultValues = [12, 18, 25, 9, 15];
        
//             function renderChart(categories, values) {
//                 var highRiskPregnancyOptions = {
//                     series: [{
//                         name: "High-Risk Pregnancies",
//                         data: values
//                     }],
//                     chart: {
//                         type: 'bar',
//                         height: 300
//                     },
//                     plotOptions: {
//                         bar: {
//                             horizontal: false,
//                             columnWidth: '50%',
//                         }
//                     },
//                     xaxis: {
//                         categories: categories
//                     },
//                     colors: ['#FF4560']
//                 };
        
//                 // Render the Chart
//                 var highRiskPregnancyChart = new ApexCharts(document.querySelector("#highRiskPregnancyChart"), highRiskPregnancyOptions);
//                 highRiskPregnancyChart.render();
//             }
        
//             // Fetch Data from API
//             axios.get(apiUrl, {
//                 headers: {
//                     Authorization: `Bearer ${accessToken}`
//                 }
//             })
//             .then(response => {
//                 const data = response.data;  // Adjust according to your API response
//                 const categories = data.map(item => item.union_name);
//                 const values = data.map(item => item.count);
                
//                 // Render Chart with API Data
//                 renderChart(categories, values);
//             })
//             .catch(error => {
//                 console.error("Error fetching data:", error);
                
//                 // Render Chart with Default Data
//                 renderChart(defaultCategories, defaultValues);
//             });
//         });
//     </script>
//          {% endcomment %}
        


// static/Js/dashboard.js
document.addEventListener("DOMContentLoaded", function () {
    const accessToken = localStorage.getItem('access_token'); // or wherever you store token
    const apiUrl = "/api/dashboard-data/";  // Adjust if your API endpoint differs

    if (!accessToken) {
        console.error("No access token found");
        return;
    }

    axios.get(apiUrl, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    })
    .then(response => {
        const data = response.data;
        console.log(data);
        // Update simple stats text
        document.querySelector("#pregnant-patients").innerText = data.pregnant_patients_this_month ?? "0";
        document.querySelector("#total-deliveries").innerText = data.total_deliveries_last_month ?? "0";
        document.querySelector("#high-risk-pregnancies").innerText = data.high_risk_pregnancies ?? "0";
        document.getElementById("total-birth").innerText = data.total_births_last_month ?? "0";
        document.getElementById("expected-birth").innerText = data.expected_births_next_month;
        // Note: Your template shows hardcoded values for total births and expected births
        // If you want to update those dynamically, you'd add IDs to those elements and update similarly:
        // For example, add id="total-births" and id="expected-births" in your template and update here:
        // document.querySelector("#total-births").innerText = data.total_births_last_month ?? "0";
        // document.querySelector("#expected-births").innerText = data.expected_births_next_month ?? "0";

        // Update Delivery Type text
        const dtNormal = data.delivery_type_chart_data?.series[0] ?? 0;
        const dtCesarean = data.delivery_type_chart_data?.series[1] ?? 0;
        const deliveryTypeCard = document.querySelector(".card.custom-card .card-body > .d-flex.justify-content-between.mt-2");
        if (deliveryTypeCard) {
            deliveryTypeCard.children[0].querySelector('strong').innerText = dtNormal;
            deliveryTypeCard.children[1].querySelector('strong').innerText = dtCesarean;
        }

        // Update Birth Outcomes text
        const birthOutcomes = data.birth_outcomes_chart_data;

        const stillbirthCount = birthOutcomes.series[0];
        const livebirthCount = birthOutcomes.series[1];

        document.getElementById("stillbirth-count").textContent = stillbirthCount.toLocaleString();
        document.getElementById("livebirth-count").textContent = livebirthCount.toLocaleString();


        // Update Delivery Location text
        const locHospitalClinic = data.delivery_location_last_month?.hospital_clinic ?? 0;
        const locHome = data.delivery_location_last_month?.home ?? 0;
        const deliveryLocationCard = document.querySelector(".card.custom-card .card-body > .d-flex.justify-content-between.mt-2");
        // This is tricky since you have multiple similar containers, better to add IDs in HTML for them to select safely:
        // I'll do it by index here assuming your order matches:
        const deliveryLocationElements = document.querySelectorAll(".card.custom-card .card-body .d-flex.justify-content-between.mt-2");
        if (deliveryLocationElements.length >= 3) {
            deliveryLocationElements[2].children[0].querySelector('strong').innerText = locHospitalClinic;
            deliveryLocationElements[2].children[1].querySelector('strong').innerText = locHome;
        }

        // Monthly Pregnancies Trend Chart
        const pregnancyTrendChartEl = document.querySelector("#pregnancyTrendChart");
        if (pregnancyTrendChartEl) {
            const pregnancyTrendOptions = {
                series: [{
                    name: "Pregnancies",
                    data: data.monthly_pregnancies_trend_chart_data?.series || []
                }],
                chart: {
                    type: 'line',
                    height: 300
                },
                xaxis: {
                    categories: data.monthly_pregnancies_trend_chart_data?.labels || [],
                    title: { text: "Months" }
                },
                yaxis: {
                    title: { text: "Number of Pregnancies" }
                },
                stroke: { curve: 'smooth' },
                colors: ['#008FFB']
            };
            ApexCharts.exec('pregnancyTrendChart', 'destroy'); // Clear if already exists
            const pregnancyTrendChart = new ApexCharts(pregnancyTrendChartEl, pregnancyTrendOptions);
            pregnancyTrendChart.render();
        }

        // High-Risk Pregnancies by Union Bar Chart
        const highRiskPregnancyChartEl = document.querySelector("#highRiskPregnancyChart");
        if (highRiskPregnancyChartEl) {
            const unionCategories = data.high_risk_pregnancies_by_union_chart_data?.categories || [];
            const unionSeriesData = data.high_risk_pregnancies_by_union_chart_data?.series?.[0]?.data || [];

            const highRiskPregnancyOptions = {
                series: [{
                    name: "High-Risk Pregnancies",
                    data: unionSeriesData
                }],
                chart: {
                    type: 'bar',
                    height: 300
                },
                plotOptions: {
                    bar: { horizontal: false, columnWidth: '50%' }
                },
                xaxis: { categories: unionCategories },
                colors: ['#FF4560']
            };

            ApexCharts.exec('highRiskPregnancyChart', 'destroy');
            const highRiskPregnancyChart = new ApexCharts(highRiskPregnancyChartEl, highRiskPregnancyOptions);
            highRiskPregnancyChart.render();
        }

        // Delivery Type Pie Chart
        const deliveryTypeChartEl = document.querySelector("#deliveryTypeChart");
        if (deliveryTypeChartEl) {
            const deliveryTypeOptions = {
                series: data.delivery_type_chart_data?.series || [0,0],
                chart: { type: 'pie', height: 300 },
                labels: data.delivery_type_chart_data?.labels || ['Normal', 'Cesarean'],
                colors: ['#63993D', '#F5921B']
            };
            ApexCharts.exec('deliveryTypeChart', 'destroy');
            const deliveryTypeChart = new ApexCharts(deliveryTypeChartEl, deliveryTypeOptions);
            deliveryTypeChart.render();
        }

        // Birth Outcomes Donut Chart
        const birthOutcomesChartEl = document.querySelector("#birthOutcomesChart");
        if (birthOutcomesChartEl) {
            const birthOutcomesOptions = {
                series: data.birth_outcomes_chart_data?.series || [0,0],
                chart: { type: 'donut', height: 300 },
                labels: data.birth_outcomes_chart_data?.labels || ['Stillbirths', 'Live Births'],
                colors: ['#EC6B56', '#47B39C']
            };
            ApexCharts.exec('birthOutcomesChart', 'destroy');
            const birthOutcomesChart = new ApexCharts(birthOutcomesChartEl, birthOutcomesOptions);
            birthOutcomesChart.render();
        }

        // ANC Schedule List update
        const ancData = data.anc_schedule_last_month || {};
        const ancListItems = document.querySelectorAll(".card.custom-card ul.list-group li.list-group-item");
        ancListItems.forEach(li => {
            if (li.textContent.includes('1st ANC')) li.querySelector('span').innerText = ancData['1st ANC'] ?? 0;
            else if (li.textContent.includes('2nd ANC')) li.querySelector('span').innerText = ancData['2nd ANC'] ?? 0;
            else if (li.textContent.includes('3rd ANC')) li.querySelector('span').innerText = ancData['3rd ANC'] ?? 0;
            else if (li.textContent.includes('4th ANC')) li.querySelector('span').innerText = ancData['4th ANC'] ?? 0;
        });

        // High-Risk Pregnancies by Union List update (optional, since chart exists)
        // If you want to update the list dynamically too, you can do it here.
        // Assuming you add ids or classes to those list items for easy targeting.


        const unionList = data.high_risk_pregnancies_by_union_chart_data;
        const container = document.getElementById("high-risk-union-list");

        // Clear any existing items
        container.innerHTML = "";

        const names = unionList.categories;
        const counts = unionList.series[0].data;

        names.forEach((name, index) => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.innerHTML = `${name}: <span class="fw-semibold">${counts[index]}</span>`;
            container.appendChild(li);
        });


    })
    .catch(error => {
        console.error("Error fetching dashboard data:", error);
        // You can show some default fallback UI or error messages here if you want
    });
});
