#!/bin/bash

while true; do
    # Executa o comando
    pipenv run python3 run.py

    # Espera 10 minutos
    sleep 600
done
