
from django.shortcuts import render
from farmers.models import Product
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST


@require_POST
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    # store quantity in cart; default add 1
    cart_item = cart.get(str(product.pk), {'name': product.name, 'qty': 0})
    cart_item['qty'] = cart_item.get('qty', 0) + 1
    cart[str(product.pk)] = cart_item
    request.session['cart'] = cart
    return redirect('marketplace:marketplace_index')

def index(request):
    products = Product.objects.all()
    return render(request, 'marketplace/index.html', {'products': products})


def cart(request):
    """Show cart stored in session."""
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, data in cart.items():
        try:
            prod = Product.objects.get(pk=int(pid))
            qty = int(data.get('qty', 0))
            subtotal = qty * float(prod.price)
            items.append({'product': prod, 'qty': qty, 'subtotal': subtotal})
            total += subtotal
        except Product.DoesNotExist:
            continue
    return render(request, 'marketplace/cart.html', {'items': items, 'total': total})
