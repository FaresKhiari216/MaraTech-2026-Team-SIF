from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.index_event, name="index"),
    path("create/", views.create_event, name="create_event"),
    path("<int:event_id>/", views.details_event, name="Details_event"),
    path("<int:event_id>/join/", views.join_event, name="join_event"),
    path("<int:event_id>/cancel/", views.cancel_event, name="cancel_event"),
    path('<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path("search/", views.search_events, name="search"),
]