from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from farmers.models import FarmerProfile, Product
from payments.models import Payment
from django.db.models import Sum, Count

@staff_member_required
def dashboard_home(request):
    stats = {
        'total_users': User.objects.count(),
        'total_farmers': FarmerProfile.objects.count(),
        'total_products': Product.objects.count(),
        'total_payments': Payment.objects.count(),
        'total_revenue': Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0,
        'pending_payments': Payment.objects.filter(status='pending').count(),
    }
    recent_payments = Payment.objects.select_related('user').order_by('-created_at')[:10]
    return render(request, 'dashboard/home.html', {'stats': stats, 'recent_payments': recent_payments})

@staff_member_required
def users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users.html', {'users': users})

@staff_member_required
def farmers_list(request):
    farmers = FarmerProfile.objects.select_related('user').annotate(product_count=Count('products')).order_by('-id')
    return render(request, 'dashboard/farmers.html', {'farmers': farmers})

@staff_member_required
def products_list(request):
    products = Product.objects.select_related('farmer__user').order_by('-created_at')
    return render(request, 'dashboard/products.html', {'products': products})

@staff_member_required
def payments_list(request):
    payments = Payment.objects.select_related('user').order_by('-created_at')
    return render(request, 'dashboard/payments.html', {'payments': payments})
