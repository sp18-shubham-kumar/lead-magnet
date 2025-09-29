from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from ...models import RoleCost, Role, Location


@staff_member_required
def rolecost_list_view(request):
    rolecosts = RoleCost.objects.all().select_related(
        'role', 'location').order_by('id')
    roles = Role.objects.all().order_by('id')
    locations = Location.objects.all().order_by('id')
    return render(request, "role_cost/list.html", {
        "rolecosts": rolecosts,
        "roles": roles,
        "locations": locations
    })


@staff_member_required
def rolecost_create_view(request):
    if request.method == "POST":
        role_id = request.POST.get("role")
        location_id = request.POST.get("location")
        cost_usd = request.POST.get("cost_usd")
        role = get_object_or_404(Role, pk=role_id)
        location = get_object_or_404(Location, pk=location_id)
        RoleCost.objects.create(
            role=role, location=location, cost_usd=cost_usd)
        return redirect("rolecost-list")
    roles = Role.objects.all()
    locations = Location.objects.all()
    return render(request, "role_cost/form.html", {"roles": roles, "locations": locations})


@staff_member_required
def rolecost_detail_view(request, pk):
    rolecost = get_object_or_404(RoleCost, pk=pk)
    return render(request, "role_cost/detail.html", {"rolecost": rolecost})


@staff_member_required
def rolecost_update_view(request, pk):
    rolecost = get_object_or_404(RoleCost, pk=pk)
    if request.method == "POST":
        role_id = request.POST.get("role")
        location_id = request.POST.get("location")
        cost_usd = request.POST.get("cost_usd")
        rolecost.role = get_object_or_404(Role, pk=role_id)
        rolecost.location = get_object_or_404(Location, pk=location_id)
        rolecost.cost_usd = cost_usd
        rolecost.save()
        return redirect("rolecost-list")
    roles = Role.objects.all()
    locations = Location.objects.all()
    return render(request, "role_cost/form.html", {
        "rolecost": rolecost,
        "roles": roles,
        "locations": locations
    })


@staff_member_required
def rolecost_delete_view(request, pk):
    rolecost = get_object_or_404(RoleCost, pk=pk)
    if request.method == "POST":
        rolecost.delete()
        return redirect("rolecost-list")
    return render(request, "role_cost/confirm_delete.html", {"rolecost": rolecost})
