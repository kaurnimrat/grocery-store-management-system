import datetime
from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.TextField(max_length=255)

    def __str__(self):
        return self.name

class Item(models.Model):
    name=models.TextField(max_length=255)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.FloatField() 
    quantity=models.IntegerField()

    def __str__(self):
        return f"{self.name} : {self.category.name} :    {self.price}/-"

class Order(models.Model):
    name=models.TextField(max_length=255)
    items=models.ManyToManyField(Item, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid=models.BooleanField()

    def __str__(self):
        return f"{self.name} : {self.created_at}"
        # return f"{self.name} :"