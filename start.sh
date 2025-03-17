#!/bin/bash
while true; do
    pipenv run python3 run.py
    echo "Reiniciando em 5 segundos..."
    sleep 5
done

# Mantém o contêiner rodando para evitar que ele saia
tail -f /dev/null