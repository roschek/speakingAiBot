import logging
from integrations.chatgpt_integration import get_chatgpt_response
from user_preferences import get_user_language
import config

logger = logging.getLogger(__name__)

def handle_user_message(bot, message):
    """Обработка пользовательских сообщений"""
    try:
        user_id = message.from_user.id
        user_language = get_user_language(user_id) or config.DEFAULT_LANGUAGE
        
        response = get_chatgpt_response(message.text, language=user_language)
        bot.reply_to(message, response)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {str(e)}")
        bot.reply_to(message, config.ERROR_MESSAGES['general_error'])
