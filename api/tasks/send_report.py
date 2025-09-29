from celery import shared_task
from django.core.mail import EmailMessage
from ..models import ReportHistory, ReportItem, Lead
from utils.report_generation import generate_report_pdf
from django.utils.html import format_html
from django.utils import timezone


@shared_task
def send_report_email(email, report_id):
    try:
        report = ReportHistory.objects.get(id=report_id)
        items = ReportItem.objects.filter(report=report)

        report.status = "queued"
        report.save(update_fields=["status"])

        # Calculate totals
        total_usd = sum(i.savings_usd for i in items)

        # Generate PDF
        # pdf_file = generate_report_pdf(report, items, total_usd)

        # # Send email
        # subject = f"Hiring Cost Report #{report.id}"
        # body = f"""
        # Hi,

        # Please find attached your hiring cost report.
        # Total Savings:
        # {total_usd:.2f} USD

        # Regards,
        # Team Lead Magnet
        # """
        # email_msg = EmailMessage(subject, body, to=[email])
        # email_msg.attach_file(pdf_file)
        # email_msg.send()
        location_name = (
            items[0].from_location.country_name.title()
            if items and items[0].from_location else "Unknown"
        )
        table_rows = ""
        for item in items:
            role_display = f"{item.role.role} ({item.role.level})"
            exp_display = (
                f"{item.role.experience_min}-{item.role.experience_max} Yrs"
            )

            table_rows += f"""
                <tr>
                    <td>{role_display}</td>
                    <td>{exp_display}</td>
                    <td>{item.from_cost_usd:.2f}</td>
                    <td>{item.sp18_cost_usd:.2f}</td>
                    <td>{item.savings_usd:.2f}</td>
                </tr>
            """

        # Totals row
        table_rows += f"""
            <tr style="font-weight:bold;background-color:#f0f0f0;">
                <td>TOTAL SAVINGS</td><td></td><td></td><td></td>
                <td>{total_usd:.2f} USD</td>
            </tr>
        """

        # Full email body
        body_html = f"""
        <p>Hi,</p>
        <p>Please find below your hiring cost report:</p>

        <div style="margin:10px 0;padding:10px;background:#f3f3f3;border-radius:6px;">
            <strong>Client Location:</strong> {location_name}<br>
        </div>

        <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse; font-size: 13px;">
            <thead style="background-color:#333;color:#fff;">
                <tr>
                    <th>Role</th>
                    <th>Experience</th>
                    <th>Client Cost pa (USD)</th>
                    <th>Spark18 Cost pa (USD)</th>
                    <th>Savings pa (USD)</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>

        <p>Regards,<br>Team Lead Magnet</p>
        """

        # Send email
        subject = f"Hiring Cost Report (Lead Magnet)"
        email_msg = EmailMessage(subject, body_html, to=[email])
        email_msg.content_subtype = "html"  # send as HTML
        email_msg.send()

        report.status = "sent"
        report.sent_at = timezone.now()
        report.save(update_fields=["status", "sent_at"])
    except Exception as e:
        try:
            report = ReportHistory.objects.get(id=report_id)
            report.status = "failed"
            report.save(update_fields=["status"])
        except:
            pass
        raise e
