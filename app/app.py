import asyncio
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

# Importação das rotas
from app.jobs.session_checker import start_session_checker
from app.routes import (
    specialist,
    service,
    appointment,
    customer,
    chat
)

# Importação das configurações
from app.data.config import DATABASE_CONFIG
from main import init

app = FastAPI()

# Registro das rotas
app.include_router(specialist.router, prefix="/specialists",
                   tags=["Specialists"])
app.include_router(service.router, prefix="/services", tags=["Services"])
app.include_router(appointment.router,
                   prefix="/appointments", tags=["Appointments"])
app.include_router(customer.router, prefix="/customers", tags=["Customers"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])  # Nova rota


@app.on_event("startup")
async def startup_event():
    """Executa todas as tarefas necessárias durante o startup."""
    print("Executando verificação de migrações...")
    await init()

    # Inicia o job de verificação de sessões em background
    asyncio.create_task(start_session_checker())


register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)
