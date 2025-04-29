from django.db import models

class Category(models.Model):
    name = models.TextField(max_length=255)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.TextField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    url = models.URLField(default="https://cdn-icons-png.flaticon.com/512/263/263142.png")

    def __str__(self):
        return f"{self.name} : {self.category.name} : {self.price}/-"

class Order(models.Model):
    name = models.TextField(max_length=255)
    items=models.ManyToManyField(Item, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} : {self.created_at}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} x {self.quantity} in {self.order.name}"
