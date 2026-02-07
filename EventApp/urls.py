from django.urls import path
from .views import index_event, create_event, search_events

app_name = "events"

urlpatterns = [
    path("", index_event, name="index"),
    path("create/", create_event, name="create_event"),
    path("search/", search_events, name="search"),
]