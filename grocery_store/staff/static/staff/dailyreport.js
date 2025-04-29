// SIDEBAR TOGGLE

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

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



// //--------- CHARTS ----------

// //BAR CHART

// var options = {
//     series: [{
//     data: [400, 430, 448, 470]
//   }],
//     chart: {
//     type: 'bar',
//     height: 350
//   },
//   plotOptions: {
//     bar: {
//       borderRadius: 4,
//       borderRadiusApplication: 'end',
//       horizontal: true,
//     }
//   },
//   dataLabels: {
//     enabled: false
//   },
//   xaxis: {
//     categories: ['vegetables', 'fruits', 'dairy products', 'other'
//     ],
//   }
//   };


//   var options2 = {
//     series: [{
//     name: 'TEAM A',
//     type: 'area',
//     data: [44, 55, 31, 47, 31, 43, 26, 41, 31, 47, 33]
//   }, {
//     name: 'TEAM B',
//     type: 'line',
//     data: [55, 69, 45, 61, 43, 54, 37, 52, 44, 61, 43]
//   }],
//     chart: {
//     height: 350,
//     type: 'line',
//   },
//   stroke: {
//     curve: 'smooth'
//   },
//   fill: {
//     type:'solid',
//     opacity: [0.35, 1],
//   },
//   labels: ['Dec 01', 'Dec 02','Dec 03','Dec 04','Dec 05','Dec 06','Dec 07','Dec 08','Dec 09 ','Dec 10','Dec 11'],
//   markers: {
//     size: 0
//   },
//   yaxis: [
//     {
//       title: {
//         text: 'Series A',
//       },
//     },
//     {
//       opposite: true,
//       title: {
//         text: 'Series B',
//       },
//     },
//   ],
//   tooltip: {
//     shared: true,
//     intersect: false,
//     y: {
//       formatter: function (y) {
//         if(typeof y !== "undefined") {
//           return  y.toFixed(0) + " points";
//         }
//         return y;
//       }
//     }
//   }
//   };
  

//   document .addEventListener("DOMContentLoaded",function() {
  
//   var chart = new ApexCharts(document.querySelector("#bar-chart"), options);
//   chart.render();
  
// var chart2 = new ApexCharts(document.querySelector("#area-chart"), options2);
// chart2.render();

//   })

// // AREA CHART
 
// // var chart = new ApexCharts(document.querySelector("#bar-chart"), options);
// // chart.render();



document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/dailyreport-data/")
      .then(response => response.json())
      .then(data => {
          // Bar chart (Top Products by Quantity)
          const barOptions = {
              series: [{
                  data: data.top_products.map(p => p.quantity)
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
              xaxis: {
                  categories: data.top_products.map(p => p.name),
                  labels: {
                      style: {
                          colors: '#999', // Black color
                          fontSize: '14px',
                          fontWeight: 600,
                      }
                  }
              },
              yaxis: {
                  labels: {
                      style: {
                          colors: '#999',
                          fontSize: '14px',
                          fontWeight: 600,
                      }
                  }
              }
          };
          const barChart = new ApexCharts(document.querySelector("#bar-chart"), barOptions);
          barChart.render();

          // Area chart (Purchases and Sales)
          const areaOptions = {
              series: [
                  {
                      name: "Purchases",
                      type: "area",
                      data: data.daily_orders.map(o => o.purchases)
                  },
                  {
                      name: "Sales",
                      type: "line",
                      data: data.daily_orders.map(o => o.sales)
                  }
              ],
              chart: {
                  type: "line",
                  height: 350
              },
              stroke: {
                  curve: "smooth"
              },
              labels: data.daily_orders.map(o => o.date),
              xaxis: {
                  labels: {
                      style: {
                          colors: '#999',
                          fontSize: '14px',
                          fontWeight: 600,
                      }
                  }
              },
              yaxis: [
                  {
                      title: {
                          text: "Purchases",
                          style: {
                              color: '#999',
                              fontSize: '14px',
                              fontWeight: 600
                          }
                      },
                      labels: {
                          style: {
                              colors: '#999',
                              fontSize: '14px',
                              fontWeight: 600
                          }
                      }
                  },
                  {
                      opposite: true,
                      title: {
                          text: "Sales",
                          style: {
                              color: '#999',
                              fontSize: '14px',
                              fontWeight: 600
                          }
                      },
                      labels: {
                          style: {
                              colors: '#999',
                              fontSize: '14px',
                              fontWeight: 600
                          }
                      }
                  }
              ],
              tooltip: {
                  shared: true,
                  intersect: false
              }
          };
          const areaChart = new ApexCharts(document.querySelector("#area-chart"), areaOptions);
          areaChart.render();
      })
      .catch(error => {
          console.error("Error loading chart data:", error);
      });
});

