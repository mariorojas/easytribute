from django.contrib import admin

from .models import Report, Tribute


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['summary', 'created_at', 'tribute', 'is_tribute_active']
    readonly_fields = ['is_tribute_active']

    @admin.display()
    def summary(self, obj):
        summary = obj.detail[:20]
        return f'{summary}...'

    @admin.display(boolean=True)
    def is_tribute_active(self, obj):
        return obj.tribute.active


@admin.register(Tribute)
class TributeAdmin(admin.ModelAdmin):
    list_display = ['slug', 'pk', 'name', 'owner', 'picture', 'active']
