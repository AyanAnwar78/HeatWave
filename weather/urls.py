from django.urls import path
from . import views

app_name = "weather"

urlpatterns = [
    path("",          views.dashboard, name="dashboard"),
    path("forecast/", views.forecast,  name="forecast"),
    path("heatmap/",  views.heatmap,   name="heatmap"),
    path("about/",    views.about,     name="about"),
    path("api/weather/", views.api_weather, name="api_weather"),
]

