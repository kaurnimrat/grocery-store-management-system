from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt 
from django.db.models import Count
import json
from .models import Item, Category, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now, timedelta
from datetime import timedelta
from django.db.models import Sum, F, DecimalField


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
    
    return render(request, "landingPage.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "login.html")

@login_required
def dashboardPage(request):
    context = {
        'orders': [], 
        'products': Item.objects.all(),
        "total_purchases": Order.objects.count(),
        "total_sales": OrderItem.objects.filter(
                order__created_at__date=timezone.now().date()
            ).aggregate(
                total_sales=Sum(F('quantity') * F('item__price'), output_field=DecimalField())
            )['total_sales'] or 0,
        "stock_value": Item.objects.aggregate(stock_value=Sum(F('price') * F('quantity'), output_field=DecimalField()))['stock_value'] or 0,
    }
    context["paid_orders"] = Order.objects.filter(is_paid=True).count()
    
    # orders = Order.objects.prefetch_related('orderitem_set__item').filter(is_paid=False)
    orders = Order.objects.filter(is_paid=False).prefetch_related("orderitem_set__item")

    for order in orders:
        temp = {
            'id': order.id,
            'name': order.name,
            'items': [],
            'total': 0,
        }

        total = 0
        for order_item in order.orderitem_set.all():
            item = order_item.item
            quantity = order_item.quantity
            temp_item = {
                'name': item.name,
                'price': item.price,
                'url': item.url,
                'quantity': quantity,
            }
            total += item.price * quantity
            temp['items'].append(temp_item)

        temp['total'] = total
        context['orders'].append(temp)

    return render(request, "dashboard.html", context)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('login_username')
        password = data.get('login_password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, 'message': 'Invalid credentials'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def inventoryPage(request):
    context = {'items': []}
    items = Item.objects.all()
    for item in items:
        temp = {
            'name': item.name,
            'category': item.category.name,
            'price': item.price,
            'quantity': item.quantity,
            'stock_price': item.quantity * item.price,
        }
        context["items"].append(temp)
    return render(request, "inventory.html", context)

@login_required
def orderPage(request):
    context = {'orders': []}
    orders = Order.objects.prefetch_related('orderitem_set__item')

    for order in orders:
        temp = {
            'id': order.id,
            "name": order.name,
            "items": [],
            "total_items": 0,
            "total": 0,
        }

        for order_item in order.orderitem_set.all():
            item = order_item.item
            quantity = order_item.quantity
            temp["items"].append({
                "name": item.name,
                "price": item.price,
                "quantity": quantity,
            })
            temp["total_items"] += quantity
            temp["total"] += item.price * quantity

        context["orders"].append(temp)
    return render(request, "order.html", context)

@login_required
def addStockPage(request):
    return render(request, "add_stock.html")

@csrf_exempt
@login_required
def addStock_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item_name = data.get('item_name')
        item_category = data.get('item_category')
        item_price = data.get('item_price')
        item_quantity = data.get('item_quantity')

        item_name = str(item_name).lower()
        item_category = str(item_category).lower()

        cat, _ = Category.objects.get_or_create(name=item_category)

        item, created_item = Item.objects.get_or_create(
            name=item_name, category=cat,
            defaults={'price': item_price, 'quantity': item_quantity}
        )

        if not created_item:
            return JsonResponse({"success": False, 'message': 'Item already exists'})
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)
@login_required
def salePage(request):
    products_count = Item.objects.count()
    categories_count = Category.objects.count()
    customers_count = Order.objects.values('name').distinct().count()
    alerts_count = Item.objects.filter(quantity__lt=10).count()

    context = {
        "products_count": products_count,
        "categories_count": categories_count,
        "customers_count": customers_count,
        "alerts_count": alerts_count,
    }
    return render(request, "sale.html", context)

@login_required
def saleDataAPI(request):
    top_products_qs = Item.objects.order_by('-quantity')[:4]
    top_products = [{"name": item.name, "quantity": item.quantity} for item in top_products_qs]

    today = timezone.now()
    seven_days_ago = today - timedelta(days=7)

    daily_orders = (
        Order.objects
        .filter(created_at__date__gte=seven_days_ago.date())
        .extra(select={'day': "date(created_at)"})
        .values('day')
        .annotate(sales=Count('id'))
        .order_by('day')
    )

    dates = []
    sales = []

    for entry in daily_orders:
        # entry["day"] is a string already because of .extra()
        dates.append(entry["day"])
        sales.append(entry["sales"])

    response_data = {
        "top_products": top_products,
        "sales_data": {
            "dates": dates,
            "sales": sales,
        }
    }
    return JsonResponse(response_data)

@login_required
def dailyreportPage(request):
    return render(request, "dailyreport.html")

@csrf_exempt
@login_required
def ajax_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid method"}, status=400)


@csrf_exempt
@login_required
def create_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_name = data.get("customer_name")
            items_data = data.get("items", [])

            if not customer_name or not items_data:
                return JsonResponse({"error": "Customer name and items are required."}, status=400)
            
            is_paid = data.get("is_paid", False)
            order = Order.objects.create(name=customer_name, is_paid=is_paid)


            # Add each item to the order
            for entry in items_data:
                item_id = entry.get("item_id")
                quantity = int(entry.get("quantity", 1))

                if not item_id or quantity < 1:
                    continue  # Skip invalid entries

                item = Item.objects.get(id=item_id)
                OrderItem.objects.create(order=order, item=item, quantity=quantity)

            return JsonResponse({"status": "success", "order_id": order.id})

        except Item.DoesNotExist:
            return JsonResponse({"error": "One or more items not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
@login_required
def delete_cart(request, order_id):
    if request.method == "DELETE":
        try:
            Order.objects.filter(id=order_id).delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt
@login_required
def get_cart(request, order_id):
    try:
        order = Order.objects.prefetch_related("orderitem_set__item").get(id=order_id)
        items = [
            {"id": oi.item.id, "name": oi.item.name, "quantity": oi.quantity}
            for oi in order.orderitem_set.all()
        ]
        all_products = list(Item.objects.values("id", "name"))
        return JsonResponse({
            "name": order.name,
            "is_paid": order.is_paid,
            "items": items,
            "all_products": list(all_products)
        })
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

@csrf_exempt
@login_required
def edit_cart(request, order_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            order = Order.objects.get(id=order_id)
            order.name = data["customer_name"]
            order.is_paid = data.get("is_paid", False)
            order.save()

            order.orderitem_set.all().delete()
            for item_data in data["items"]:
                item = Item.objects.get(id=item_data["item_id"])
                OrderItem.objects.create(order=order, item=item, quantity=item_data["quantity"])

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        
@csrf_exempt
@login_required
def checkout_cart(request, order_id):
    if request.method == "POST":
        try:
            order = Order.objects.get(id=order_id)
            order.is_paid = True
            order.save()
            return JsonResponse({"status": "success"})
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Order not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        

@login_required
def dailyreport_data(request):
    # Top 4 products by stock quantity
    top_products = list(
        Item.objects.order_by('-quantity')[:4].values('name', 'quantity')
    )

    # Daily sales and purchase counts for the past 10 days
    today = now().date()
    days = [today - timedelta(days=i) for i in range(9, -1, -1)]
    labels = [d.strftime("%b %d") for d in days]

    daily_orders = []
    for date in days:
        next_day = date + timedelta(days=1)
        sales = Order.objects.filter(created_at__date=date, is_paid=True).count()
        purchases = Order.objects.filter(created_at__date=date, is_paid=False).count()
        daily_orders.append({
            "date": date.strftime("%b %d"),
            "sales": sales,
            "purchases": purchases
        })

    return JsonResponse({
        "top_products": top_products,
        "daily_orders": daily_orders
    })