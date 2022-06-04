from django.shortcuts import render, get_object_or_404
from.models import Product, Category, Carousel, Price_filter
from cart.forms import CartAddProductForm

# Create your views here.

def product_list(request, category_slug=None, price_slug=None):
    category = None
    price_filter = None
    prices = Price_filter.objects.all()
    carousels = Carousel.objects.all()
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    
    if price_slug:
        price_filter = get_object_or_404(Price_filter, slug=price_slug)
        products = products.filter(price_filter=price_filter)

    
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'index.html', {'categories':categories, 
                                                        'category':category,
                                                        'products':products,
                                                        'carousels':carousels,
                                                        'prices':prices,
                                                        'price_filter':price_filter,
                                                        }
                                                        )
    
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'product.html', {'product':product, 'cart_product_form': cart_product_form})



