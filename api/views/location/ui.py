from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from ...models import Location
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from utils.location_handler import location_setter


def location_list_view(request):
    if not request.user.is_staff:
        locations = Location.objects.exclude(
            country_name__iexact="Spark Eighteen").order_by("id")
    else:
        locations = Location.objects.all().order_by("id")
    return render(request, "locations/list.html", {"locations": locations})


@staff_member_required
def location_detail_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
    return render(request, "locations/detail.html", {"location": location})


@staff_member_required
def location_create_view(request):
    if request.method == "POST":
        country_name = location_setter(request.POST.get("country_name", ""))
        if Location.objects.filter(country_name__iexact=country_name).exists():
            messages.error(
                request, "A location with this name already exists.")
        else:
            Location.objects.create(country_name=country_name)
            messages.success(request, "Location created successfully.")
        return redirect("location-list")
    return render(request, "locations/form.html")


@staff_member_required
def location_update_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        country_name = location_setter(request.POST.get("country_name", ""))
        if Location.objects.exclude(pk=pk).filter(country_name__iexact=country_name).exists():
            messages.error(
                request, "A location with this name already exists.")
        else:
            location.country_name = country_name
            location.save()
            messages.success(request, "Location updated successfully.")
            return redirect("location-list")
    return render(request, "locations/form.html", {"location": location})


@staff_member_required
def location_delete_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        location.delete()
        messages.success(request, "Location deleted successfully.")
        return redirect("location-list")
    return render(request, "locations/confirm_delete.html", {"location": location})


class LocationBulkUploadView(View):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            messages.error(request, "No file uploaded")
            return redirect("location-list-create")

        # TODO: implement Excel parsing logic
        # For now, just print or log the file name
        print("Uploaded file:", file.name)

        messages.success(request, "Bulk upload successful!")
        return redirect("location-list-create")
