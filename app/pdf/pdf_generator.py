from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from config.settings import get_settings


class PDFGenerator:
    def __init__(self) -> None:
        self.output_dir = Path(get_settings().reports_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_pdf(
        self,
        city_key: str,
        hourly_data: list[dict],
        current_conditions: dict | None,
        filters: dict[str, str | None],
        report_name: str,
    ) -> str:
        file_path = self.output_dir / report_name
        document = SimpleDocTemplate(str(file_path), pagesize=A4, leftMargin=1.5 * cm, rightMargin=1.5 * cm, topMargin=1.5 * cm, bottomMargin=1.5 * cm)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("ReportTitle", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#075985"))
        content = [
            Paragraph("Weather Forecast Report", title_style),
            Paragraph(f"Location key: {city_key}", styles["Normal"]),
            Paragraph(
                f"Applied filters: date = {filters.get('day') or 'all'}, period = {filters.get('period') or 'all'}",
                styles["Normal"],
            ),
            Paragraph(f"Generated at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]),
            Spacer(1, 0.5 * cm),
        ]
        if current_conditions:
            current_rows = [["Temperature", f"{current_conditions['temperature']} °C"], ["Humidity", f"{current_conditions['humidity']}%"], ["Wind speed", f"{current_conditions['wind_speed']} km/h"], ["Weather code", str(current_conditions['weather_code'])]]
            current_table = Table(current_rows, colWidths=[5 * cm, 5 * cm])
            current_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e0f2fe")), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bae6fd")), ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"), ("PADDING", (0, 0), (-1, -1), 7)]))
            content.extend([Paragraph("Current conditions", styles["Heading2"]), current_table, Spacer(1, 0.5 * cm)])
        rows = [["Time", "Temperature", "Humidity", "Wind", "Weather code"]]
        rows.extend([[row["time"], f"{row['temperature']} °C", f"{row['humidity']}%", f"{row['wind_speed']} km/h", str(row["weather_code"])] for row in hourly_data])
        hourly_table = Table(rows, colWidths=[3.2 * cm, 3 * cm, 2.7 * cm, 2.7 * cm, 3 * cm], repeatRows=1)
        hourly_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#075985")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("ALIGN", (1, 1), (-1, -1), "CENTER"), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]), ("PADDING", (0, 0), (-1, -1), 6)]))
        content.extend([Paragraph("Hourly forecast", styles["Heading2"]), hourly_table])
        document.build(content)
        return str(file_path)


pdf_generator = PDFGenerator()
