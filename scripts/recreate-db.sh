#!/bin/bash

# Carrega as variáveis do .env
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
    echo "Arquivo .env não encontrado"
    exit 1
fi

echo "Verificando Redis..."
# Verifica se o Redis está instalado e rodando
if ! command -v redis-cli &> /dev/null; then
    echo "Redis não está instalado. Por favor, instale o Redis primeiro."
    exit 1
fi

if ! redis-cli ping &> /dev/null; then
    echo "Redis não está rodando. Iniciando Redis..."
    sudo service redis-server start
    sleep 2
fi

echo "Limpando dados do Redis..."
redis-cli FLUSHALL

echo "Recriando banco de dados..."

# Executar os comandos do PostgreSQL como usuário postgres
sudo -u postgres psql << EOF
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'pulse_ai';
DROP DATABASE IF EXISTS pulse_ai;
CREATE DATABASE pulse_ai;
EOF

echo "Banco de dados recriado com sucesso!"

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

echo "Verificando conexão com Redis..."
if redis-cli ping | grep -q "PONG"; then
    echo "Redis está funcionando corretamente!"
else
    echo "AVISO: Redis não está respondendo corretamente!"
fi

echo "Processo finalizado com sucesso!"

# Inicia o servidor
uvicorn app.app:app --reload