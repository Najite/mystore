from django.forms import SlugField
from django.urls import reverse
from django.db import models


class Product_Tag(models.Model):
    product_tag = (
        ('best seller', 'best seller',
         'new', 'new',
         'old', 'old')
    )
    name = models.CharField(max_length=13)
    
    def __str__(self):
        return self.name
    
    

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=12, db_index=True)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(upload_to='media/category', blank=True, null=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])
  
    
class Carousel(models.Model):
    name = models.CharField(max_length=13)
    image = models.ImageField(upload_to='media/banner')
    slug = models.SlugField(null=False, unique=True)
    
    def __str__(self):
        return self.name
    

class Price_filter(models.Model):
    price_filter = (
        ('100 - 1000', '100.00 - 1000'),
        ('1000 - 5000', '1000 - 5000'),
        ('5000 - 10000', '5000 - 10000'),
        ('10000 - 20000', '10000 - 20000'),
        ('20000 - 50000', '20000 - 50000'),
    )
    slug = models.SlugField(unique=True, null=False)
    price = models.CharField(choices=price_filter, max_length=13)
    
    def __str__(self):
        return self.price
    
    def get_absolute_url(self):
        return reverse("store:product_price_filter", args=[self.slug])
    

    
    
    
# create products
class Product(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(default='lets make a description right here. You cant get a better product than what we have here', null=True,
                                    blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_filter = models.ForeignKey(Price_filter, on_delete=models.CASCADE, blank=True, max_length=13)
    available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/product')
    add_to_carousel = models.ForeignKey(Carousel, related_name='carousels', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, null=False)
    
    class Meta:
        ordering = ['-created']
        index_together = (('id', 'slug'),)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])


    
