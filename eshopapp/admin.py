from django.contrib import admin
from .models import *
# Register your models here
admin.site.register([Admin,Customer, ProductCategory, Color, Size, ProductBrand, ProductRemark, Product,  Order, Slider,Cart,CartProduct])