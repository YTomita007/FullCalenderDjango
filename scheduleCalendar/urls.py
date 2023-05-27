from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import ImageUploadView

app_name = "cal"
urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.get_events, name="get_events"),
    path("show/<int:parameter>/", views.get_event, name="get_event"),
    path("add/", views.add_event, name="add_event"),
    path("edit/", views.edit_event, name="edit_event"),
    path("delete/<int:_id>/", views.delete_event, name="delete_event"),
    path('admin/', admin.site.urls),
    path("image-upload/", ImageUploadView.as_view(), name="image-upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
