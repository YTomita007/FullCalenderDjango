from django.urls import path
from . import views

app_name = "cal"
urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.get_events, name="get_events"),
    path("add/", views.add_event, name="add_event"),
    path("edit/", views.edit_event, name="edit_event"),
    path("delete/<int:_id>/", views.delete_event, name="delete_event"),
]