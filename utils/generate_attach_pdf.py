import tempfile
from django.core.files import File
from .report_generation import generate_report_pdf
from ..api.models import ReportItem


def generate_and_attach_pdf(report):
    # collect related items
    items = ReportItem.objects.filter(report=report)

    # calculate total savings
    total_savings = {
        "usd": sum(item.savings_usd for item in items),
    }

    # create temporary file
    tmp = tempfile.NamedTemporaryFile(delete=True, suffix=".pdf")

    # generate the PDF file into tmp.name
    file_path = generate_report_pdf(report, items, total_savings)

    # save to report_file field
    with open(file_path, "rb") as f:
        report.report_file.save(f"report_{report.id}.pdf", File(f))

    report.save()
    return report.report_file.path
