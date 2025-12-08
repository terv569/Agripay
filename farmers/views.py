
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FarmerProfile, Product
from .forms import ProductForm
from django.contrib.auth.models import User

def index(request):
    products = Product.objects.all()
    farmers = FarmerProfile.objects.select_related('user').all()
    return render(request, 'farmers/index.html', {'products': products, 'farmers': farmers})


def profile(request, pk):
    fp = get_object_or_404(FarmerProfile, pk=pk)
    # get products for this farmer (omit prices in template)
    products = fp.products.all()
    return render(request, 'farmers/profile.html', {'farmer': fp, 'products': products})

@login_required
def create_product(request):
    # create a simple farmer profile if missing
    fp, _ = FarmerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.farmer = fp
            p.save()
            return redirect('farmers:farmers_index')
    else:
        form = ProductForm()
    return render(request, 'farmers/product_form.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer__user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('farmers:farmers_index')
    else:
        form = ProductForm(instance=product)
    return render(request, 'farmers/product_form.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer__user=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('farmers:farmers_index')
    return render(request, 'farmers/confirm_delete.html', {'product': product})
