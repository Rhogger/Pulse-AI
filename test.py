from tortoise import Tortoise, run_async

async def init():
    await Tortoise.init(
        config={
            "connections": {
                "default": "postgres://postgres:postgres123@localhost:5435/pulse_ai"
            },
            "apps": {
                "models": {
                    "models": [
                        "app.models.specialist",
                        "app.models.service",
                        "app.models.customer",
                        "app.models.chat_session",
                        "app.models.chat_message",
                        "aerich.models",
                    ],
                    "default_connection": "default",
                },
            },
        }
    )
    print("Tortoise ORM initialized successfully!")
    await Tortoise.close_connections()

run_async(init())
