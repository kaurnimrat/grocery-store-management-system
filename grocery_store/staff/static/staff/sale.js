// SIDEBAR TOGGLE
var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
    if (!sidebarOpen) {
        sidebar.classList.add("sidebar-responsive");
        sidebarOpen = true;
    }
}

function closeSidebar() {
    if (sidebarOpen) {
        sidebar.classList.remove("sidebar-responsive");
        sidebarOpen = false;
    }
}

// --------- CHARTS ----------
document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/sale-data/")
        .then(response => response.json())
        .then(data => {
            const topProducts = data.top_products;
            const salesData = data.sales_data;

            // BAR CHART - Top Products
            var barChartOptions = {
                series: [{
                    data: topProducts.map(p => p.quantity)
                }],
                chart: {
                    type: 'bar',
                    height: 350
                },
                plotOptions: {
                    bar: {
                        borderRadius: 4,
                        horizontal: true,
                    }
                },
                dataLabels: {
                    enabled: false
                },
                xaxis: {
                    categories: topProducts.map(p => p.name),
                    labels: {
                        style: {
                            colors: "#fff",
                            fontSize: "14px",
                        }
                    }
                }
            };

            var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
            barChart.render();

            // AREA CHART - Sales
            var areaChartOptions = {
                series: [{
                    name: 'Sales',
                    data: salesData.sales
                }],
                chart: {
                    height: 350,
                    type: 'area',
                },
                stroke: {
                    curve: 'smooth'
                },
                fill: {
                    type: 'solid',
                    opacity: 0.6,
                },
                labels: salesData.dates,
                markers: {
                    size: 5
                },
                yaxis: {
                    labels: {
                        style: {
                            colors: "#fff",
                            fontSize: "14px",
                        }
                    }
                },
                xaxis: {
                    labels: {
                        style: {
                            colors: "#fff",
                            fontSize: "14px",
                        }
                    }
                },
                tooltip: {
                    shared: true,
                    intersect: false
                }
            };

            var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
            areaChart.render();
        })
        .catch(error => {
            console.error("Error loading sale data:", error);
        });
});
