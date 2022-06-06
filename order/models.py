from django.db import models
from store.models import Product

# Create your models here.

class Order(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.IntegerField()
    address = models.CharField(max_length=30)
    email = models.EmailField()
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Order, {self.id}'
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name= 'order_item', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)
    
    
    def __str__(self):
        return str(self.id)
    
    
    def get_cost(self):       
        return self.price * self.quantity
    
    