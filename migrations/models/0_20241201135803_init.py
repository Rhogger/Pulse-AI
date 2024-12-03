from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "specialist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "contact_number" VARCHAR(16) NOT NULL
);
CREATE TABLE IF NOT EXISTS "services" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "duration" INT NOT NULL,
    "price" DECIMAL(10,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS "customer" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "contact_number" VARCHAR(16) NOT NULL
);
CREATE TABLE IF NOT EXISTS "chat_sessions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "contact_number" VARCHAR(20) NOT NULL,
    "status" VARCHAR(10) NOT NULL  DEFAULT 'idle',
    "last_interaction" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "chat_sessions"."status" IS 'ACTIVE: active\nPROCESSING: processing\nIDLE: idle\nCLOSED: closed';
CREATE TABLE IF NOT EXISTS "chat_messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "session_id" INT NOT NULL REFERENCES "chat_sessions" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "service_specialist" (
    "services_id" INT NOT NULL REFERENCES "services" ("id") ON DELETE CASCADE,
    "specialist_id" INT NOT NULL REFERENCES "specialist" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_service_spe_service_89333b" ON "service_specialist" ("services_id", "specialist_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
