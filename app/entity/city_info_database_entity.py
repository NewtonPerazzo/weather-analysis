from config.base import Base
from datetime import datetime, timedelta, timezone

from config.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String

class CityInfoDatabaseEntity(Base):
    __tablename__ = "city_info"

    id: Mapped[str] = mapped_column(String(255), nullable=False, primary_key=True,)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    elevation: Mapped[float] = mapped_column(nullable=True)
    feature_code: Mapped[str] = mapped_column(String(255), nullable=False)
    country_code: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(255), nullable=False)
    population: Mapped[int] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    admin1: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=1),
    )