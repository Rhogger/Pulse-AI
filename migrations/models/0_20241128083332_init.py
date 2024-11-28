from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "specialist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "contact_number" VARCHAR(16) NOT NULL
);
CREATE TABLE IF NOT EXISTS "service" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "time_slots" INT NOT NULL  DEFAULT 1
);
CREATE TABLE IF NOT EXISTS "customer" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "contact_number" VARCHAR(16) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "service_specialist" (
    "service_id" INT NOT NULL REFERENCES "service" ("id") ON DELETE CASCADE,
    "specialist_id" INT NOT NULL REFERENCES "specialist" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_service_spe_service_4ea817" ON "service_specialist" ("service_id", "specialist_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
