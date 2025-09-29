from django.db import models
from ..models import Role, Location


class RoleCost(models.Model):
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='rolecosts')
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="rolecosts")
    cost_usd = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('role', 'location')
        ordering = ["role", "location"]

    def __str__(self):
        return f"{self.role} - {self.location} :{self.cost_usd} USD"
