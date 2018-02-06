from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib import messages
from product.models import Product, Subcategory, Order


def index(request):
    context = {
        'products': Product.objects.filter(on_the_main=True)
    }
    return render(request, 'product/index.html', context)


def subcategory_product(request, id):
    context = {
        'subcategory': get_object_or_404(Subcategory, id=id)
    }
    return render(request, 'product/subcategory-product.html', context)


def product_details(request, id):
    context = {
        'product': get_object_or_404(Product, id=id)
    }
    return render(request, 'product/product-details.html', context)


def add_product_to_session(request, p_id, quantity):
    request.session.modified = True
    if 'products' not in request.session:
        request.session['products'] = []
    if p_id not in request.session['products']:
        request.session['products'].append(
            {'product_id': p_id,
             'quantity': quantity
             }
        )

        messages.info(request, 'Added to cart!')
    else:
        messages.info(request, 'Already exists!')


def cart(request):
    if request.method == 'POST':
        next_page = request.POST.get('next', '/')
        p_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        add_product_to_session(request, p_id, quantity)
        return HttpResponseRedirect(next_page)
    else:
        if request.session.get('products'):
            all_products = []
            for item in request.session.get('products'):
                p_id = item.get('product_id')
                quantity = item.get('quantity')
                product = Product.objects.filter(id=p_id)
                for pr in product:
                    product_title = pr.title
                    product_price = pr.price

                product_dict = {
                    'id': p_id,
                    'title': product_title,
                    'price': product_price,
                    'quantity': quantity
                }

                all_products.append(product_dict)

            subtotal = 0
            for product in all_products:
                subtotal = subtotal + product.get('price')

            if 'subtotal' not in request.session:
                request.session['subtotal'] = []
            request.session['subtotal'] = subtotal

            return render(request, 'product/cart.html', {'products': all_products, 'subtotal': subtotal})

        else:
            return render(request, 'product/cart.html')


def remove_product_from_session(request):
    if request.method == 'POST':
        request.session.modified = True
        p_id = request.POST.get('product_id')

        for product in request.session['products']:
            if product.get('product_id') == str(p_id):
                request.session['products'].remove(product)

        messages.info(request, 'Product removed from cart!')

        return redirect('/cart')


def checkout(request):
    return render(request, 'product/checkout.html')



def complete_order(request):
    if request.method == 'POST':
        request.session.modified = True
        name = request.POST.get('name')
        email = request.POST.get('email')
        subtotal = request.session['subtotal']

        order = Order(name=name, email=email, subtotal=subtotal)
        order.save()

        request.session.flush()



    return redirect('/cart')
