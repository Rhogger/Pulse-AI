from tortoise import Tortoise, run_async
from aerich import Command
from app.data.config import DATABASE_CONFIG 

async def init():
    """
    Inicializa o Tortoise ORM e aplica as migrações pendentes.
    """
    await Tortoise.init(config=DATABASE_CONFIG)

    print("Verificando migrações...")
    command = Command(tortoise_config=DATABASE_CONFIG)
    
    try:
        await command.init()
        await command.migrate()  
        await command.upgrade(run_in_transaction=True)
        print("Banco de dados e migrações inicializados com sucesso!")
    except Exception as e:
        print(f"Erro ao aplicar migrações: {e}")

    print("Banco de dados e migrações inicializados com sucesso!")
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(init())
