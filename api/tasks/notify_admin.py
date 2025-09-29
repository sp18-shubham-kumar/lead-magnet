from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import format_html


@shared_task
def notify_admin_pending_request(request_id):
    # import inside task to avoid circular imports
    from ..models import PendingRequest
    try:
        req = PendingRequest.objects.get(id=request_id)
    except PendingRequest.DoesNotExist:
        return "Request not found"

    subject = "🚨 New Pending Request Submitted"

    body = format_html(
        """
        <h2>New Pending Request</h2>
        <p><b>Name:</b> {}</p>
        <p><b>Email:</b> {}</p>
        <p><b>Company:</b> {}</p>
        <p><b>Location:</b> {}</p>
        <p><b>Roles to Compare:</b> {}</p>
        <hr>
        <p style="color:gray;">This request is currently <b>{}</b>.</p>
        """,
        req.name or "N/A",
        req.email,
        req.company or "N/A",
        req.location or "N/A",
        req.roles or "N/A",
        req.status,
    )

    admin_email = getattr(settings, "ADMIN_EMAIL", None)
    if not admin_email:
        return "Admin email not configured"

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[admin_email],
    )
    email.content_subtype = "html"  # send as HTML
    email.send(fail_silently=False)

    return "Admin notified"
