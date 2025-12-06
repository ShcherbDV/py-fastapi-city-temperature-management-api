from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.temperature import models as temperature_models
from src.city import models as city_models
from src.temperature.weather_service import fetch_temperature_for_city


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None):
    result = await db.execute(select(temperature_models.TemperatureModel))

    if city_id:
        result = await db.execute(select(temperature_models.TemperatureModel).where(temperature_models.TemperatureModel.city_id == city_id))

    temperatures = result.scalars().all()
    return temperatures


async def get_temperature_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(temperature_models.TemperatureModel).where(temperature_models.TemperatureModel.city_id == city_id))
    temperatures = result.scalars().all()

    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperatures found for this city")

    return temperatures


async def update_all_temperatures(db: AsyncSession):
    result = await db.execute(select(city_models.CityModel))
    cities = result.scalars().all()
    if not cities:
        return {"updated": 0}

    count = 0
    for city in cities:
        temperature = await fetch_temperature_for_city(city.name)

        new_record = temperature_models.TemperatureModel(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temperature
        )

        db.add(new_record)
        count += 1

    await db.commit()

    return {"updated": count}
