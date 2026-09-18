from django.shortcuts import render

# Create your views here.

def my_cart(request):
    return render(request, 'cart.html')