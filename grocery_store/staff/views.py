from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt 
import json

# Create your views here.
def landingPage(request):
    return render(request, "landingPage.html")

def loginPage(request):
    return render(request, "login.html")

def dashboardPage(request):
    return render(request, "dashboard.html")

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('login_username')
        password = data.get('login_password')

        user=authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, 'message': 'Invalid credentials'})
    return JsonResponse({'success': False, 'message': 'invalid request method'})