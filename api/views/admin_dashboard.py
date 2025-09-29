from django.shortcuts import render, redirect
from rest_framework.views import APIView


class AdminDashboardView(APIView):
    template_name = "admin/dashboard.html"

    def get(self, request):
        # If session expired or not superuser → force login
        if not request.user.is_authenticated:
            return redirect("admin-login")
        if not request.user.is_superuser:
            return redirect("home")  # redirect non-admins safely
        return render(request, self.template_name, {"user": request.user})
