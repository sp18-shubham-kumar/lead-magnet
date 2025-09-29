import openpyxl
from rapidfuzz import fuzz
from django.contrib import messages
from django.shortcuts import render, redirect
from ...models import Role, RoleCost, Location
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def rolecost_bulk_upload_view(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            messages.error(request, "Please upload a file")
            return redirect("rolecost-bulk-upload")

        wb = openpyxl.load_workbook(file)
        sheet = wb.active

        added, skipped = 0, 0
        for row in sheet.iter_rows(min_row=2, values_only=True):
            role_name, level, exp_min, exp_max, location_name, cost = row

            # ---- Role fuzzy match ----
            existing_roles = Role.objects.values_list(
                "id", "role", "level", "experience_min", "experience_max")
            matched_role = None
            for rid, r, l, e_min, e_max in existing_roles:
                score = fuzz.token_sort_ratio(
                    f"{r} {l}", f"{role_name} {level}")
                if score > 90 and e_min == exp_min and e_max == exp_max:
                    matched_role = Role.objects.get(id=rid)
                    break
            if not matched_role:
                matched_role = Role.objects.create(
                    role=role_name.strip(),
                    level=level.strip(),
                    experience_min=int(exp_min),
                    experience_max=int(exp_max),
                )

            # ---- Location fuzzy match ----
            existing_locations = Location.objects.values_list(
                "id", "country_name")
            matched_loc = None
            for lid, cname in existing_locations:
                score = fuzz.token_sort_ratio(cname, location_name)
                if score > 90:
                    matched_loc = Location.objects.get(id=lid)
                    break
            if not matched_loc:
                matched_loc = Location.objects.create(
                    country_name=location_name.strip())

            # ---- RoleCost check ----
            rolecost_obj = RoleCost.objects.filter(
                role=matched_role, location=matched_loc).first()
            if rolecost_obj:
                if float(rolecost_obj.cost_usd) != float(cost):
                    rolecost_obj.cost_usd = cost
                    rolecost_obj.save()
                    added += 1  # count updated as added
                else:
                    skipped += 1
            else:
                RoleCost.objects.create(
                    role=matched_role,
                    location=matched_loc,
                    cost_usd=cost
                )
                added += 1

        messages.success(
            request, f"Upload completed: {added} added/updated, {skipped} skipped (no changes)")
        return redirect("rolecost-list")

    return render(request, "role_cost/bulk_upload.html")
