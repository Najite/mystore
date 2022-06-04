from django.contrib import admin
from.models import Product, Category, Carousel, Price_filter

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =['name']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','created', 'updated', 'slug', 'category', 
                    'available']
    list_filter = ['price', 'created','updated']
    prepopulated_fields = {'slug':('name',)}
    
@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug':('name',)}
    

@admin.register(Price_filter)
class Price_filterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('price',)}
    