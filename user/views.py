import re

from django.core.exceptions import FieldDoesNotExist
from admin1.views import products, viewOrder
from user.models import Address, Cart, CouponUse, Orders, RefferalCoupon, UserPhone, ViewOrder
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http.response import JsonResponse
from admin1.models import Categories, Coupons, Products
from django.contrib.auth.hashers import check_password
import json
import razorpay
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import random, string
import base64
from django.core.files.base import ContentFile
from twilio.rest import Client 
from django.core.cache import cache
from datetime import date, datetime, timedelta, timezone
# from django.core.exceptions import doe
# from admin1.models import FieldDoesNotExist
import socket


# Create your views here.
def home(request):
    catgrs = Categories.objects.all()
    prods = Products.objects.all()
    for category in catgrs:
        if category.categoryOffer:
            discount = category.categoryDiscount
            products_ = Products.objects.filter(category=category.id)
            for product in products_:
                product.offered_price = product.price - product.price * float(discount) / 100
                product.save()
    totalItem = 0
    if request.user.is_authenticated:
        customer = request.user.id
        userId = UserPhone.objects.get(id=customer)
        cartOrders = Cart.objects.filter(user=userId)
        totalItem = 0
        for item in cartOrders:
            totalItem += item.quantity
    context = {
        'catgrs': catgrs,
        'prods': prods,
        'totalItem': totalItem
    }
    return render(request, 'home.html', context)


def login(request):
    catgrs = Categories.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return JsonResponse('true', safe=False)

        else:
            if User.objects.filter(username=username).exists():
                userB = User.objects.get(username=username)
                if userB.is_active == True:
                    print('no')
                    return JsonResponse('false1', safe=False)
                else:
                    return JsonResponse('false2', safe=False)
            else:
                return JsonResponse('false1', safe=False)
    else:
        return render(request, 'login.html', {'catgrs': catgrs})

def loginByotp(request):
    if request.method == 'POST':
        mobileNo = request.POST['mobileNo']

        if UserPhone.objects.filter(phone=mobileNo).exists():
            request.session['phone'] = mobileNo
            global otp
            otp = random.randint(1000, 9999)
            account_sid = 'ACbf923ac299325fcb9f548068f60f9838'
            token = 'df141e5a73a69700a5c436733d44478e'
            client = Client(account_sid, token)
            message = client.messages.create(
                body = f"your otp is {otp}",
                from_ = '+14243535184',
                to = f'+917736666049'
            )
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false', safe=False)
    else:
        return redirect('login')
    

def otpLogin(request):
    if request.method == 'POST':
        otp_num = request.POST['otp']
        number = request.session['phone']
        get_user = UserPhone.objects.get(phone=number)
        user = User.objects.get(id=get_user.id)
        
        global otp
        if otp == int(otp_num):
            auth.login(request, user)
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false', safe=False)
    else:
        catgrs = Categories.objects.all()
        return render(request, 'user_side/otp_login/otp_login.html', {'catgrs':catgrs})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return JsonResponse('false1', safe=False)
            elif User.objects.filter(email=email).exists():
                return JsonResponse('false2', safe=False)
            elif UserPhone.objects.filter(phone=phone).exists():
                return JsonResponse('false4', safe=False)
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()

                userP = UserPhone(id=None, phone=phone, details=user)
                userP.save()

                auth.login(request, user)
        else:
            return JsonResponse('false3', safe=False)

        return JsonResponse('true', safe=False)
    else:
        return redirect('login')

def referalSignup(request, idk):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                # print('usrname taken')
                return JsonResponse('false1', safe=False)
            elif User.objects.filter(email=email).exists():
                # print('email already taken')
                return JsonResponse('false2', safe=False)
            elif UserPhone.objects.filter(phone=phone).exists():
                # print('Phone number already taken')
                return JsonResponse('false4', safe=False)
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()

                userNew = UserPhone(id=None, phone=phone, details=user)
                userNew.save()

                userRefer = UserPhone.objects.get(id=idk)
                couponCodeR = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
                userCouponR = RefferalCoupon.objects.create(userK=userRefer, couponName='refferal Coupon "25%" off)', couponCode=couponCodeR, discount=25)
                userCouponR.save()

                couponCodeN = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
                userCouponN = RefferalCoupon.objects.create(userK=userNew, couponName='refferal Coupon "18%" off', couponCode=couponCodeN, discount=18)
                userCouponN.save()

                auth.login(request, user)
        else:
            return JsonResponse('false3', safe=False)

        return JsonResponse('true', safe=False)
    else:
        # print('host:')
        # host = request.get_host()
    
        refUser = UserPhone.objects.get(details__id=idk)
        catgrs = Categories.objects.all()
        context = {
            'catgrs':catgrs,
            'refUser':refUser
        }
        return render(request, 'user_side/base/referal_signup.html', context)


def userProfile(request):
    if request.user.is_authenticated:
        user = request.user.id

        address = Address.objects.filter(user=user)
        if address != '':
            adresFst = Address.objects.filter(user=user).first()
        else:
            adresFst = 'add address'
        cartOrders = Cart.objects.filter(user=user)
        totalItem = 0
        for item in cartOrders:
            totalItem += item.quantity
        userPr = UserPhone.objects.get(id=user)
        host = request.get_host()
        context = {
            'address': address,
            'userPr': userPr,
            'adresFst': adresFst,
            'totalItem': totalItem,
            'host':host
        }
        return render(request, 'user_side/user_profile.html', context)
    else:
        return redirect('login')

def addProfpic(request):
    if request.method == 'POST':
        userId = request.user.id
        userP = UserPhone.objects.get(id=userId)
        userName = userP.details.username
        imgProf = request.POST['imgProf']
        format, imgstr = imgProf.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=userName+ '.' + ext)

        userP.profile_pic = data
        userP.save()
        
        
        return JsonResponse('true', safe=False)


def profEdit(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        gender = request.POST['gender']
        age = request.POST['age']
        address = request.POST['address']
        
        email = request.POST['email']
        phone = request.POST['phone']
        userId = request.user.id
        profile = UserPhone.objects.get(id=userId)
        prof = User.objects.get(id=userId)
        adres = Address.objects.filter(user=userId).first()
        adres.address = address
        adres.save()
        
        prof.username = Name
        profile.gender = gender
        profile.age = age
        prof.email = email
        profile.phone = phone
        profile.save()
        prof.save()
        return JsonResponse('true', safe=False)
    else:
        return redirect('userProfile')


def orderHistory(request):
    userId = request.user.id
    userId = UserPhone.objects.get(id=userId)
    orders = Orders.objects.filter(userId=userId)
    cartOrders = Cart.objects.filter(user=userId)
    totalItem = 0
    for item in cartOrders:
        totalItem += item.quantity
    
    products = []
    for order in orders:
        orderId = order.id
        orderId = Orders.objects.get(id=orderId)
        prods = ViewOrder.objects.filter(orderId=orderId)
        for prod in prods:
            products.append(prod)
    context = {
        'products': products,
        'totalItem':totalItem
    }

    return render(request, 'user_side/user_profile/order_history.html', context)

def coupons(request):
    time_threshold = datetime.now()
    print(time_threshold)
    user = request.user.id
    userId = UserPhone.objects.get(id=user)
    cartOrders = Cart.objects.filter(user=userId)
    totalItem = 0
    for item in cartOrders:
        totalItem += item.quantity
    adminCoupons = Coupons.objects.filter(active=True, validTo__gte=time_threshold)
    referralCoupons = RefferalCoupon.objects.filter(userK=userId)
    coupons = []
    if referralCoupons !='':
        for coupon in referralCoupons:
            coupons.append(coupon)
    if adminCoupons != '':
        for coupon in adminCoupons:
            coupons.append(coupon)

    unusedCoupons = []
    for coupon in coupons:
        couponCode = coupon.couponCode
        if CouponUse.objects.filter(couponCode=couponCode, userId=userId).exists():
            continue
        else:
            unusedCoupons.append(coupon)
    
    context = {
        'unusedCoupons':unusedCoupons,
        'totalItem':totalItem
    }
    return render(request, 'user_side/user_profile/coupons.html', context)

def changePassword(request):
    if request.method == 'POST':
        customer = request.user.id
        current_password = request.user.password
        oldpassword = request.POST['oldPassword']
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']
        customer = User.objects.get(id=customer)
        if check_password(oldpassword, current_password) == False:
            return JsonResponse('false1', safe=False)
        elif newPassword == confirmPassword:
            if newPassword == '' or confirmPassword == '':
                return JsonResponse('false2', safe=False)
            else:
                customer.set_password(confirmPassword)
                customer.save()
                return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false3', safe=False)


def cart(request):
    if request.user.is_active:
        catgrs = Categories.objects.all()
        customer = request.user.id
        user = UserPhone.objects.get(id=customer)
        cartOrders = Cart.objects.filter(user=user)
        totalItem = 0
        for item in cartOrders:
            totalItem += item.quantity
        totalproducts = Cart.objects.filter(user=user).count()
        
        gr_total = 0
        for order in cartOrders:
            if order.product.category.categoryOffer:
                x = order.quantity * order.product.offered_price
            else:
                x = order.quantity * order.product.price
            gr_total += x
        
        gr_total = "{0:.2f}".format(gr_total)
        grandTotal = float(gr_total) + 50
        grandTotal = "{0:.2f}".format(grandTotal)
        obj = {'catgrs': catgrs, 'cartOrders': cartOrders, 'totalItem': totalItem, 'gr_total': gr_total,
                'totalproducts':totalproducts,
               'grandTotal': grandTotal}
        return render(request, 'user_side/cart.html', obj)
    else:
        catgrs = Categories.objects.all()
        obj = {'catgrs': catgrs}
        return render(request, 'home.html', obj)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']


    customer = request.user.id
    user = UserPhone.objects.get(id=customer)
    product = Products.objects.get(id=productId)
    order, created = Cart.objects.get_or_create(user=user, product=product)

    if action == 'add':
        order.quantity = (order.quantity + 1)
    elif action == 'remove':
        order.quantity = (order.quantity - 1)
    order.save()
    if order.quantity <= 0:
        order.delete()

    return JsonResponse('item was added', safe=False)


def change(request, idk):
    if request.method == 'GET':
        qty = request.GET['qty']
        cartId = Cart.objects.get(id=idk)
        cartId.quantity = qty
        cartId.save()
        if int(cartId.quantity) <= 0:
            return JsonResponse('false', safe=False)
        
        return JsonResponse('true', safe=False)

def deleteCart(request, idk):
    if request.user.is_active:
        cart = Cart.objects.get(id=idk)
        cart.delete()
        return JsonResponse('true', safe=False)
    else:
        return redirect('home')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')


def category(request, idk):
    user = request.user.id
    catgrs = Categories.objects.all()
    catgry = Categories.objects.get(id=idk)
    prods = Products.objects.all()
    cartOrders = Cart.objects.filter(user=user)
    totalItem = 0
    for item in cartOrders:
        totalItem += item.quantity
    catObj = {'catgry': catgry, 'catgrs': catgrs, 'prods': prods, 'totalItem': totalItem}
    return render(request, 'user_side/category.html', catObj)


def product(request, idk):
    user = request.user.id
    catgrs = Categories.objects.all()
    prodt = Products.objects.get(id=idk)
    cartOrders = Cart.objects.filter(user=user)
    totalItem = 0
    for item in cartOrders:
        totalItem += item.quantity
    prodObj = {'prodt': prodt, 'catgrs': catgrs, 'totalItem': totalItem}
    return render(request, 'user_side/product.html', prodObj)


def discount(request):
    if request.method == 'POST':
        # userId = user1.id 
        time_threshold = datetime.now()
        discountCode = request.POST['discountCode']
        print(discountCode)
        if discountCode !='':
            try:
                user = request.user.id
                user1 = UserPhone.objects.get(id=user)
                coupon = Coupons.objects.get(couponCode=discountCode, active=True, validTo__gte=time_threshold)
                if CouponUse.objects.filter(couponCode=discountCode, userId=user1).exists():
                    return JsonResponse('used', safe=False)
                else:
                    request.session['code'] = discountCode
                    discounts = coupon.discount

            except Coupons.DoesNotExist:
                try:
                    coupon = RefferalCoupon.objects.get(couponCode=discountCode, active=True)
                    if CouponUse.objects.filter(couponCode=discountCode, userId=user1).exists():
                        return JsonResponse('used', safe=False)
                    else:
                        request.session['code'] = discountCode
                        discounts = coupon.discount
                except RefferalCoupon.DoesNotExist:
                    return JsonResponse('false', safe=False)
                    
            request.session['discounts'] = discounts
        else:
            request.session['code'] = discountCode
            discounts = 0
            request.session['discounts'] = discounts 
        
        return JsonResponse('true', safe=False)
    else:
        return redirect('cart')

def checkout(request):
    if request.method == 'POST':
        user = request.user.id

        shipName = request.POST['shipName']
        address = request.POST['address']
        landMark = request.POST['landMark']
        phone = request.POST['phone']
        pincode = request.POST['pincode']
        userId = User.objects.get(id=user)
        newAddress = Address.objects.create(user=userId, shipName=shipName, address=address, landMark=landMark,
                                            phoneNo=phone, pincode=pincode)
        newAddress.save()
        return JsonResponse('true', safe=False)
    else:
        user = request.user.id
        address = Address.objects.filter(user=user)
        products = Cart.objects.filter(user=user)
        gr_total = 0
        for order in products:
            if order.product.category.categoryOffer:
                x = order.quantity * order.product.offered_price
            else:
                x = order.quantity * order.product.price
            gr_total += x
        gr_total = "{0:.2f}".format(gr_total)
        grandTotal = float(gr_total) + 50
        
        couponDiscount = request.session['discounts']
        if couponDiscount != 0:
            grandTotal = grandTotal - (grandTotal * int(couponDiscount)/100)
            
        grandTotal = "{0:.2f}".format(grandTotal)
        context = {'address': address, 'products': products, 'gr_total': gr_total, 'grandTotal': grandTotal, 'couponDiscount':couponDiscount}
        return render(request, 'user_side/checkout.html', context)


def delete(request, idk):
    if request.user.is_active:
        address = Address.objects.get(id=idk)
        address.delete()
        return JsonResponse('true', safe=False)
    else:
        return redirect('home')


def payment(request):
    if request.method == 'POST':
        addId = request.POST['address']

        gateway = request.POST['gateway']
        amount = request.POST['amount']
        request.session['amount'] = amount
        request.session['addId'] = addId
        request.session['gateway'] = gateway

        if gateway == 'cod':
            return JsonResponse('false', safe=False)
        # return render(request, 'user_side/payment.html')
        return JsonResponse('true', safe=False)
    else:
        amount = request.session['amount']
        addId = request.session['addId']
        gateway = request.session['gateway']
        amountUsd = ('{:.2f}'.format(float(amount) / 72))
        paisa = float(amount) / 100

        context = {
            'amountUsd': amountUsd,
            'amount': amount,
            'addId': addId,
            'gateway': gateway
        }
        if gateway == 'paypal':
            return render(request, 'user_side/payment/paypal.html', context)
        elif gateway == 'razorpay':
            return redirect('razorpay')


def razorpay1(request):
    amount = request.session['amount']
    paisa = float(amount) * 100
    if request.method == 'POST':
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_BxzCGCso9MsXoi', 'rp5tFJd7Y8iEYuzHoieESrjg'))
        payment = client.order.create({'amount': paisa, 'currency': 'INR', 'payment_capture': '1'})
    context = {
        'amount': amount,
        'paisa': paisa
    }
    return render(request, 'user_side/payment/razorpay.html', context)


@csrf_exempt
def success(request):
    userId = request.user.id
    amount = request.session['amount']
    amount = ('{:.0f}'.format(float(amount)))
    
    couponCode = request.session['code']
    # amount = int(amount)
    userId = UserPhone.objects.get(details=userId)
    gateway = request.session['gateway']
    addId = request.session['addId']
    addId = Address.objects.get(id=addId)
    address = addId.address
    shipName = addId.shipName
    pincode = addId.pincode
    altPhone = addId.phoneNo
    landMark = addId.landMark

    productIds = Cart.objects.filter(user=userId)
    if Cart.objects.filter(user=userId).exists():
        if gateway == 'cod':
            userOrder = Orders.objects.create(userId=userId, amount=amount, address=address, shipName=shipName,
                                            pincode=pincode, transactionDetails='COD', phoneNo=altPhone, landMark=landMark)
            userOrder.save()
            couponUsed = CouponUse.objects.get_or_create(userId=userId, couponCode=couponCode)
            try:
                couponUsed.save()
            except AttributeError:
                pass
        else:
            userOrder = Orders.objects.create(userId=userId, amount=amount, complete=True, address=address,
                                            shipName=shipName, transactionDetails='UPI', pincode=pincode, phoneNo=altPhone, landMark=landMark)
            userOrder.save()

            couponUsed = CouponUse.objects.get_or_create(userId=userId, couponCode=couponCode)
            try:
                couponUsed.save()
            except AttributeError:
                pass
            
        for product in productIds:
            productName = product.product.productName
            qty = product.quantity
            price = product.product.price
            total = product.get_total
            orderProd = ViewOrder.objects.create(orderId=userOrder, productName=productName, quantity=qty, price=price,
                                                total=total)
            orderProd.save()

        productIds.delete()
    context = {
        'gateway': gateway,
    }
    return render(request, 'user_side/payment/success.html', context)

def search(request):
    catgrs = Categories.objects.all()
    if 'Product' in request.GET:
        search_item = request.GET['Product']
        item = Products.objects.filter(productName__icontains=search_item)     
        searchItem = search_item
        context = {
        'catgrs':catgrs,
        'item':item,
        'searchItem':searchItem 
        }
        return render(request, 'user_side/base/search.html', context)
    else:
        return redirect('/')

    
