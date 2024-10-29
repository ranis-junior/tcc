from datetime import datetime

from sqlalchemy import Column, Float, Integer, DateTime
from database.sqlite import Base


class Leitura(Base):
    __tablename__ = "leituras"

    id: int = Column(Integer, primary_key=True, index=True)
    tensao: float = Column(Float, nullable=False)
    corrente: float = Column(Float, nullable=False)
    horario_leitura: datetime = Column(DateTime, nullable=False)
