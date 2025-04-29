from django.urls import path
from . import views

urlpatterns = [
    path("", views.landingPage, name="landing"),
    path("login", views.loginPage, name="login"),
    path("dashboard/", views.dashboardPage, name="dashboard"),
    path("api/login", views.login_view, name="api_login"),
    path("api/addstock", views.addStock_view, name="api_addstock"), 
    path("inventory", views.inventoryPage, name="inventory"),
    path("orders", views.orderPage, name="orders"),
    path("addstock", views.addStockPage, name="addstock"),
    path("sale", views.salePage, name="sale"),
    path('api/sale-data/', views.saleDataAPI, name='sale-data-api'),
    path("dailyreport", views.dailyreportPage, name="dailyreport"),
    path("logout/", views.ajax_logout, name="logout"),
    path("api/createcart", views.create_cart, name="create_cart"),
    path('cart/delete/<int:order_id>/', views.delete_cart, name='delete_cart'),
    path('cart/get/<int:order_id>/', views.get_cart, name='get_cart'),
    path('cart/edit/<int:order_id>/', views.edit_cart, name='edit_cart'),
    path('cart/checkout/<int:order_id>/', views.checkout_cart, name='checkout_cart'),
    path("ajax/logout/", views.ajax_logout, name="ajax_logout"),
    path("api/dailyreport-data/", views.dailyreport_data, name="dailyreport_data"),
]
