#!/bin/bash

# Проверка на наличие аргумента (пути до сервисов)
if [ -z "$1" ]; then
  echo "Укажите пути до сервисов, разделенные пробелом."
  exit 1
fi

# Обработка каждого сервиса
for SERVICE_PATH in "$@"; do
  # Проверка существования директории
  if [ ! -d "$SERVICE_PATH" ]; then
    echo "Указанная директория $SERVICE_PATH не существует."
    continue
  fi

  pipenv requirements > "$SERVICE_PATH/requirements.txt"

  echo "requirements.txt для $SERVICE_PATH создан."
done
