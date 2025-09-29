from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from ...models import ReportHistory
from utils.form import ReportHistoryForm, ReportItemForm


@staff_member_required
def report_history_list(request):
    reports = ReportHistory.objects.all().order_by("-created_at")
    return render(request, "report_history/list.html", {"reports": reports})


@staff_member_required
def report_history_create(request):
    if request.method == "POST":
        form = ReportHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            messages.success(request, "Report created successfully.")
            return redirect("reporthistory-detail", pk=report.id)
        else:
            messages.error(request, "Please fix form errors below.")
    else:
        form = ReportHistoryForm()
    return render(request, "report_history/form.html", {"form": form})


@staff_member_required
def report_history_detail(request, pk):
    report = get_object_or_404(ReportHistory, pk=pk)
    items = report.items.all().order_by("-created_at")
    item_form = ReportItemForm()
    return render(
                request, "report_history/detail.html", 
                {"report": report, "items": items, 
                 "item_form": item_form}
                )


@staff_member_required
def report_history_delete(request, pk):
    report = get_object_or_404(ReportHistory, pk=pk)
    if request.method == "POST":
        report.delete()
        messages.success(request, "Report deleted.")
        return redirect("reporthistory-list")
    return render(request, "report_history/confirm_delete.html", 
                  {"report": report})
