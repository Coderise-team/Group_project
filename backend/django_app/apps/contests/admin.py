from django.contrib import admin

from .models import Contest


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "start_time", "end_time")
    list_filter = ("status",)
    search_fields = ("title",)
    date_hierarchy = "start_time"
    filter_horizontal = ("problems", "participants")
    ordering = ("-start_time",)
