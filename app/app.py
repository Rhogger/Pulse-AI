from app.routes.customer import router as customer_router
from fastapi import FastAPI, BackgroundTasks
from app.routes import specialist, service, appointment
from tortoise.contrib.fastapi import register_tortoise
from app.data.config import DATABASE_CONFIG
from main import init
from app.crew.crew import run_crew
from multiprocessing import Process
from tortoise import Tortoise

app = FastAPI()

app.include_router(specialist.router, prefix="/specialists",
                   tags=["Specialists"])
app.include_router(service.router, prefix="/services", tags=["Services"])
app.include_router(appointment.router, prefix="/appointments",
                   tags=["Appointments"])
app.include_router(customer_router, prefix="/customers", tags=["Customers"])


@app.on_event("startup")
async def startup_event():
    """
    Executa todas as tarefas necessárias durante o startup.
    """
    print("Executando verificação de migrações...")
    await init()


def run_crew_process(contact_number, message):
    """
    Função que será executada em um processo separado
    """
    import asyncio
    
    async def run():
        try:
            # Inicializa a conexão com o banco de dados no novo processo
            await Tortoise.init(config=DATABASE_CONFIG)
            results = await run_crew(contact_number, message)
            print("Resultado do crew:", results)
        except Exception as e:
            print(f"Erro ao executar crew: {str(e)}")
        finally:
            # Fecha a conexão com o banco de dados
            await Tortoise.close_connections()
    
    asyncio.run(run())


@app.post("/start-crew")
async def start_crew():
    """
    Endpoint para iniciar o crew AI em um processo separado
    """
    process = Process(
        target=run_crew_process,
        args=("(64) 9 9984-0431", "Boa tarde, quero agendar um horário.")
    )
    process.start()
    return {"message": "Crew AI iniciado em processo separado"}


register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)
