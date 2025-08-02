from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    
    def ready(self):
        # Import admin and models here to avoid circular imports
        from django.contrib import admin
        from .models import Product
        from .admin import ProductAdmin
        
        # Unregister and re-register to prevent duplicate
        if admin.site.is_registered(Product):
            admin.site.unregister(Product)
        admin.site.register(Product, ProductAdmin)