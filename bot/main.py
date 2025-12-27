"""Главный файл для запуска бота"""
import asyncio
import logging
import signal
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import TELEGRAM_BOT_TOKEN
from bot.utils.logger import setup_logger
from bot.handlers import start, messages

# Настройка логирования
setup_logger()
logger = logging.getLogger(__name__)

# Глобальные переменные для graceful shutdown
bot_instance: Bot = None


def signal_handler(signum, frame):
    """Обработчик сигналов для корректного завершения"""
    logger.info(f"Получен сигнал {signum}, завершение работы...")
    if bot_instance:
        asyncio.create_task(bot_instance.session.close())
    sys.exit(0)


async def main():
    """Основная функция запуска бота"""
    global bot_instance
    
    # Регистрация обработчиков сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Инициализация бота и диспетчера
    bot_instance = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(messages.router)
    
    logger.info("Бот запущен и готов к работе")
    
    try:
        # Запуск polling
        await dp.start_polling(bot_instance, skip_updates=True)
    finally:
        # Закрытие соединений при завершении
        await bot_instance.session.close()
        # Закрытие AI сервиса из handlers
        from bot.handlers.messages import ai_service
        await ai_service.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)



