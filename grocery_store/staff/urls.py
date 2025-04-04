from django.urls import path
from . import views

urlpatterns = [
    path("", views.landingPage),
    path("login",views.loginPage),
    path("dashboard",views.dashboardPage),
    path("api/login",views.login_view),
    path("api/addstock",views.addStock_view), 
    path("inventory",views.inventoryPage),
    path("orders",views .orderPage),
    path("addstock",views.addStockPage),
    path("sale",views.salePage),
    path("dailyreport",views.dailyreportPage),
]

