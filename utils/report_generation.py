from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tempfile
from django.conf import settings
import os


def generate_report_pdf(report, items, total_savings):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    filename = tmp.name
    tmp.close()

    doc = SimpleDocTemplate(filename)

    elements = []
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]

    # Title
    elements.append(Paragraph(f"Hiring Cost Report", title_style))
    elements.append(Paragraph(
        f"Created At: {report.created_at.strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Table header
    data = [
        ["Role", "Experience", "From Location",
         "Client Cost (USD)", "Spark18 Cost (USD)", "Savings (USD)"]
    ]

    # Table rows
    for item in items:
        role_display = f"{item.role.role} ({item.role.level})"
        exp_display = f"{item.role.experience_min}-{item.role.experience_max} Yrs" if item.role.experience_min or item.role.experience_max else "-"
        from_loc = item.from_location.country_name if item.from_location else "-"

        data.append([
            role_display,
            exp_display,
            from_loc,
            f"{item.from_cost_usd:.2f}",
            f"{item.sp18_cost_usd:.2f}",
            f"{item.savings_usd:.2f}",
        ])

    # Totals row
    data.append([
        "TOTAL SAVINGS", "", "",
        "", "",
        f"{total_savings} USD"
    ])

    # Table styling
    table = Table(data, repeatRows=1, colWidths=[150, 70, 90, 90, 90, 90])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -2), colors.beige),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
    ]))

    elements.append(table)
    doc.build(elements)
    return filename
