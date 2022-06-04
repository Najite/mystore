from asyncio import log
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from order.models import Order
from rave_python import Rave
import math
import random
import requests
import environ
import os
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# from rest_framework

# Create your views here.

env = environ.Env()
environ.Env.read_env()

rave = rave = (Rave(os.getenv('RAVE_PUBLIC_KEY'), os.getenv('RAVE_SECRET_KEY')))


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    total_cost = order.get_total_price()
    auth_token = env('RAVE_SECRET_KEY')
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
        'tx_ref':'' +str(math.floor(10000 +random.random() * 800000)),
        'amount':f'{total_cost}',
        'currency':'NGN',
        'redirect_url':'http://127.0.0.1:8000',
        'payment_options':'card',
        'customer':{
            'email':request.POST.get('email'),
            'phoneumber':request.POST.get('phone'),
            'name':request.POST.get('name')
        }
    }
    
    
    
    url = 'https://api.flutterwave.com/v3/payments'
    response = requests.post(url,json=data,headers=hed)
    response=response.json()
    link=response['data']['link']
    return redirect(link)


def webhook(request):
    secret_hash = env('secret_hash')
    signature = request.headers.get('verifi-hash')
    if signature == None or (signature != secret_hash):
        return HttpResponse(status=401)
    payload = request.body
    log(payload)
    return HttpResponse(status=200)