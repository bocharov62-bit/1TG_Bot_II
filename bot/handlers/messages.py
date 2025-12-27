"""Обработчик текстовых сообщений"""
from aiogram import Router, F
from aiogram.types import Message
import logging

from bot.services.ai_service import AIService

router = Router()
# Создаем один экземпляр сервиса для переиспользования
ai_service = AIService()

logger = logging.getLogger(__name__)


@router.message(F.text)
async def handle_message(message: Message):
    """Обработка текстовых сообщений"""
    user_question = message.text.strip()
    
    # Игнорируем пустые сообщения
    if not user_question:
        return
    
    user_id = message.from_user.id
    logger.info(f"Вопрос от {user_id}: {user_question[:50]}...")
    
    try:
        # Показываем, что бот печатает
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        # Получаем ответ от AI
        response = await ai_service.generate_response(user_question)
        
        # Отправляем ответ
        await message.answer(response)
        logger.debug(f"Ответ отправлен пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения от {user_id}: {e}", exc_info=True)
        await message.answer("Произошла ошибка при обработке вашего вопроса.")



