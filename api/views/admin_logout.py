from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect


def admin_logout_view(request):
    auth_logout(request)
    request.session.flush()
    return redirect("home")
