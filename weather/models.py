from django.db import models


class WeatherSearch(models.Model):
    """Stores recent city weather searches for history tracking."""
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=10, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    heat_index = models.FloatField()
    risk_level = models.CharField(max_length=30)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']

    def __str__(self):
        return f"{self.city} – {self.searched_at:%Y-%m-%d %H:%M}"
