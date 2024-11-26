from fastapi import FastAPI
from app.routes import specialist, service, schedule
from tortoise.contrib.fastapi import register_tortoise
from app.data.config import DATABASE_CONFIG
from main import init

app = FastAPI()

app.include_router(specialist.router, prefix="/specialists", tags=["Specialists"])
app.include_router(service.router, prefix="/services", tags=["Services"])
app.include_router(schedule.router, prefix="/schedules", tags=["Schedules"])


@app.on_event("startup")
async def check_migrations():
    """
    Checa e aplica migrações durante o startup.
    """
    print("Executando verificação de migrações...")
    await init()


register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)
