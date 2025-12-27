"""Конфигурация бота"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434").rstrip('/')
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "logs")

# Валидация конфигурации
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env файле")

if OLLAMA_TIMEOUT <= 0:
    raise ValueError("OLLAMA_TIMEOUT должен быть положительным числом")

if not OLLAMA_URL.startswith(('http://', 'https://')):
    raise ValueError("OLLAMA_URL должен начинаться с http:// или https://")



