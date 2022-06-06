from django.urls import path
from . import views

app_name='order'

urlpatterns = [
    path('', views.order_create, name='order_create'),
    path('callback/', views.webhook, name='callback'),
    
    
]
