from django.db import models
from django.db.models import Sum

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return self.name
    
    def total_sold(self):
        # Safely calculate total sold using aggregation
        result = self.order_items.aggregate(total_sold=Sum('quantity'))
        return result['total_sold'] or 0