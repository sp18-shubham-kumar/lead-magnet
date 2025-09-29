from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views import View
from ...models import Role


@staff_member_required
def role_list_view(request):
    roles = Role.objects.all().order_by("id")
    return render(request, "roles/list.html", {"roles": roles})


@staff_member_required
def role_detail_view(request, pk):
    """Show role details (GET only)"""
    role = get_object_or_404(Role, pk=pk)
    return render(request, "roles/detail.html", {"role": role})


@staff_member_required
def role_update_view(request, pk):
    """Update an existing role"""
    role = get_object_or_404(Role, pk=pk)
    if request.method == "POST":
        role.role = request.POST.get("role")
        role.level = request.POST.get("level")
        role.experience_min = request.POST.get("experience_min")
        role.experience_max = request.POST.get("experience_max")
        role.save()
        messages.success(request, "Role updated successfully")
        return redirect("role-list")
    return render(request, "roles/form.html", {"role": role})


@staff_member_required
def role_delete_view(request, pk):
    """Delete a role"""
    role = get_object_or_404(Role, pk=pk)
    if request.method == "POST":
        role.delete()
        messages.success(request, "Role deleted successfully")
        return redirect("role-list")
    return render(request, "roles/confirm_delete.html", {"role": role})


@staff_member_required
def role_create_view(request):
    if request.method == "POST":
        role = request.POST.get("role")
        level = request.POST.get("level")
        experience_min = request.POST.get("experience_min")
        experience_max = request.POST.get("experience_max")
        Role.objects.create(
            role=role,
            level=level,
            experience_min=experience_min,
            experience_max=experience_max,
        )
        messages.success(request, "Role created successfully")
        return redirect("role-list")
    return render(request, "roles/form.html")


class RoleBulkUploadView(View):
    """Handle bulk Excel uploads via UI"""

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            messages.error(request, "No file uploaded")
            return redirect("role-list")
        # TODO: implement Excel parsing
        print("Uploaded file:", file.name)
        messages.success(request, "Bulk upload successful!")
        return redirect("role-list")
