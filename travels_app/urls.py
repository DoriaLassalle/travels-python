from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('travel', views.travel),
    path('loginForm',views.loginForm),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('travels/destination/<dest_id>', views.showDestination),
    path('travels/add', views.showFormAdd),
    path('addTrip', views.addTrip),
    path('join/<travel_id>', views.join)
]
