from django.contrib import admin
from .models import Product

# First unregister if already registered
if admin.site.is_registered(Product):
    admin.site.unregister(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_price', 'get_stock', 'total_sold']
    search_fields = ('name', 'description')
    
    def get_name(self, obj):
        return obj.name
    get_name.short_description = 'Name'
    
    def get_price(self, obj):
        return obj.price
    get_price.short_description = 'Price'
    
    def get_stock(self, obj):
        return obj.stock
    get_stock.short_description = 'Stock'
    
    def total_sold(self, obj):
        return obj.total_sold()
    total_sold.short_description = 'Units Sold'

admin.site.register(Product, ProductAdmin)