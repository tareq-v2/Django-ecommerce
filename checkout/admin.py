from django.contrib import admin
from .models import Order, OrderItem
from django.db.models import Sum, F

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'get_cost')
    
    def get_cost(self, obj):
        return obj.price * obj.quantity
    get_cost.short_description = 'Cost'

# Use this registration approach for OrderAdmin too
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'first_name', 'last_name', 'email', 'paid', 'get_total_cost')
    list_filter = ('paid', 'created')
    search_fields = ('first_name', 'last_name', 'email')
    inlines = [OrderItemInline]
    readonly_fields = ('get_total_cost',)
    
    def get_total_cost(self, obj):
        return sum(item.get_cost() for item in obj.items.all())
    get_total_cost.short_description = 'Total Cost'
    
    change_list_template = 'admin/orders/order/change_list.html'
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        
        # Calculate sales metrics
        total_orders = Order.objects.count()
        total_sales = Order.objects.aggregate(
            total=Sum(F('items__price') * F('items__quantity'))
        )['total'] or 0
        
        # Get top selling products
        from products.models import Product
        top_products = Product.objects.annotate(
            total_sold=Sum('order_items__quantity')
        ).order_by('-total_sold')[:5]
        
        if not response.context_data:
            response.context_data = {}
            
        response.context_data['total_orders'] = total_orders
        response.context_data['total_sales'] = total_sales
        response.context_data['top_products'] = top_products
        
        return response

# Register Order model
admin.site.register(Order, OrderAdmin)