"""Настройка логирования"""
import logging
import os
from datetime import datetime
from pathlib import Path

from bot.config import LOG_LEVEL, LOG_DIR


def setup_logger():
    """Настройка логгера"""
    # Создание папки для логов
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    # Имя файла лога с датой
    log_file = log_dir / f"bot_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    # Настройка формата
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Настройка логгера
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)



