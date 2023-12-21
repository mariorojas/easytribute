from django.contrib import admin

from .models import Tribute


@admin.register(Tribute)
class TributeAdmin(admin.ModelAdmin):
    list_display = ['slug', 'pk', 'name', 'owner', 'active']
