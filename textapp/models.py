from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username if self.user else "Unnamed Profile"
    
class Categories(models.Model):
    CategoryName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.CategoryName
    
class Brands(models.Model):
    Name = models.CharField(max_length=100,default="")   
    
    def __str__(self):
        return self.Name

class Product(models.Model):
    ProductName = models.CharField(max_length=100,default="")
    Brand = models.ForeignKey(Brands,on_delete=models.CASCADE , null=True,blank=True ,related_name='brand_products')
    Model = models.CharField(max_length=100,default="")
    Meterial = models.CharField(max_length=100,default="")
    Subtitle = models.CharField(max_length=100,default="")
    About = models.TextField(default="")
    AvailableQuantity = models.IntegerField(default=1)
    ProductCategory = models.CharField(max_length=100,default="")
    Image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Sidebarimage = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Sidebarimage2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Sidebarimage3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Description = models.TextField(default="")
    Price = models.DecimalField(max_digits=10, decimal_places=2,default="")
    OfferPrice = models.DecimalField(max_digits=10, decimal_places=2,default="")
    DealCategory = models.ForeignKey(Categories,on_delete=models.CASCADE , null=True,blank=True , related_name='category_products')
    StockStatus = models.CharField(max_length=100,default="Available")
    
    def get_sidebar_images(self):
        return list(filter(None, [self.Image,self.Sidebarimage, self.Sidebarimage2, self.Sidebarimage3]))

    def save(self,*args,**kwargs):
        if self.AvailableQuantity < 1 :
            self.StockStatus = "Out of stock"
        elif self.AvailableQuantity < 5 :
            self.StockStatus = "Low quantity" 
        else:
            self.StockStatus = "Available"  
        super().save(*args, **kwargs)     
    def __str__(self):
        return self.ProductName

class Titlepage(models.Model):
    Logo = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Title = models.CharField(max_length=150 , null=True)
    
    Image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Description = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.Title

class Subtitles(models.Model):
    Image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Description = models.TextField()

    def __str__(self):
        return self.Description
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.Price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_items = models.CharField(max_length=100, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    date = models.DateTimeField(auto_created=True,auto_now_add=True,blank=True, null=True)   