from datetime import datetime
from config.base import Base
from sqlalchemy import BigInteger, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class WeatherForecastDatabaseEntity(Base):
    __tablename__ = "weather_forecast"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    city_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    forecast_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    forecast_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )