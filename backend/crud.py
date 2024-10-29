from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from sqlalchemy.future import select
from datetime import datetime
import models
import schemas
from models import Leitura


async def get_reading_since(db: AsyncSession, since: datetime):
    return db.query(models.Leitura).filter(models.Leitura.horario_leitura >= since).first()


async def create_leitura(db: AsyncSession, leitura: schemas.Leitura):
    db_leitura = models.Leitura(tensao=leitura.tensao, corrente=leitura.corrente,
                                horario_leitura=leitura.horario_leitura)
    db.add(db_leitura)
    await db.commit()
    await db.refresh(db_leitura)
    return db_leitura


async def create_many_leituras(db: AsyncSession, leituras: [schemas.Leitura]):
    for leitura in leituras:
        db_leitura = models.Leitura(tensao=leitura.tensao, corrente=leitura.corrente,
                                    horario_leitura=leitura.horario_leitura)
        db.add(db_leitura)
    await db.commit()


async def get_last_n_items(db: AsyncSession, limit: int = 100):
    query = select(Leitura).order_by(desc(Leitura.id)).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
