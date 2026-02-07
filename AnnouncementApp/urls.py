from django.contrib import admin
from django.urls import include, path
from .views import*

urlpatterns = [
    path('', home, name='home'),
    path('event/', event, name='event'),
    path('announcement/', announcement, name='announcement'),
    
    
]
