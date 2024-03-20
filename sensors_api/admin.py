# admin.py
from django.contrib import admin
from .models import ESP32Device


class ESP32DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'token','user','switching_token')  # Customize the display fields in the list view


admin.site.register(ESP32Device, ESP32DeviceAdmin)
