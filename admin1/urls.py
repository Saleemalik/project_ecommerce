from django.urls import path
from . import views

urlpatterns = [
    path('', views.Alogin, name='Alogin'),
    path('loginD/', views.loginD, name='loginD'),
    path('adminD/', views.adminD, name='adminD'),
    path('logout/', views.logout,name='logout'),
    path('products/', views.products, name='products'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('editProd/<int:idk>', views.editProd, name='editProd'),
    path('delProduct/<int:idk>', views.delProduct, name='delProducts'),
    path('categories/', views.categories, name='categories'),
    path('addCategory/',views.addCategory, name='addCategory'),
    path('catadd/', views.catadd, name='catadd'),
    path('editCategory/<int:idk>',views.editCategory, name='editCategory'),
    path('updateCategory/<int:idk>', views.updateCategory, name='updateCategory'),
    path('deleteCat/<int:idk>',views.deleteCat, name='deleteCat'),
    path('delCategories/',views.delcategories, name='delCategories'),
    path('add_offer/<int:idk>',views.addOffer, name='addOffer'),
    path('remove_offer/<int:idk>',views.removeOffer, name='removeOffer'),
    path('add_coupon/', views.addCoupon, name='addCoupon'),
    path('view_coupons/', views.viewCoupons, name='viewCoupons'),
    path('active_coupons/<int:idk>', views.activeCoupons, name='activeCoupons'),
    path('users/', views.users, name='users'),
    path('block/<int:idk>', views.block, name= 'block'),
    path('orders/', views.orders, name= 'orders'),
    path('viewOrder/<int:idk>', views.viewOrder, name='viewOrder'),
    path('order_status/<int:idk>', views.orderStatus, name='orderStatus'),
    path('reports/', views.reports, name='reports'),
]
