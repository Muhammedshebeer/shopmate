from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponseBadRequest
from django.conf import settings
import json
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import UserProfile
from django.http import HttpResponseRedirect
import razorpay


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        return redirect('profile')  # Replace with your URL name

    return render(request, 'profile.html', {'profile': profile})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'register.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, "Invalid credentials.")
#             return redirect('login')

#     return render(request, 'login.html')


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    products = Product.objects.all()
    titles = Titlepage.objects.first()
    subtitle = Subtitles.objects.all()
    category = Categories.objects.all()

    Featuredproducts = Product.objects.none()  # fallback if no match
    Topdealproducts = Product.objects.none()

    try:
        featured_category = Categories.objects.get(CategoryName='featured')
        Featuredproducts = Product.objects.filter(DealCategory=featured_category)
    except Categories.DoesNotExist:
        pass
    
    try:
        top_deal_category = Categories.objects.get(CategoryName='top deal')
        Topdealproducts = Product.objects.filter(DealCategory=top_deal_category)
    except Categories.DoesNotExist:
        pass

    
    cart = request.session.get('cart', {})
    has_cart_items = bool(cart)
    print("Cart contents:", cart)           # Debug print
    print("Has cart items?:", has_cart_items)  # Debug print

    
    context = {
        'products': products,
        'titles': titles,
        'subtitle': subtitle,
        'category': category,
        'Featuredproducts': Featuredproducts,
        'Topdealproducts': Topdealproducts,
        'has_cart_items': has_cart_items,  # include the flag here
    }

    return render(request, 'index.html', context)

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('home')  # or wherever you want

def clear_orders(request):
    OrderItem.objects.all().delete()
    Order.objects.all().delete()

    messages.success(request, "All orders and order items have been deleted.")
    return HttpResponseRedirect(reverse('admin:index'))
    
    return HttpResponse(message)
def delete_all_products(request):
    if request.method == 'POST':
        Product.objects.all().delete()
        return redirect('product_list')  # Replace with the name of your product list URL/view
    return redirect('product_list')


def header(request):
    return render(request,"header.html")

# def analyzed(request):
#     if request.method == 'GET':
#         text = request.GET.get('text', '')
#         remove = request.GET.get('remove', 'off')
#         capital = request.GET.get('capital', 'off')

#         if remove == "off" and capital == "off":
#             return HttpResponse('You should click on the checkbox')

#         analyze = text

#         if remove == "on":
#             punctuations = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
#             analyze = ''.join(char for char in analyze if char not in punctuations)

#         if capital == "on":
#             analyze = analyze.upper()

#         data = {
#             "analyzed_text": analyze
#         }

#         return render(request, 'analyze.html', data)

#     return HttpResponse("Invalid Request")

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('ProductName')
        product_category = request.POST.get('ProductCategory')
        image = request.FILES.get('Image')  # image comes from request.FILES
        description = request.POST.get('Description')
        price = request.POST.get('Price')
        offer_price = request.POST.get('OfferPrice')

        Product.objects.create(
            ProductName=product_name,
            ProductCategory=product_category,
            Image=image,
            Description=description,
            Price=price,
            OfferPrice=offer_price
        )
        return redirect('add_product')  # Or redirect to a product list page

    products=Product.objects.all()
    
    return render(request,'add_product.html',{"products":products})

# def title(request):
#     # titles= Titlepage.objects.all()
#     return render(request,'index.html',{"titles":titles})

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    Featuredproducts = Product.objects.none()
    
    try:
        featured_category = Categories.objects.get(CategoryName='featured')
        Featuredproducts = Product.objects.filter(DealCategory=featured_category)
    except Categories.DoesNotExist:
        pass
    
    return render(request, 'productdetails.html', {'product': product,'Featuredproducts': Featuredproducts,}) 


def Product_page(request):
    print('***********')
    allproducts =Product.objects.all()
    brandsearch = Brands.objects.all()
    
    return render (request, 'productpage.html', {'allproducts' : allproducts , 'brandsearch':brandsearch})  


# def add_to_cart(request, product_id):
#     if request.method == "POST":
#         cart = request.session.get('cart', {})
#         product_id_str = str(product_id)

#         if product_id_str in cart:
#             cart[product_id_str] += 1
#         else:
#             cart[product_id_str] = 1

#         request.session['cart'] = cart
#         return JsonResponse({'success': True, 'message': 'Product successfully added to cart!'})

#     return JsonResponse({'success': False, 'message': 'Invalid request'})

# # Simulated cart structure (in session)
# def cart_view(request):
#     cart = request.session.get('cart', {})
#     cart_items = []
#     total_price = 0

#     for product_id, quantity in cart.items():
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             continue  # Skip if product was deleted

#         subtotal = product.Price * quantity
#         cart_items.append({
#             'product': product,
#             'quantity': quantity,
#             'subtotal': subtotal
#         })
#         total_price += subtotal

#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price
#     }
    
    
#     return render(request, 'cart.html', context)

# def update_cart(request, product_id):
#     if request.method == "POST":
#         action = request.POST.get('action')
#         cart = request.session.get('cart', {})
#         product_id_str = str(product_id)

#         if product_id_str in cart:
#             if action == "increase":
#                 cart[product_id_str] += 1
#             elif action == "decrease":
#                 if cart[product_id_str] > 1:
#                     cart[product_id_str] -= 1
#                 else:
#                     del cart[product_id_str]

#         request.session['cart'] = cart
#     return redirect('cart_view')


# def remove_from_cart(request, product_id):
#     if request.method == "POST":
#         cart = request.session.get('cart', {})
#         product_id_str = str(product_id)

#         if product_id_str in cart:
#             del cart[product_id_str]

#         request.session['cart'] = cart
#     return redirect('cart_view')


@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'success': True, 'message': 'Product added to cart'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.subtotal for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'cart.html', context)


@login_required
def update_cart(request, product_id):
    if request.method == "POST":
        action = request.POST.get('action')
        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
        except CartItem.DoesNotExist:
            return redirect('cart_view')

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                return redirect('cart_view')

        cart_item.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, product_id):
    if request.method == "POST":
        CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart_view')

def all_products_view(request):
    search_query = request.GET.get('search', '')
    brand_filter = request.GET.get('brand', '')
    sort_option = request.GET.get('sort', '')
    
    products = Product.objects.all()
    brands = Brands.objects.all()
    if search_query:
        products = products.filter(ProductName__icontains=search_query)
    
    if brand_filter:
        # Assuming brand_filter holds brand name, filter by Brand.Name
        products = products.filter(Brand__Name=brand_filter)
        
    if sort_option == 'name_asc':
        products = products.order_by('ProductName')
    elif sort_option == 'name_desc':
        products = products.order_by('-ProductName')
    elif sort_option == 'price_asc':
        products = products.order_by('Price')
    elif sort_option == 'price_desc':
        products = products.order_by('-Price')    

    brandsearch = Brands.objects.all()    

    context = {
        'allproducts': products,
        'brandsearch': brandsearch,
        'search_query': search_query,
        'brand_filter': brand_filter,  # For future use (brand filter)
    }
    return render(request, 'productpage.html', context)  # Update template name if needed


def some_view(request):
    cart = request.session.get('cart', {})
    has_items = bool(cart)  # True if cart has any product

    context = {
        'has_cart_items': has_items,
        # other context data...
    }
    return render(request, 'home.html', context)



# Initialize Razorpay client with your test keys
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# @login_required
# def checkout_view(request):
#     user = request.user
#     cart_items = CartItem.objects.filter(user=user)
#     total_price = sum(item.subtotal for item in cart_items)
#     razorpay_amount = int(total_price * 100)  # Razorpay accepts amount in paise

#     if request.method == 'POST':
#         # This POST comes after successful payment
#         full_name = request.POST.get('full_name')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         postal_code = request.POST.get('postal_code')
#         phone = request.POST.get('phone')
#         razorpay_order_id = request.POST.get('razorpay_order_id')
#         razorpay_payment_id = request.POST.get('razorpay_payment_id')
#         razorpay_signature = request.POST.get('razorpay_signature')

#         # Step 1: Verify payment signature
#         params_dict = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': razorpay_payment_id,
#             'razorpay_signature': razorpay_signature
#         }

#         try:
#             razorpay_client.utility.verify_payment_signature(params_dict)
#         except:
#             messages.error(request, "Payment verification failed.")
#             return redirect('checkout')

#         # Step 2: Validate stock
#         insufficient_items = []
#         for item in cart_items:
#             if item.quantity > item.product.AvailableQuantity:
#                 insufficient_items.append(
#                     f"{item.product.ProductName} (Available: {item.product.AvailableQuantity}, Requested: {item.quantity})"
#                 )

#         if insufficient_items:
#             for msg in insufficient_items:
#                 messages.error(request, f"Not enough stock for: {msg}")
#             return redirect('cart_view')

#         # Step 3: Create Order
#         order = Order.objects.create(
#             user=user,
#             full_name=full_name,
#             address=address,
#             city=city,
#             postal_code=postal_code,
#             phone=phone,
#             total_price=total_price,
#         )

#         # Step 4: Create OrderItems and deduct stock
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 subtotal=item.subtotal
#             )
#             product = item.product
#             product.AvailableQuantity -= item.quantity
#             product.save()

#         # Step 5: Clear Cart
#         cart_items.delete()

#         messages.success(request, 'Your order has been placed successfully!')
#         return redirect('payment_success')

#     else:
#         # Create Razorpay Order on GET
#         razorpay_order = razorpay_client.order.create({
#             'amount': razorpay_amount,
#             'currency': 'INR',
#             'payment_capture': '1'
#         })

#         return render(request, 'checkout.html', {
#             'cart_items': cart_items,
#             'total_price': total_price,
#             'razorpay_order': razorpay_order,
#             'razorpay_key_id': settings.RAZORPAY_KEY_ID,
#         })


@login_required
def checkout_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = sum(item.subtotal for item in cart_items)
    razorpay_amount = int(total_price * 100)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')

        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except:
            return HttpResponse("Payment signature verification failed", status=400)

        # Create JSON-style product list
        product_list = []
        for item in cart_items:
            product_list.append({
                'product_id': item.product.id,
                'product_name': item.product.ProductName,
                'quantity': item.quantity,
                'price': float(item.product.Price),
                'subtotal': float(item.subtotal),
            })

        # Create Order (includes JSON summary)
        order = Order.objects.create(
            user=user,
            full_name=full_name,
            address=address,
            city=city,
            postal_code=postal_code,
            phone=phone,
            total_amount=total_price,
            ordered_items=product_list,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            paid=True,
        )

        # Create individual OrderItem entries
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.Price
            )

        # Clear the user's cart
        cart_items.delete()
        return redirect('success')

    # Razorpay order create (for frontend)
    razorpay_order = razorpay_client.order.create(dict(
        amount=razorpay_amount,
        currency='INR',
        payment_capture='1'
    ))

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order': razorpay_order,
        'user': user,
    }
    return render(request, 'checkout.html', context)


# @login_required
# def checkout_view(request):
#     user = request.user
#     cart_items = CartItem.objects.filter(user=user)
#     total_price = sum(item.subtotal for item in cart_items)

#     if request.method == 'POST':
#         full_name = request.POST.get('full_name')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         postal_code = request.POST.get('postal_code')
#         phone = request.POST.get('phone')

#         # Step 1: Validate Stock for all items
#         insufficient_items = []
#         for item in cart_items:
#             if item.quantity > item.product.AvailableQuantity:
#                 insufficient_items.append(
#                     f"{item.product.ProductName} (Available: {item.product.AvailableQuantity}, Requested: {item.quantity})"
#                 )

#         if insufficient_items:
#             for msg in insufficient_items:
#                 messages.error(request, f"Not enough stock for: {msg}")
#             return redirect('cart_view')

#         # Step 2: Create Order
#         order = Order.objects.create(
#             user=user,
#             full_name=full_name,
#             address=address,
#             city=city,
#             postal_code=postal_code,
#             phone=phone,
#             total_price=total_price
#         )

#         # Step 3: Create OrderItems and deduct stock
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 subtotal=item.subtotal
#             )
#             product = item.product
#             product.AvailableQuantity -= item.quantity
#             product.save()

#         # Step 4: Clear Cart
#         cart_items.delete()

#         messages.success(request, 'Your order has been placed successfully!')
#         return redirect('order-success')

#     return render(request, 'checkout.html', {
#         'cart_items': cart_items,
#         'total_price': total_price
#     })
    
# def order_success(request):
#     return render(request, 'ordersuccess.html')



# client = razorpay.Client(auth=("rzp_test_xvfbKQfVSgrD2m", "EI42BygwCKRduMQY2rcjXB7z"))

# def create_order(request):
#     if request.method == "POST":
#         amount = 50000  # e.g., Rs. 500.00 in paise

#         order = Order.objects.create(user=request.user, amount=amount / 100)

#         payment = client.order.create({
#             "amount": amount,
#             "currency": "INR",
#             "payment_capture": "1"
#         })

#         order.razorpay_order_id = payment['id']
#         order.save()

#         context = {
#             "order": order,
#             "order_id": payment['id'],
#             "amount": amount,
#             "razorpay_key": "rzp_test_xvfbKQfVSgrD2m",
#             "user": request.user,
#         }
#         return render(request, "payment.html", context)

#     return render(request, "checkout.html")
    
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        from .models import Order

        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.paid = True
            order.save()

            return JsonResponse({'status': 'success'})

        except Order.DoesNotExist:
            return JsonResponse({'status': 'failed', 'reason': 'Order not found'}, status=404)

    return JsonResponse({'status': 'failed', 'reason': 'Invalid request'}, status=400)


def success_page(request):
    return render(request, "ordersuccess.html")