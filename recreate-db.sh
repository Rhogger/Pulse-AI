#!/bin/bash

# Carrega as variáveis do .env
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
    echo "Arquivo .env não encontrado"
    exit 1
fi

echo "Recriando banco de dados..."

# Encerra todas as conexões com o banco (usando sudo -u postgres)
sudo -u postgres psql -c "
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = '$DATABASE_NAME'
AND pid <> pg_backend_pid();"

# Drop e create do banco usando sudo -u postgres
echo "Dropando banco de dados..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DATABASE_NAME;"
if [ $? -ne 0 ]; then
    echo "Erro ao dropar o banco de dados"
    exit 1
fi

echo "Criando banco de dados..."
sudo -u postgres psql -c "CREATE DATABASE $DATABASE_NAME OWNER $DATABASE_USER;"
if [ $? -ne 0 ]; then
    echo "Erro ao criar o banco de dados"
    exit 1
fi

echo "Banco de dados recriado com sucesso"

# Remove migrations antigas
echo "Removendo migrations antigas..."
rm -rf migrations/*

# Aguarda alguns segundos para garantir que o banco está pronto
sleep 2

# Inicializa as migrations
echo "Inicializando migrations..."
aerich init-db
if [ $? -ne 0 ]; then
    echo "Erro ao inicializar as migrations"
    exit 1
fi

# Gera nova migration
echo "Gerando nova migration..."
aerich migrate --name initial
if [ $? -ne 0 ]; then
    echo "Erro ao gerar migration"
    exit 1
fi

# Aplica as migrations
echo "Aplicando migrations..."
aerich upgrade
if [ $? -ne 0 ]; then
    echo "Erro ao aplicar migrations"
    exit 1
fi

echo "Processo finalizado com sucesso!"

# Inicia o servidor
uvicorn app.app:app --reload