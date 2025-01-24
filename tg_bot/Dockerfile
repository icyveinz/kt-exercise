# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /tg_bot

# Копируем содержимое текущей директории в контейнер
COPY . /tg_bot

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH=/tg_bot

# Команда для запуска main.py
CMD ["python", "main.py"]