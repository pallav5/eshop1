from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

from .utils import unique_slug_generator,slugify,random_string_generator
# Create your models here.


class TimeStamp(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)
    def __str__(self):
        return self.full_name





class ProductCategory(TimeStamp):
    slug =models.SlugField(unique=True, null=True, editable=False, blank=True,max_length=100)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="productcategory", null=True, blank=True)

    def __str__(self):
        return self.title

class Color(TimeStamp):
    title = models.CharField(max_length=200)
    hex_code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


SIZE = (
    (None, "Select Standard"),
    ("Int", "Int"),
    ("EU", "EU"),
)

MAIN_CATEGORY = (
     ("Kid's Wear", "Kid's Wear"),
     ("Men's Wear", "Men's Wear"),
     ("Women's Wear", "Women's Wear"),
     ("Others", "Others"),
)


class Size(TimeStamp):
    standard = models.CharField(max_length=200, choices=SIZE)
    title = models.CharField(max_length=200)
    shortname = models.CharField(max_length=10,default='none')
    class Meta:
        unique_together = ('standard', 'title')

    def __str__(self):
        return   self.title


# class Tag(TimeStamp):
#     title = models.CharField(max_length=200)

#     def __str__(self):
#         return self.title




class ProductBrand(TimeStamp):
    
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(
        upload_to="productbrands", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    

class ProductRemark(TimeStamp):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title



class Product(TimeStamp):
    slug =models.SlugField(unique=True, null=True, editable=False, blank=True,max_length=100)
    title = models.CharField(max_length=200)
    product_id = models.CharField(
    max_length=200, unique=True, null=True, blank=True)
    main_category = models.CharField(default=MAIN_CATEGORY[1][1] ,max_length=200, choices=MAIN_CATEGORY)
    category = models.ManyToManyField(ProductCategory)
    instock = models.PositiveIntegerField(default=0)
    color = models.ManyToManyField(
        Color,  null=True, blank=True)
    size = models.ManyToManyField( 
        Size,  null=True, blank=True)
    marked_price = models.IntegerField(max_length=19)
    selling_price = models.IntegerField(max_length=19,  null=True, blank=True)
    discount_pct = models.PositiveIntegerField(default=0)

    # tags = models.ManyToManyField(Tag)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    # status = models.CharField(
    #     max_length=100, choices=PRODUCT_STATUS, default="Pending")
    # remarks = models.CharField(max_length=200, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    # sale_count = models.PositiveIntegerField(default=0)
    # weight and volumes
    views = models.PositiveIntegerField(default=0)
    length = models.TextField( null=True, blank=True)
    width = models.TextField( null=True, blank=True)
    height = models.TextField( null=True, blank=True)
    weight = models.TextField(  null=True, blank=True)
    return_policy = models.TextField(max_length=1024, null=True, blank=True)
    image1 = models.ImageField(upload_to="products/images/",default='')
    image2 = models.ImageField(upload_to="products/images/",default='')
    image3 = models.ImageField(upload_to="products/images/",null=True,blank=True)
    image4 = models.ImageField(upload_to="products/images/",null=True, blank=True)
    image5 = models.ImageField(upload_to="products/images/",null=True, blank=True)
    def __str__(self):
        return self.title
    

class ProductSizeStock(TimeStamp):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    instock = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product.title
        


# class ProductImage(TimeStamp):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="products/images/")
#     featured_image = models.BooleanField(default=False, null=True, blank=True)



#     def __str__(self):
#         return self.product.title


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    size = models.ManyToManyField( 
        Size,  null=True, blank=True)
    color = models.CharField(max_length=200, null=True, blank=True, default=None) 

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)



class Order(TimeStamp):
    
    slug =models.SlugField(unique=True, null=True, editable=False, blank=True,max_length=100)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, default='1')
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS,default=ORDER_STATUS[1][1])
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_charge = models.PositiveIntegerField(
        default=50, null=True, blank=True)

    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)
    


class Slider(TimeStamp):
    title = models.CharField(max_length=200)
    image1 = models.ImageField(upload_to="sliders")
    image2 = models.ImageField(upload_to="sliders")
    image3 = models.ImageField(upload_to="sliders")
    

    def __str__(self):
        return self.title


class Organization(TimeStamp):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='organization')
    address = models.CharField(max_length=500)
    introduction = models.TextField()
    profile_image = models.ImageField(upload_to='organization',null=True, blank=True)
    contact_no = models.CharField(max_length=200)
    alt_contact_no = models.CharField(max_length=200, null=True, blank=True)
    map_location = models.CharField(max_length=2000, null=True, blank=True)
    email = models.EmailField()
    alt_email = models.EmailField(null=True, blank=True)
    slogan = models.CharField(max_length=500, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)
    
    terms_and_conditions = models.TextField(null=True, blank=True)
    

    
    def __str__(self):
        return self.name





ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)



class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)



def all_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(all_pre_save, sender=Product)
pre_save.connect(all_pre_save, sender=ProductCategory)
