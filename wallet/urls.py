from django.urls import path,include
#from django.contrib import admin
from .import views

urlpatterns = [
 
    path('', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addmoney/',views.addmoney,name='addmoney'),
    path('transfer/', views.trasfermoney, name='transfer'),
    path('passbook/', views.passbook, name='passbook'),
    path('sum/',views.addition,name='addition'),
    path('', include('django.contrib.auth.urls')),
]