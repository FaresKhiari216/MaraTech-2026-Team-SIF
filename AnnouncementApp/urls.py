from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "announcements"

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.new_announcement, name='create'),
    path('<int:announcement_id>/', views.details_announcement, name='Details_Announcement'),
    path('<int:announcement_id>/edit/', views.edit_announcement, name='Edit_Announcement'),
    path('<int:announcement_id>/delete/', views.delete_announcement, name='Delete_Announcement'),
    path('<int:announcement_id>/donate/', views.donate_announcement, name='Donate_Announcement'),
    path('search/', views.search_announcements, name='search'),
]
