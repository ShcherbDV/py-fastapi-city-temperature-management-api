from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.city import models, schemas


async def get_all_cities(db:AsyncSession):
    query = select(models.CityModel)
    cities = await db.execute(query)
    return [city[0] for city in cities.fetchall()]


async def create_citi(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.CityModel).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.CityModel).where(models.CityModel.id == city_id))
    city = result.scalar_one_or_none()
    if city is None:
        raise HTTPException(status_code=404, detail="City with such id is not found")
    return city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityUpdate):
    result = await db.execute(select(models.CityModel).where(models.CityModel.id == city_id))
    db_city = result.scalar_one_or_none()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City with such id is not found")

    if city.name:
        db_city.name = city.name

    if city.additional_info:
        db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.CityModel).where(models.CityModel.id == city_id))
    city = result.scalar_one_or_none()
    if city is None:
        raise HTTPException(status_code=404, detail="City with such id is not found")
    await db.delete(city)
    await db.commit()

    return {"detail": "City deleted successfully"}
