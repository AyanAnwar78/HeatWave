from django.contrib import admin
from .models import WeatherSearch


@admin.register(WeatherSearch)
class WeatherSearchAdmin(admin.ModelAdmin):
    list_display = ("city", "country", "temperature", "heat_index", "risk_level", "searched_at")
    list_filter  = ("risk_level", "country")
    search_fields = ("city",)
    readonly_fields = ("searched_at",)
