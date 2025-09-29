from ...models import OTPVerification
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def otp_list_view(request):
    otps = OTPVerification.objects.all()
    return render(request, "otp/list.html", {"otps": otps})