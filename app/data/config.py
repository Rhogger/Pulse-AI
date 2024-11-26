from decouple import Config, RepositoryEnv
import os

# Caminho para o .env
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
env_path = os.path.join(BASE_DIR, ".env")
config = Config(RepositoryEnv(env_path))

DATABASE_NAME = config("DATABASE_NAME")
DATABASE_USER = config("DATABASE_USER")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_HOST = config("DATABASE_HOST", default="localhost")
DATABASE_PORT = config("DATABASE_PORT", default=5432, cast=int)

DATABASE_CONFIG = {
    "connections": {
        "default": f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    },
    "apps": {
        "models": {
            "models": [
                "app.models.specialist",
                "app.models.service",
                "aerich.models"],
            "default_connection": "default",
        },
    },
    "aerich": {
        "tortoise_orm": "app.data.config.DATABASE_CONFIG",
        "location": os.path.join(BASE_DIR, "migrations"),
        "commands_path": os.path.join(BASE_DIR, "aerich", "commands")
    }
}
