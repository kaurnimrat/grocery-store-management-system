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
const topProductsData = JSON.parse(document.getElementById('top-products-data').textContent);
const salesData = JSON.parse(document.getElementById('sales-data').textContent);
console.print(topProductsData)

// --------- CHARTS ----------

document.addEventListener("DOMContentLoaded", function () {
    // Get data from Django template


    // BAR CHART - Top Products
    var barChartOptions = {
        series: [{
            data: topProductsData.map(p => p.quantity)
        }],
        chart: {
            type: 'bar',
            height: 350
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                borderRadiusApplication: 'end',
                horizontal: true,
            }
        },
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories: topProductsData.map(p => p.name),
        }
    };

    var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
    barChart.render();

    // AREA CHART - Orders
    var areaChartOptions = {
        series: [
            {
                name: 'Sales',
                type: 'area',
                data: salesData.sales
            },
            {
                name: 'Purchases',
                type: 'line',
                data: salesData.purchases
            }
        ],
        chart: {
            height: 350,
            type: 'line',
        },
        stroke: {
            curve: 'smooth'
        },
        fill: {
            type: 'solid',
            opacity: [0.35, 1],
        },
        labels: salesData.dates,
        markers: {
            size: 0
        },
        yaxis: [
            {
                title: {
                    text: 'Sales',
                },
            },
            {
                opposite: true,
                title: {
                    text: 'Purchases',
                },
            },
        ],
        tooltip: {
            shared: true,
            intersect: false,
            y: {
                formatter: function (y) {
                    if (typeof y !== "undefined") {
                        return y.toFixed(0) + " orders";
                    }
                    return y;
                }
            }
        }
    };

    var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
    areaChart.render();
});
