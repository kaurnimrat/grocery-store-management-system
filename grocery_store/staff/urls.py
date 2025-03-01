from django.urls import path
from . import views

urlpatterns = [
    path("", views.landingPage),
    path("login",views.loginPage),
    path("dashboard",views.dashboardPage),
    path("api/login",views.login_view),
]

