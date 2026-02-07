from django.urls import path
from .views import index_event, create_event

app_name = "events"

urlpatterns = [
    path("", index_event, name="index"),
    path("create/", create_event, name="create_event"),
]