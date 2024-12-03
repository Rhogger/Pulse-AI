#!/bin/bash

# Carrega as variáveis do .env
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
    echo "Arquivo .env não encontrado"
    exit 1
fi

# Imprimir as variáveis de ambiente carregadas
echo "Variáveis de ambiente carregadas:"
echo "DATABASE_NAME=$DATABASE_NAME"
echo "DATABASE_USER=$DATABASE_USER"
echo "DATABASE_PASSWORD=$DATABASE_PASSWORD"
echo "DATABASE_HOST=$DATABASE_HOST"
echo "DATABASE_PORT=$DATABASE_PORT"
echo "GEMINI_API_KEY=$GEMINI_API_KEY"
echo "BASE_URL=$BASE_URL"
echo "REDIS_URL=$REDIS_URL"
echo "REDIS_HOST=$REDIS_HOST"
echo "REDIS_PORT=$REDIS_PORT"
echo "REDIS_TTL=$REDIS_TTL"

if [ -z "$DATABASE_NAME" ] || [ -z "$DATABASE_USER" ] || [ -z "$DATABASE_PASSWORD" ] || [ -z "$DATABASE_HOST" ] || [ -z "$DATABASE_PORT" ] || [ -z "$REDIS_HOST" ] || [ -z "$REDIS_PORT" ]; then
    echo "Erro: Variáveis de ambiente ausentes no .env"
    exit 1
fi

echo "Verificando Redis..."
# Verifica se o Redis está instalado e rodando
if ! command -v redis-cli &> /dev/null; then
    echo "Redis não está instalado. Por favor, instale o Redis primeiro."
    exit 1
fi

# Verifica a conexão com Redis usando o host e a porta configurada no .env
echo "Tentando conectar ao Redis..."
# Tente conectar usando o IP do contêiner Redis
if ! redis-cli -h $REDIS_HOST -p $REDIS_PORT ping | grep -q "PONG"; then
    echo "Redis não está rodando ou não pode ser acessado. Tentando iniciar o Redis..."
    # Tente iniciar o Redis no contêiner se ele não estiver rodando
    sudo docker start redis_secondary
    sleep 2
fi


# Limpa todos os dados do Redis
echo "Limpando dados do Redis..."
redis-cli -h $REDIS_HOST -p $REDIS_PORT FLUSHALL
if [ $? -ne 0 ]; then
    echo "Erro ao limpar os dados do Redis."
    exit 1
fi

# Verifica se o Redis está funcionando
echo "Verificando se o Redis está funcionando..."
if redis-cli -h $REDIS_HOST -p $REDIS_PORT ping | grep -q "PONG"; then
    echo "Redis está funcionando corretamente!"
else
    echo "AVISO: Redis não está respondendo corretamente!"
    exit 1
fi

# Recria o banco de dados PostgreSQL
echo "Recriando banco de dados..."

docker exec -i postgres_secondary psql -U postgres -d postgres -c "
REVOKE CONNECT ON DATABASE pulse_ai FROM public;
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'pulse_ai';
" && \
docker exec -i postgres_secondary psql -U postgres -d postgres -c "DROP DATABASE IF EXISTS pulse_ai;" && \
docker exec -i postgres_secondary psql -U postgres -d postgres -c "CREATE DATABASE pulse_ai;"

if [ $? -ne 0 ]; then
    echo "Erro ao recriar o banco de dados."
    exit 1
fi
echo "Banco de dados recriado com sucesso!"

# Remove migrations antigas
echo "Removendo migrations antigas..."
rm -rf migrations/*
if [ $? -ne 0 ]; then
    echo "Erro ao remover migrations antigas."
    exit 1
fi

# Aguarda alguns segundos para garantir que o banco está pronto
echo "Aguardando a inicialização do banco..."
sleep 2

# Inicializa as migrations
echo "Inicializando migrations..."
aerich init-db
if [ $? -ne 0 ]; then
    echo "Erro ao inicializar as migrations."
    exit 1
fi

# Gera nova migration
echo "Gerando nova migration..."
aerich migrate --name initial
if [ $? -ne 0 ]; then
    echo "Erro ao gerar migration."
    exit 1
fi

# Aplica as migrations
echo "Aplicando migrations..."
aerich upgrade
if [ $? -ne 0 ]; then
    echo "Erro ao aplicar migrations."
    exit 1
fi

echo "Processo de migrations completado com sucesso!"

# Inicia o servidor
echo "Iniciando o servidor..."
uvicorn app.app:app --reload