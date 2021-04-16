import json
from typing import DefaultDict
from django.core.checks import messages
from django.db.models.deletion import SET_NULL
from django.db.models.fields import DateField
# from django.http import request
from admin1.models import Categories, Coupons, Products
from user.models import Orders, UserPhone, ViewOrder
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth.models import User, auth
from django.core.files import File
import base64
from django.core.files.base import ContentFile
from datetime import date, datetime, timedelta, timezone
from django.core import serializers
from django.core.cache import cache
import string, random
from django.core.exceptions import ValidationError


# Create your views here.

def Alogin(request):
    if request.session.has_key("key"):
        return redirect('adminD')
    else:
        return render(request, 'Alogin.html')


def loginD(request):
    if request.session.has_key("key"):
        return redirect('adminD')
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        if name == "admin" and password == '1234':
            request.session['key'] = 'check'
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false', safe=False)
    else:
        return render(request, 'Alogin.html')


def adminD(request):
    if request.session.has_key("key"):
        orderIds = Orders.objects.filter(delevered=True)

        totUsers = User.objects.all().count()
        totProducts = Products.objects.all().count()
        compltdOrder = Orders.objects.filter(complete=True)
        totRevenue = 0
        for order in compltdOrder:
            orderId = order.id
            prods = ViewOrder.objects.filter(orderId=orderId)
            gr_total = 0
            for product in prods:
                gr_total += product.total
            totRevenue += gr_total + 50

        producs = Products.objects.all()
        
        name_array = []
        name_arrays = []
        for prod in producs:
            pro_name = prod.productName
            pro_price = prod.price
            viewOrders_ofThis_prod = ViewOrder.objects.filter(productName=pro_name)
            tot_quantity_sold = 0
            tot_amount_fromThis = 0

            for viewOrder in viewOrders_ofThis_prod:
                quantity = viewOrder.quantity
                tot_quantity_sold += int(quantity)
                tot_amount_fromThis += int(viewOrder.total)
            
            name_array = [pro_name, tot_quantity_sold, pro_price, tot_amount_fromThis]
            name_arrays.append(name_array)

        prSold = []
        for orderId in orderIds:
            prods = ViewOrder.objects.filter(orderId=orderId)
            for prod in prods:
                prSold.append(prod)

        today = date.today()
        completed_delivers_month = Orders.objects.filter(complete=True, transactionDetails='COD',
                                                         date_delivered__month=today.month)
        completed_orders_month = Orders.objects.filter(complete=True, transactionDetails='UPI',
                                                       dateOrdered__month=today.month)

        monthlyOrders = []
        for order in completed_delivers_month:
            monthlyOrders.append(order)
        for order in completed_orders_month:
            monthlyOrders.append(order)
        monthRevenue = 0
        for order in monthlyOrders:
            monthRevenue += order.amount

        completed_delivers_year = Orders.objects.filter(complete=True, transactionDetails='COD',
                                                        date_delivered__year=today.year)
        completed_orders_year = Orders.objects.filter(complete=True, transactionDetails='UPI',
                                                      dateOrdered__year=today.year)

        yearlyOrders = []
        for order in completed_delivers_year:
            yearlyOrders.append(order)
        for order in completed_orders_year:
            yearlyOrders.append(order)
        # print(yearlyOrders)
        yearRevenue = 0
        for order in yearlyOrders:
            yearRevenue += order.amount

        completed_delivers_today = Orders.objects.filter(complete=True, transactionDetails='COD',
                                                         date_delivered__day=today.day)
        completed_orders_today = Orders.objects.filter(complete=True, transactionDetails='UPI',
                                                       dateOrdered__day=today.day)

        todayOrders = []
        for order in completed_delivers_today:
            todayOrders.append(order)
        for order in completed_orders_today:
            todayOrders.append(order)

        todayRevenue = 0
        for order in todayOrders:
            todayRevenue += order.amount
        pending_orders = Orders.objects.filter(delevered=False).count()

        thisday = datetime.now() - timedelta(days=0)
        
        completed_orders = Orders.objects.filter(complete=True, date_delivered__day=thisday.day)
        
        revenueData = []
        itemSoldData = []
        thisdays = []
        for num in reversed(range(7)):
            thisday = datetime.now() - timedelta(days=num)
            completed_delivers_thisday = Orders.objects.filter(complete=True, transactionDetails='COD',
                                                               date_delivered__day=thisday.day)
            completed_orders_thisday = Orders.objects.filter(complete=True, transactionDetails='UPI',
                                                             dateOrdered__day=thisday.day)

            thisdayIncomeOrders = []
            for order in completed_delivers_thisday:
                thisdayIncomeOrders.append(order)
            for order in completed_orders_thisday:
                thisdayIncomeOrders.append(order)

            thisdayRevenue = 0
            thisdayProductSold = 0
            for order in thisdayIncomeOrders:
                orderId = order.id
                prods = ViewOrder.objects.filter(orderId=orderId)
                gr_total = 0
                item_sold = 0
                for product in prods:
                    gr_total += product.total
                    item_sold += product.quantity
                thisdayRevenue += order.amount
                thisdayProductSold += item_sold

            theday = thisday.date()
            thisdays.append(theday.strftime('%B %d'))
            revenueData.append(thisdayRevenue)
            itemSoldData.append(thisdayProductSold)

        context = {
            'prSold': prSold,
            'totUsers': totUsers,
            'totProducts': totProducts,
            'pending_orders': pending_orders,
            'totRevenue': totRevenue,
            'monthRevenue': monthRevenue,
            'yearRevenue': yearRevenue,
            'todayRevenue': todayRevenue,
            'revenueData': revenueData,
            'itemSoldData': itemSoldData,
            'thisdays': thisdays,
            'name_arrays': name_arrays,

        }
        return render(request, 'index2.html', context)
    else:
        return redirect('Alogin')


def logout(request):
    request.session.flush()
    return redirect('Alogin')


def products(request):
    if request.session.has_key("key"):
        catgrs = Categories.objects.all()

        prods = Products.objects.all()
        dicObj = {'prods': prods, 'catgrs': catgrs}
        return render(request, 'Admin_management/products/Products.html', dicObj)
    else:
        return redirect('Alogin')


def addProduct(request):
    catgrs = Categories.objects.all()
    if request.session.has_key("key"):
        if request.method == 'POST':
            nameP = request.POST['nameP']
            catName = request.POST['catName']
            img1 = request.POST['crop1']
            img2 = request.POST['crop2']
            img3 = request.POST['crop3']
            price = request.POST['price']
            desc = request.POST['desc']
            Qty = request.POST['Qty']
            format1, imgstr1 = img1.split(';base64,')
            format2, imgstr2 = img2.split(';base64,')
            format3, imgstr3 = img3.split(';base64,')
            ext1 = format1.split('/')[-1]
            ext2 = format2.split('/')[-1]
            ext3 = format3.split('/')[-1]
            data1 = ContentFile(base64.b64decode(imgstr1), name=nameP + '.' + ext1)
            data2 = ContentFile(base64.b64decode(imgstr2), name=nameP + '.' + ext2)
            data3 = ContentFile(base64.b64decode(imgstr3), name=nameP + '.' + ext3)
            if Products.objects.filter(productName=nameP):
                return JsonResponse('false1', safe=False)
            else:
                catgry = Categories.objects.get(categoryName=catName)

                addProd = Products.objects.create(productName=nameP, price=price, quantity=Qty, productImg1=data1,
                                                  productImg2=data2, productImg3=data3, category=catgry,
                                                  description=desc)
                addProd.save()
                return JsonResponse('true', safe=False)
        else:
            return render(request, 'Admin_management/products/add_product.html', {'catgrs': catgrs})
    else:
        return redirect('Alogin')


def editProd(request, idk):
    if request.session.has_key("key"):
        if request.method == 'POST':
            nameP = request.POST['nameP']
            catName = request.POST['catName']
            img1 = request.FILES.get('imgInp1')
            img2 = request.FILES.get('imgInp2')
            img3 = request.FILES.get('imgInp3')
            price = request.POST['price']
            desc = request.POST['desc']
            Qty = request.POST['Qty']
            if Products.objects.filter(productName=nameP).exclude(id=idk).exists():
                # messages.info(request, 'Username Taken')
                return JsonResponse('false1', safe=False)
            else:
                prod = Products.objects.get(id=idk)
                prod.productName = nameP
                prod.category.categoryName = catName
                prod.price = price
                prod.description = desc
                prod.quantity = Qty
                if img1 is not None:
                    prod.productImg1 = img1

                if img2 is not None:
                    prod.productImg2 = img2

                if img3 is not None:
                    prod.productImg3 = img3
                prod.save()
                return JsonResponse('true', safe=False)
        else:
            prodEdit = Products.objects.get(id=idk)
            catgrs = Categories.objects.all()
            return render(request, 'Admin_management/products/editProd.html', {'prodEdit': prodEdit, 'catgrs': catgrs})
    else:
        return redirect('Alogin')


def delProduct(request, idk):
    if request.session.has_key("key"):
        prod = Products.objects.get(id=idk)
        prod.delete()
        return redirect('products')
    else:
        return redirect('Alogin')


def categories(request):
    if request.session.has_key("key"):
        catgrs = Categories.objects.all()
        if request.session.has_key("key"):
            return render(request, 'Admin_management/categories/categories.html', {'catgrs': catgrs})
        else:
            return redirect('Alogin')
    else:
        return redirect('Alogin')


def addCategory(request):
    if request.session.has_key("key"):
        return render(request, 'Admin_management/categories/addCategory.html')
    else:
        return redirect('Alogin')


def catadd(request):
    if request.session.has_key("key"):
        if request.method == 'POST':
            catName = request.POST['names']
            img = request.POST['itemImgOutput']

            format, imgstr = img.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=catName + '.' + ext)

            if Categories.objects.filter(categoryName=catName).exists():
                messages.Info(request, 'category exists')
                # return redirect('addCategory')
                return JsonResponse('false1', safe=False)
            elif Categories.objects.filter(categoryPic=img).exists():
                messages.Info(request, 'choose another Pic')
                # return redirect('addCategory')
                return JsonResponse('false2', safe=False)
            else:
                addCat = Categories.objects.create(categoryName=catName, categoryPic=data)
                addCat.save()
                # return redirect('categories')
                return JsonResponse('true', safe=False)

        else:
            return redirect('addCategory')
    else:
        return redirect('Alogin')


def editCategory(request, idk):
    if request.session.has_key("key"):
        catEdit = Categories.objects.get(id=idk)
        return render(request, 'Admin_management/categories/editCategory.html', {'catEdit': catEdit})
    else:
        return redirect('Alogin')


def updateCategory(request, idk):
    if request.session.has_key("key"):
        if request.method == 'POST':
            catName = request.POST['names']
            img = request.FILES.get('inputGroupFile01')
            print(img)

            if Categories.objects.filter(categoryName=catName).exclude(id=idk).exists():
                # messages.info(request, 'Username Taken')
                print('username taken')
                return JsonResponse('false1', safe=False)
            else:
                cat = Categories.objects.get(id=idk)
                cat.categoryName = catName
                if img is not None:
                    cat.categoryPic = img
                cat.save()
                return JsonResponse('true', safe=False)
        else:
            return redirect('editCategory')
    else:
        return redirect('Alogin')


def deleteCat(request, idk):
    if request.session.has_key("key"):
        cat = Categories.objects.get(id=idk)
        cat.delete()
        return redirect('categories')
    else:
        return redirect('Alogin')


def addOffer(request, idk):
    if request.session.has_key("key"):
        if request.method == 'POST':
            discount = request.POST['discount']
            advertise = request.POST['advertise']

            category = Categories.objects.get(id=idk)
            category.categoryOffer = True
            category.categoryDiscount = discount
            category.advertisement = advertise
            category.save()

            products_ = Products.objects.filter(category=category.id)
            for product in products_:
                product.offered_price = product.price - product.price * float(discount) / 100
                product.save()

            return JsonResponse('true', safe=False)

        else:
            category = Categories.objects.get(id=idk)
            return render(request, 'Admin_management/categories/addOffer.html', {"category": category})
    else:
        return redirect('Alogin')


def removeOffer(request, idk):
    if request.session.has_key("key"):
        cat = Categories.objects.get(id=idk)
        cat.categoryOffer = False
        cat.save()
        return redirect('categories')
    else:
        return redirect('Alogin')


def addCoupon(request):
    if request.session.has_key("key"):
        if request.method == 'POST':
            couponName = request.POST['couponName']
            validFrom = request.POST['validFrom']
            validTo = request.POST['validTo']
            discount = request.POST['discount']
            couponCode = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            try:
                coupon = Coupons.objects.create(couponName=couponName, validFrom=validFrom, validTo=validTo,
                                                discount=discount, couponCode=couponCode)
            except ValidationError:
                return JsonResponse('false', safe=False)
            coupon.save()
            return JsonResponse('true', safe=False)
        else:
            return render(request, 'Admin_management/coupons/add_coupon.html')
    else:
        return redirect('Alogin')


def viewCoupons(request):
    if request.session.has_key("key"):
        coupons = Coupons.objects.all()
        context = {
            'coupons': coupons
        }
        return render(request, 'Admin_management/coupons/view_coupons.html', context)
    else:
        return redirect('Alogin')


def activeCoupons(request, idk):
    if request.session.has_key("key"):
        coupon = Coupons.objects.get(id=idk)
        if coupon.active:
            coupon.active = False
        else:
            coupon.active = True
        coupon.save()
        return redirect('viewCoupons')
    else:
        return redirect('Alogin')


def delcategories(request):
    if request.session.has_key("key"):
        return render(request, 'Admin_management/categories/delCategories.html')
    else:
        return redirect('Alogin')


def users(request):
    if request.session.has_key("key"):
        if 'search' in request.GET:
            search = request.GET['search']
            users = UserPhone.objects.filter(phone__icontains=search) or UserPhone.objects.filter(
                details__username__icontains=search)
        else:
            users = UserPhone.objects.all()
        if request.session.has_key("key"):
            return render(request, 'Admin_management/users/users.html', {'users': users})
    else:
        return redirect('Alogin')


def block(request, idk):
    if request.session.has_key("key"):
        user = User.objects.get(id=idk)
        if user.is_active == True:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('users')
    else:
        return redirect('Alogin')


def orders(request):
    if request.session.has_key("key"):
        orders = Orders.objects.all()
        context = {
            'orders': orders
        }
        return render(request, 'Admin_management/orders/orders.html', context)
    else:
        return redirect('Alogin')


def viewOrder(request, idk):
    if request.session.has_key("key"):
        orderId = Orders.objects.get(id=idk)
        products = ViewOrder.objects.filter(orderId=orderId)
        product_array = []
        product_arrays = []
        sub_total = 0
        for product in products:
            productName = product.productName
            product_get = Products.objects.get(productName=productName)
            offered_price = product_get.offered_price
            product_img = product_get.imgurl1
            product_array = [product, offered_price, product_img]
            product_arrays.append(product_array)

            sub_total += product.total

        total = sub_total + 50
        amount = orderId.amount

        print(product_arrays)
        context = {
            'products': products,
            'product_arrays': product_arrays,
            'sub_total': sub_total,
            'amount': amount
        }
        return render(request, 'Admin_management/orders/view_order.html', context)
    else:
        return redirect('Alogin')


def orderStatus(request, idk):
    if request.session.has_key("key"):
        orderId = Orders.objects.get(id=idk)
        if orderId.shipped:
            if orderId.delevered:
                orderId.complete = True

                orderId.save()
                return redirect('orders')
            else:
                orderId.delevered = True
                orderId.complete = True
                # now = datetime.now()
                orderId.date_delivered = datetime.now()
                orderId.save()
                return redirect('orders')
        else:
            orderId.shipped = True
            orderId.save()
            return redirect('orders')
    else:
        return redirect('Alogin')
    # if orderId.complete:
    #     orderId.transactionDetails = 'UPI'
    # else:
    #     orderId.transactionDetails = 'COD'
    # orderId.save()
    # return redirect('orders')


def reports(request):
    if request.session.has_key("key"):
        if request.method == 'POST':
            print('dsas')
            from_ = request.POST['from']
            to = request.POST['to']

            order_rows = Orders.objects.filter(dateOrdered__range=[from_, to])

            cache.set('order_rows', order_rows)
            # equipment = cache.get('order_rows')

            return JsonResponse('true', safe=False)
        else:
            order_rows = cache.get('order_rows')
            print(order_rows)
            if order_rows is None:
                order_rows = Orders.objects.all()
                print('dsdsd')
            cache.delete('order_rows')

            # print(order_rows)

            context = {
                'order_rows': order_rows
            }
            return render(request, 'Admin_management/reports/reports.html', context)
    else:
        return redirect('Alogin')


def reports2(request):
    if request.session.has_key("key"):
        if request.method == 'POST':
            date_ = request.POST['date']

            order_rows = Orders.objects.filter(dateOrdered__date=date_)
            print('asaq')
            print(order_rows)

            cache.set('order_rows', order_rows)
            # equipment = cache.get('order_rows')

            return JsonResponse('true', safe=False)
        else:
            return redirect('reports')
    else:
        return redirect('Alogin')
