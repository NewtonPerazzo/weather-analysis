from app.pdf.pdf_generator import pdf_generator
from config.celery import celery_app


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_report_task(self, data: dict) -> dict:
    city_key = data.get("city_key", "unknown")
    hourly = data["hourly"]
    current = data["current"]
    filters = data.get("filters", {})
    hourly_data = [
        {
            "time": hourly["time"][index],
            "temperature": hourly["temperature_2m"][index],
            "humidity": hourly["relative_humidity_2m"][index],
            "wind_speed": hourly["wind_speed_10m"][index],
            "weather_code": hourly["weather_code"][index],
        }
        for index in range(len(hourly["time"]))
    ]
    current_conditions = (
        {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "weather_code": current["weather_code"],
        }
        if current
        else None
    )
    report_suffix = "_".join(
        value for value in (filters.get("day"), filters.get("period")) if value
    )
    report_name = f"weather_report_{city_key}{f'_{report_suffix}' if report_suffix else ''}.pdf"
    file_path = pdf_generator.create_pdf(
        city_key=city_key,
        hourly_data=hourly_data,
        current_conditions=current_conditions,
        filters=filters,
        report_name=report_name,
    )
    return {
        "city_key": city_key,
        "file": file_path,
        "report": report_name,
        "status": "completed",
    }
