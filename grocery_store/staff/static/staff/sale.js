// SIDEBAR TOGGLE

var sidebarOpen = false;
var sidebar = document.getElementById{"sidebar"};

function openSidebar() {
    if(!sidebarOpen) {
        sidebar.classlist.add("sidebar-responsive");
        sidebarOpen = true;
    }
}

function closeSidebar() {
    if(!sidebarOpen) {
        sidebar.classlist.remove("sidebar-responsive");
        sidebarOpen = false;
    }
}



//--------- CHARTS ----------

//BAR CHART
// var barChartOptions = {
//     series: [{
//         data: [10, 8, 6, 4, 2],
//         name: "Products",
//     }],
//     charts: {
//       type: "bar",
//       background: "transparent",
//       height: 350,
//       toolbar: {
//         show: false,
//       },
//     },
//     colors: [
//         "#2962ff",
//         "#d50000",
//         "#2e7d32",
//         "#ff6d00",
//         "#583cb3",
//     ],
//     plotOptions: {
//         bar: {
//             distribution: true,
//             borderRadius: 4,
//             horizontal: false,
//             columnWidth: "40%",
//         }
//     },
//     dataLabels: {
//      enabled: false,
//     },
//     fill: {
//      opacity: 1,
//     },
//     grid: {
//         borderColor: "#55596e",
//         yaxis: {
//             lines: {
//                 show: true,
//             },
//         },
//         xaxis: {
//          lines: {
//           show: true,
//             },
//         },
//     },
//     legend: {
//         labels: {
//             colors: "#f5f7ff",
//         },
//         show: true,
//         position: "top",
//     },
//     stroke: {
//         colors: ["tranparent"],
//         show: true,
//         width: 2
//     },
//     tooltip: {
//         shared: true,intersect: false,
//         theme: "dark",
//     },
//     xaxis: {
//         categories: ["Laptop", "Phone", "Monitor", "Headphones", "Camera"],
//         title: {
//             style: {
//                 color: "#f5f7ff",
//             },
//         },
//         axisBorder: {
//             show: true,
//             color: "#55596e",
//         },
//         axisTricks: {
//             show: true,
//             color: "#55596e",
//         },
//         labels: {
//             style: {
//                 colors: "#f5f7ff",
//             },
//         },
//     },
//     yaxis: {
//         title:{
//             text: "Count",
//             style: {
//                 color: "#f5f7ff",
//             },
//         },
//     }
// },


var options = {
    series: [{
    data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
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
    categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
      'United States', 'China', 'Germany'
    ],
  }
  };

  var chart = new ApexCharts(document.querySelector("#chart"), options);
  chart.render();
