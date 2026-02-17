from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


@login_required(login_url='login')
def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'store/product_detail.html', {'product': product})


@login_required(login_url='login')
def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart
    return redirect('view_cart')


@login_required(login_url='login')
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    final_amount = 0

    for id in cart:
        product = Product.objects.get(id=id)
        quantity = cart[id]
        total = product.price * quantity
        final_amount += total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'final_amount': final_amount
    })


@login_required(login_url='login')
def increase(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')


@login_required(login_url='login')
def decrease(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        if cart[str(id)] > 1:
            cart[str(id)] -= 1
        else:
            del cart[str(id)]

    request.session['cart'] = cart
    return redirect('view_cart')


@login_required(login_url='login')
def remove(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart
    return redirect('view_cart')


@login_required(login_url='login')
def checkout(request):
    request.session['cart'] = {}
    return render(request, 'store/checkout.html')
