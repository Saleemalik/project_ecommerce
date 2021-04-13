# from admin1.views import products
from datetime import timezone
from django.db.models.aggregates import Count
from django.db.models.base import Model
from django.http import request
from admin1.models import Coupons, Products
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import CharField
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class UserPhone(models.Model):
    phone = models.CharField(max_length=13)
    details = models.ForeignKey(User, on_delete=models.CASCADE)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'O', u'Others'),
        (u'U', u'Unspecified'),
    )
    age = models.IntegerField(blank=True, null=True, default=18)
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES, default='Male')
    address  = models.CharField(max_length=200, default='kohikode')
    profile_pic = models.ImageField(upload_to='user', blank=True, null=True )

    @property
    def imageurlProf(self):
        try:
            img = self.profile_pic.url
        except:
            img = ''
        return img


class Cart(models.Model):
    user = models.ForeignKey(UserPhone, on_delete= models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        if self.product.category.categoryOffer:
            total = self.product.offered_price * self.quantity
            total = "{0:.2f}".format(total)
        else:
            total = self.product.price * self.quantity
            total = "{0:.2f}".format(total)
        return total



class Address(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    shipName = models.CharField(max_length=50)
    address  = models.CharField(max_length=100)
    landMark = models.CharField(max_length=50)
    pincode = models.PositiveIntegerField()
    phoneNo = models.PositiveBigIntegerField()


class Orders(models.Model):
    userId = models.ForeignKey(UserPhone, on_delete=models.SET_NULL, null=True, blank=True)
    dateOrdered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    address = models.CharField(max_length=200, default='kozhikode')
    shipName = models.CharField(max_length=50, default='blank')
    address  = models.CharField(max_length=100, default='blank')
    landMark = models.CharField(max_length=50, default='blank')
    pincode = models.PositiveIntegerField(default=0)
    phoneNo = models.PositiveBigIntegerField(default=0)
    transactionDetails = models.CharField(max_length=200, null=True)
    amount = models.IntegerField(default=0)
    shipped = models.BooleanField(default=False)
    delevered = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    date_delivered = models.DateTimeField(auto_now=False, blank=True, null=True)



class ViewOrder(models.Model):
    orderId = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True, blank=True)
    productName = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    total = models.FloatField(default=0)


class CouponUse(models.Model):
    userId = models.ForeignKey(UserPhone, on_delete=models.SET_NULL, null=True, blank=True)
    couponCode = models.CharField(max_length=20)
    status = models.CharField(max_length=100, default='used')

class RefferalCoupon(models.Model):
    userK = models.ForeignKey(UserPhone, on_delete=models.SET_NULL, null=True, blank=True)
    couponName = models.CharField(max_length=100)
    couponCode = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True)

    


    




            