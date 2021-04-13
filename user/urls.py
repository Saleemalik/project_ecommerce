from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name= 'login'),
    path('loginByotp/', views.loginByotp, name= 'loginByotp'),
    path('otp_login/', views.otpLogin, name= 'otp_login'),
    path('signup/', views.signup, name='signup'),
    path('refferal_signup/<int:idk>', views.referalSignup, name='refferal'),
    path('logout/', views.logout, name='logout'),
    path('userProfile/', views.userProfile, name='userProfile'),
    path('add_Prof_pic/', views.addProfpic, name='addProfPic'),
    path('profEdit/', views.profEdit, name='profEdit'),
    path('orderHistory/', views.orderHistory, name='orderHistory'),
    path('coupons/', views.coupons, name='coupons'),
    path('changePassword/',views.changePassword, name='changePassword'),
    path('cart/', views.cart, name='cart'),
    path('delete_cart/<int:idk>', views.deleteCart, name='delete_cart'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('change/<int:idk>', views.change, name='change'),
    path('category/<int:idk>', views.category, name='category'),
    path('product/<int:idk>', views.product, name='product'),
    path('discount/', views.discount, name='discount'),
    path('checkout/', views.checkout, name='checkout'),
    path('delete/<int:idk>', views.delete, name='delete'),
    path('payment/', views.payment, name='payment'),
    path('razorpay/', views.razorpay1, name='razorpay'),
    path('success/', views.success, name='success'),
    path('search/', views.search, name='search')
    
]
