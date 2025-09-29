from ...models import PendingRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def pending_request_list_view(request):
    prs = PendingRequest.objects.all()
    return render(request, "pending_requests/list.html", {"prs": prs})
