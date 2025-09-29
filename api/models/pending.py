from django.db import models


class PendingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', "Pending"),
        ("completed", "Completed"),
    ]

    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    company = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    roles = models.CharField(max_length=1023, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.role} - {self.seniority} ({self.location}) [{self.status}]"
