
from django.core import validators
from django.db.models.fields import BooleanField
# from django.contrib.auth.models import User
# from user.models import UserPhone
# from admin1.views import products
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import activate

# Create your models here.

class Categories(models.Model):
    categoryName = models.CharField(max_length=100)
    categoryPic = models.ImageField(upload_to='pics')
    categoryOffer = models.BooleanField(default=False)
    categoryDiscount = models.FloatField(default=0)
    advertisement = models.CharField(max_length=200 , default="Best Deals For this category")

    @property
    def imageurl(self):
        try:
            img = self.categoryPic.url
        except:
            img = ''
        return img

class Products(models.Model):

    productName = models.CharField(max_length=100)
    productImg1 = models.ImageField(upload_to='img')
    productImg2 = models.ImageField(upload_to='img')
    productImg3 = models.ImageField(upload_to='img')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.FloatField()
    offered_price = models.FloatField(default= 0)
    quantity = models.IntegerField()
    description = models.TextField()

    @property
    def imgurl1(self):
        try:
            img = self.productImg1.url
        except:
            img = ''
        return img
    
    @property
    def imgurl2(self):
        try:
            img = self.productImg2.url
        except:
            img = ''
        return img
    
    @property
    def imgurl3(self):
        try:
            img = self.productImg3.url
        except:
            img = ''
        return img



class Coupons(models.Model):

    couponName = models.CharField(max_length=100)
    couponCode = models.CharField(max_length=50, unique=True)
    validFrom = models.DateTimeField()
    validTo = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=False)