from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product

# Add product to cart
def product_list(request):
    return render(request, 'store/product_list.html')
                        
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})
    
    # If product already in the cart, increase quantity
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'name': product.name, 'price': str(product.price), 'quantity': 1}
    
    # Save the updated cart in session
    request.session['cart'] = cart
    return redirect('cart')

# View cart
def view_cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'store/cart.html', {'cart': cart})

# Checkout with WhatsApp redirection
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')  # If cart is empty, redirect back to cart

    # Prepare the cart details as a message
    cart_details = ""
    total_price = 0
    for item in cart.values():
        cart_details += f"{item['name']} (x{item['quantity']}) - ${item['price']} each\n"
        total_price += float(item['price']) * item['quantity']

    message = f"Hi, I'd like to buy the following products:\n\n{cart_details}\nTotal: ${total_price}\nPlease contact me for further details."
    
    # Redirect to WhatsApp with the cart details
    whatsapp_url = f"https://wa.me/?text={message}"
    return redirect(whatsapp_url)


