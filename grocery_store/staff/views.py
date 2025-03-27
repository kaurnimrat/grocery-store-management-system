from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt 
import json
from .models import *

# Create your views here.
def landingPage(request):
    items_list = Item.objects.all()
    context = {
        "products": [],
        "Category": [],
    }

    for item in items_list:
        temp = {
            "name" : item.name,
            "price" : item.price,
        }
        context["products"].append(temp)
    

        print(context)
    return render(request, "landingPage.html", context)

def loginPage(request):
    return render(request, "login.html")

def dashboardPage(request):
    context = {
        'orders' : [],
    }

    orders = Order.objects.all()
    print(orders)
    for order in orders:
        if (order.is_paid):
            continue
        else:
            temp = {
                'id' : order.id,
                "name": order.name,
                "items": [],
                'total' :0,
            }
            total = 0
            for item in order.items.all():
                temp_item = {
                    "name" : item.name,
                    "price": item.price,

                }
                total += item.price
                temp["items"].append(temp_item)

            temp["total"]=total
            context["orders"].append(temp)

    return render(request, "dashboard.html", context)

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

def inventoryPage(request):
    context = {
        'items' : [],
    }

    items = Item.objects.all()
    print(items)
    for item in items:
        temp = {
            'name' : item.name,
            'category' : item.category.name,
            'price' : item.price,
            'quantity' :  item.quantity,
            'stock_price': item.quantity*item.price,
        }
        context["items"].append(temp)
    
    print(context)
    
    return render(request,"inventory.html", context)

def orderPage(request):
    context = {
        'orders' : [], 
    }

    orders = Order.objects.all()
    print(orders)
    for order in orders:
        temp = {
            'id' : order.id,
            "name": order.name,
            "items": [],
            "total_items" : 0
        }
        total = 0

        for item in order.items.all():
            temp_item = {
                "name" : item.name,
                "price": item.price,
            }
            total += item.price
            temp["items"].append(temp_item)
            temp["total_items"] += 1
            
        temp["total"]=total
        context["orders"].append(temp)
    return render(request,"order.html", context)

def addStockPage(request):
    return render(request,"add_stock.html")

def salePage(request):
    return render(request,"sale.html")