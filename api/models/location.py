from django.db import models


class Location(models.Model):
    country_name = models.CharField(unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["country_name"]

    def __str__(self):
        return f"{self.country_name}"
