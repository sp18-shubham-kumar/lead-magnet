from django.shortcuts import get_object_or_404, render, redirect
from ...models import Lead
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def lead_list_view(request):
    leads = Lead.objects.all()
    return render(request, "lead/list.html", {"leads": leads})


@staff_member_required
def lead_create_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        company = request.POST.get("company")
        Lead.objects.create(name=name, email=email, company=company)
        return redirect("lead-list")
    return render(request, "lead/form.html")


@staff_member_required
def lead_update_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        lead.name = request.POST.get("name")
        lead.email = request.POST.get("email")
        lead.company = request.POST.get("company")
        lead.save()
        return redirect("lead-list")
    return render(request, "lead/form.html", {"lead": lead})


@staff_member_required
def lead_delete_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        lead.delete()
        return redirect("lead-list")
    return render(request, "lead/confirm_delete.html", {"lead": lead})


@staff_member_required
def lead_detail_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, "lead/detail.html", {"lead": lead})
