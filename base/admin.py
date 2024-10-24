from django.contrib import admin

# Register your models here.
from .models import Room,Topic,Message

# for viewing this item and wotk in built-in admin panel
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)