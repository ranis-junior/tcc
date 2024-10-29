import asyncio
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from time import sleep

load_dotenv()
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import models
import schemas
from database.sqlite import get_db, engine
from config.default import Config


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


asyncio.create_task(init_models())

reader = Config.connection_type

app = FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/leituras/{limit}", response_model=List[schemas.Leitura])
async def get_last_n_items(limit: int = 100, db: AsyncSession = Depends(get_db)):
    async with db as db:
        leituras = await crud.get_last_n_items(db, limit=limit)
    return leituras


async def start_serial_reading():
    print("Inicializando leitura serial em 3...")
    await asyncio.sleep(3)
    with reader(Config.port, Config.baudrate) as rd:
        while True:
            await asyncio.sleep(1)
            leituras = []
            # for _ in range(5):
            read_value = rd.read_line()
            while not read_value or len(read_value) < 13:
                read_value = rd.read_line()
                await asyncio.sleep(0.3)
            corrente, tensao = read_value.rstrip('\n').split('|')
            leitura = schemas.Leitura(tensao=float(tensao), corrente=float(corrente),
                                      horario_leitura=datetime.now())
            leituras.append(leitura)
            if len(leituras) > 0:
                async with get_db() as db:
                    await crud.create_many_leituras(db, leituras)


@app.on_event("startup")
async def schedule_periodic():
    loop = asyncio.get_event_loop()
    loop.create_task(start_serial_reading())


@app.on_event("shutdown")
async def shutdown_event():
    print("Parando leitura serial...")
    print("Leitura serial finalizada")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
