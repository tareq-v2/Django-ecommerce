import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from cart.utils import Cart
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutView(TemplateView):
    template_name = 'checkout/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        cart = Cart(request)
        total = cart.get_total_price()
        
        try:
            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),  # Convert to cents
                currency='usd',
                automatic_payment_methods={'enabled': True},
            )
            return JsonResponse({'clientSecret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)
    return redirect('checkout:checkout')

def payment_success(request):
    cart = Cart(request)
    # Create order
    order = Order.objects.create(
        first_name="Customer First",
        last_name="Customer Last",  
        email="customer@example.com",
        address="123 Main St",
        postal_code="12345",
        city="City",
        paid=True
    )
    # Create order items
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        )
    cart.clear()
    return render(request, 'checkout/success.html', {'order': order})

def payment_cancel(request):
    return render(request, 'checkout/cancel.html')