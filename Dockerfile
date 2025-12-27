FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание папки для логов
RUN mkdir -p logs

# Установка PYTHONPATH
ENV PYTHONPATH=/app

# Запуск бота
CMD ["python", "bot/main.py"]



