#!/bin/sh

# Espera o banco de dados ficar pronto
echo "Aguardando o banco de dados ficar pronto..."
until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Banco pronto!"

# Executa migrações
python manage.py migrate

# Carrega os dados iniciais (fixtures)
echo "Carregando fixtures..."
python manage.py loaddata seapac/fixtures/*.json || echo "Nenhum fixture encontrado ou já carregado."

# Inicia o servidor
echo "Iniciando o servidor Django..."
exec python manage.py runserver 0.0.0.0:8000