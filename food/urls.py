from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
    path('', views.index, name="FoodHome"),
    path('categories/',views.categories , name="Categories"),
    path('resdishview/<single_slug>',views.single_slug, name="Resdishes"),
    path('dishes/<int:myid>',views.dishview, name="DishView"),
    path('aboutus/',views.aboutus, name= "aboutus"),
    path('contact/', views.contactus, name="contact"),
    path('login/',views.handleLogin, name="handleLogin"),
    path('logout/',views.handleLogout, name="handleLogout"),
    path('signup/',views.handleSignup, name="handleSignup"),
    path('cart/', views.cart, name="cart"),
    path('checkout/<amt>',views.checkout, name="checkout"),
    path('search/',views.search, name="search"),
    path('cart_check_out/',views.cart_check_out, name="cart_check_out"),
    path('checkout/place_order/',views.place_order, name="place_order"),
]