from datetime import datetime

from pydantic import BaseModel


class Leitura(BaseModel):
    tensao: float
    corrente: float
    horario_leitura: datetime

    class Config:
        from_attributes = True
