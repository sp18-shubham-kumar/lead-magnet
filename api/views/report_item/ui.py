from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from ...models import ReportHistory, ReportItem
from utils.form import ReportItemForm


@staff_member_required
def report_item_create(request, report_history_id):
    report = get_object_or_404(ReportHistory, pk=report_history_id)
    if request.method == "POST":
        form = ReportItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.report = report
            item.save()
            messages.success(request, "Report item added.")
            return redirect("reporthistory-detail", pk=report.id)
        else:
            messages.error(request, "Please fix form errors below.")
    else:
        form = ReportItemForm()
    return render(request, "report_item/form.html", 
                  {"form": form, "report": report})


@staff_member_required
def report_item_detail(request, report_history_id, pk):
    report = get_object_or_404(ReportHistory, pk=report_history_id)
    item = get_object_or_404(ReportItem, pk=pk, report=report)
    return render(request, "report_item/detail.html", 
                  {"item": item, "report": report})


@staff_member_required
def report_item_update(request, report_history_id, pk):
    report = get_object_or_404(ReportHistory, pk=report_history_id)
    item = get_object_or_404(ReportItem, pk=pk, report=report)
    if request.method == "POST":
        form = ReportItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Report item updated.")
            return redirect("reporthistory-detail", pk=report.id)
        else:
            messages.error(request, "Please fix form errors below.")
    else:
        form = ReportItemForm(instance=item)
    return render(request, "report_item/form.html", 
                  {"form": form, "report": report, "item": item})


@staff_member_required
def report_item_delete(request, report_history_id, pk):
    report = get_object_or_404(ReportHistory, pk=report_history_id)
    item = get_object_or_404(ReportItem, pk=pk, report=report)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Report item deleted.")
        return redirect("reporthistory-detail", pk=report.id)
    return render(request, "report_item/confirm_delete.html", 
                  {"item": item, "report": report})
