# Быстрый старт

## 1. Подготовка

1. Получите токен бота у [@BotFather](https://t.me/BotFather)
2. Скопируйте `env.example.txt` в `.env`
3. Вставьте токен в `.env`:
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_здесь
   ```

## 2. Запуск

```bash
# Запустить контейнеры
docker-compose up -d

# Загрузить модель AI
# Для Windows PowerShell (без -it):
docker exec bot_primeta_ollama ollama pull gemma3:1b

# Для Linux/Mac (с -it):
# docker exec -it bot_primeta_ollama ollama pull gemma3:1b

# Проверить логи
docker-compose logs -f bot
```

## 3. Использование

1. Найдите бота в Telegram
2. Отправьте `/start`
3. Задайте вопрос
4. Получите ответ!

## 4. Остановка

```bash
docker-compose down
```

## Проблемы?

- Проверьте, что Docker запущен
- Убедитесь, что порт 11435 свободен (внешний порт Ollama)
- Проверьте логи: `docker-compose logs bot`
- Убедитесь, что модель загружена: `docker exec bot_primeta_ollama ollama list`



