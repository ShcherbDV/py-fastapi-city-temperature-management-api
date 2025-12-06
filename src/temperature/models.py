from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database import Base


class TemperatureModel(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    date_time: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    temperature: Mapped[float] = mapped_column(nullable=False)
