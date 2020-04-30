from django.urls import path
from . import views

urlpatterns=[
    path('signup',views.signup,name="signup"),
    path('signup_submit',views.signup_submit,name="signup_submit"),
    path('login',views.login,name="login"),
    path('login_submit',views.login_submit,name="login_submit"),
    path('logout',views.logout,name="logout"),
    path('home',views.home,name="home"),
    path('plants',views.plants,name="plants"),
    path('seeds',views.seeds,name="seeds"),
    path('soilandfertilizers',views.soil,name="soil"),
    path('decor',views.decor,name="decor"),
    path('accessories',views.accessories,name="accessories"),
    path('compareprices',views.compareprices,name="compareprices"),
    path('search',views.search,name="search"),
    path('cart',views.cart,name="cart"),
    path('checkout',views.checkout,name="checkout"),
    path('confirmorder',views.confirmorder,name="confirmorder"),
    path('displayaddaddressformtoconfirmorder',views.displayaddaddressformtoconfirmorder,name="displayaddaddressformtoconfirmorder"),
    path('myprofile',views.myprofile,name="myprofile"),
    path('edit',views.edit,name="edit"),
    path('editsubmit',views.editsubmit,name="editsubmit"),
    path('addresses',views.addresses,name="addresses"),
    path('addaddress',views.addaddress,name="addaddress"),
    path('addaddresssubmit',views.addaddresssubmit,name="addaddresssubmit"),
    path('deleteaddresssubmit',views.deleteaddresssubmit,name="deleteaddresssubmit"),
    path('orderlogin',views.orderlogin,name="orderlogin"),
    path('orderlogin_submit',views.orderlogin_submit,name="orderlogin_submit"),
    path('selectaddress',views.selectaddress,name="selectaddress"),
    path('payments',views.payments,name="payments"),
    path('successfullorder',views.successfullorder,name="successfullorder"),
    path('charge/', views.charge, name="charge"),
    path('previousOrders', views.successMsg, name="previousOrders"),
]