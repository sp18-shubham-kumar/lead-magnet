from django.db import models
from ..models import Role, Location, Lead


class ReportHistory(models.Model):
    STATUS_CHOICES = [
        ("generated", "Generated"),
        ("sent", "Sent"),
        ("failed", "Failed"),
        ("queued", "Queued"),
    ]
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    report_file = models.FileField(upload_to="reports/", null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="generated")
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report for {self.lead.email} on {self.created_at}"


class ReportItem(models.Model):
    report = models.ForeignKey(
        ReportHistory, on_delete=models.CASCADE, related_name='items')
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='report_items')
    from_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="report_item_to", null=True, blank=True)
    sp18_cost_usd = models.DecimalField(max_digits=12, decimal_places=2)
    from_cost_usd = models.DecimalField(max_digits=12, decimal_places=2)
    savings_usd = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.role} ({self.from_location}) : {self.savings_usd} USD savings"
