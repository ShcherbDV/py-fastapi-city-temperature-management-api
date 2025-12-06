from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database import Base


class TemperatureModel(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    temperature: Mapped[float] = mapped_column(nullable=False)
    city = relationship("CityModel", back_populates="temperatures")
