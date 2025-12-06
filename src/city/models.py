from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class CityModel(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    additional_info: Mapped[str] = mapped_column(Text, nullable=False)
    temperatures = relationship("TemperatureModel", back_populates="city", cascade="all, delete-orphan")
