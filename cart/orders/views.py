from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, OrderedItem
from products.models import Product
from django.contrib.auth.decorators import login_required

def my_cart(request):

    user = request.user
    customer = user.customer_profile

    cart = Order.objects.filter(
        owner=customer,
        order_status=Order.CART_STAGE
    ).first()

    subtotal = 0
    cart_items = []

    if cart:
        for item in cart.added_items.all():

            item_subtotal = item.product.price * item.quantity

            item.item_subtotal = item_subtotal

            cart_items.append(item)

            subtotal += item_subtotal

    tax = subtotal * 0.18
    total = subtotal + tax

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    }

    return render(request, 'cart.html', context)

def add_to_cart(request):

    if request.method == "POST":

        user = request.user
        customer = user.customer_profile

        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')

        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        product = Product.objects.get(pk=product_id)

        # Check if product already exists in cart
        ordered_item = OrderedItem.objects.filter(
            owner=cart_obj,
            product=product
        ).first()

        if ordered_item:
            # Product already exists, increase quantity
            ordered_item.quantity += quantity
            ordered_item.save()

        else:
            # Product does not exist, create new item
            OrderedItem.objects.create(
                product=product,
                owner=cart_obj,
                quantity=quantity
            )

    return redirect('cart')

def remove_item_from_cart(request, pk):

    item = OrderedItem.objects.get(pk=pk)
    item.delete()

    return redirect('cart')

def checkout_item(request, pk):

    item = OrderedItem.objects.get(pk=pk)

    cart = item.owner
    product_name = item.product.title

    # Create a separate confirmed order
    confirmed_order = Order.objects.create(
        owner=cart.owner,
        order_status=Order.ORDER_CONFIRMED
    )

    # Save product inside confirmed order
    OrderedItem.objects.create(
        product=item.product,
        quantity=item.quantity,
        owner=confirmed_order
    )

    # Remove product from cart
    item.delete()

    messages.success(
        request,
        f"Order confirmed! Your {product_name} will be delivered within 2-3 days."
    )

    return redirect('cart')

@login_required
def order_status(request):

    customer = request.user.customer_profile

    orders = Order.objects.filter(
        owner=customer,
        order_status__gte=Order.ORDER_CONFIRMED
    ).prefetch_related(
        'added_items__product'
    ).order_by('-created_at')

    context = {
        'orders': orders
    }

    return render(request, 'order_status.html', context)