"""Сервис для работы с Ollama AI"""
import asyncio
import aiohttp
import logging
import re
from bot.config import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT

logger = logging.getLogger(__name__)

# Константы
ERROR_MESSAGE = "Вернитесь позже, я пока занят."
PROMPT_TEMPLATE = """Ты дружелюбный помощник. Отвечай на вопросы кратко и неформально, 1-2 предложениями.

Вопрос: {question}

Ответ:"""


class AIService:
    """Сервис для взаимодействия с Ollama"""
    
    def __init__(self):
        self.base_url = OLLAMA_URL.rstrip('/')
        self.model = OLLAMA_MODEL
        self.timeout = aiohttp.ClientTimeout(total=OLLAMA_TIMEOUT)
    
    async def close(self):
        """Закрытие HTTP сессии (для совместимости)"""
        pass
    
    def _truncate_to_sentences(self, text: str, max_sentences: int = 2) -> str:
        """
        Обрезка текста до указанного количества предложений
        
        Args:
            text: Исходный текст
            max_sentences: Максимальное количество предложений
            
        Returns:
            Обрезанный текст
        """
        if not text:
            return text
        
        # Разделение по точкам, восклицательным и вопросительным знакам
        sentences = re.split(r'[.!?]+\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) > max_sentences:
            result = '. '.join(sentences[:max_sentences])
            # Добавляем точку в конце, если её нет
            if not result.endswith(('.', '!', '?')):
                result += '.'
            return result
        
        return text
    
    async def generate_response(self, user_question: str) -> str:
        """
        Генерация ответа на вопрос пользователя
        
        Args:
            user_question: Вопрос пользователя
            
        Returns:
            Ответ от AI или сообщение об ошибке
        """
        if not user_question or not user_question.strip():
            return "Пожалуйста, задайте вопрос."
        
        prompt = PROMPT_TEMPLATE.format(question=user_question.strip())
        
        try:
            # Создаем новую сессию для каждого запроса (надежнее)
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 150
                        }
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        answer = data.get("response", "").strip()
                        
                        if not answer:
                            logger.warning("Получен пустой ответ от AI")
                            return "Извините, не могу ответить на этот вопрос."
                        
                        # Ограничение ответа до 2 предложений
                        answer = self._truncate_to_sentences(answer, max_sentences=2)
                        logger.debug(f"AI ответ: {answer[:100]}...")
                        return answer
                    else:
                        error_text = await response.text()
                        logger.error(f"Ошибка Ollama API: статус {response.status}, ответ: {error_text[:200]}")
                        return ERROR_MESSAGE
                        
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения к Ollama: {e}")
            return ERROR_MESSAGE
        except asyncio.TimeoutError:
            logger.error(f"Таймаут при обращении к Ollama (> {OLLAMA_TIMEOUT} сек)")
            return ERROR_MESSAGE
        except Exception as e:
            logger.error(f"Неожиданная ошибка в AI сервисе: {e}", exc_info=True)
            return ERROR_MESSAGE

