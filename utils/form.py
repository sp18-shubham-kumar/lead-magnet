from api.models import ReportHistory, ReportItem
from django import forms

# ----------------------------
# ModelForms (keeps UI validation same as ORM)
# ----------------------------
class ReportHistoryForm(forms.ModelForm):
    class Meta:
        model = ReportHistory
        fields = ["lead", "report_file"]  # lead optional, report_file optional as per model
        widgets = {
            "lead": forms.Select(attrs={"class": "form-select"}),
        }


class ReportItemForm(forms.ModelForm):
    class Meta:
        model = ReportItem
        fields = ["role", "from_location", "sp18_cost_usd", "from_cost_usd", "savings_usd"]
        widgets = {
            "role": forms.Select(attrs={"class": "form-select"}),
            "from_location": forms.Select(attrs={"class": "form-select"}),
            "sp18_cost_usd": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "from_cost_usd": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "savings_usd": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }