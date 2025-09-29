from django.db import models


class Role(models.Model):
    role = models.CharField(max_length=255)
    level = models.CharField(max_length=100)
    experience_min = models.IntegerField()
    experience_max = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('role', 'level', "experience_min", "experience_max")
        ordering = ["role", "level", "experience_min"]

    def __str__(self):
        return f"{self.role} - {self.level} ({self.experience_min}-{self.experience_max} yrs)"
