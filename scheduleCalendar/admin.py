from django.contrib import admin
from .models import SnsModel
from .models import Event

# Register your models here.
admin.site.register(SnsModel)
admin.site.register(Event)
