from django.http import HttpResponse
import environ
from django.urls import reverse


from order.tasks import order_created
from.models import OrderItem, Order
from.forms import OrderCreationForm
from cart.cart import Cart
import requests
import math
import random
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from rave_python import Rave, RaveExceptions, Misc
import os
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json



env = environ.Env()
environ.Env.read_env()



'FLWSECK_TEST-0ab780a5f4b1a4f8bb3c6daaed89255b-X'

rave = (Rave(os.getenv('RAVE_PUBLIC_KEY'), os.getenv('RAVE_SECRET_KEY')))

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method =='POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)            
            name = obj.first_name + '' + obj.last_name
            email = obj.email
            phonenumber = obj.phone
            
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                        )
                
            cart.clear()
            #launch asynchronous task
            order_created.delay(order.id)  
            
            # save the order
            request.session['order_id'] = order.id
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order,id=order_id)
            total_cost = order.get_total_price()
            auth_token = env('RAVE_SECRET_KEY')
            hed = {'Authorization': 'Bearer ' + auth_token}
            data = {
                'tx_ref':'' +str(math.floor(10000 +random.random() * 800000)),
                'amount':f'{total_cost}',
                'currency':'NGN',
                'redirect_url':'http://127.0.0.1:8000/callback',
                'payment_options':'card',
                'customer':{
                    'email':email,
                    'phoneumber':phonenumber,
                    'name':name
                }
            }
    
    
    
            url = 'https://api.flutterwave.com/v3/payments'
            response = requests.post(url,json=data,headers=hed)
            response=response.json()
            link=response['data']['link']
            response = requests.post('https://webhook.flutterwave.com/1l6lz5w1')
            print(response.status_code)
            
            
            
            return redirect(link)        
            
    
        
    else:
        form = OrderCreationForm()
    return render(request, 'order.html', {'form':form, 'cart':cart})


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def webhook(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    secret_hash = env('secret_hash')
    signature = request.headers.get('verifi-hash')
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    
    
    if  status == 'successful':
        order.paid =True
        order.save()
        return HttpResponse(status=200)
    
    
    
    else:
        return HttpResponse('payment was cancelled')
    
    
    if signature == None or (signature != secret_hash):
        return HttpResponse(status=401)
    
    print(status)
    print(tx_ref)
   
    
   
    
    