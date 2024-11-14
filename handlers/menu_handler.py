# handlers/menu_handler.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from user_preferences import set_user_language
import logging

logger = logging.getLogger(__name__)

def send_welcome_message(bot, message):
    welcome_text = (
        "👋 Привет! Я бот-преподаватель иностранных языков.\n\n"
        "🎯 Я помогу вам:\n"
        "• Улучшить разговорную речь\n"
        "• Расширить словарный запас\n"
        "• Освоить грамматику\n"
        "• Понять культурные особенности\n\n"
        "🗣 Вы можете:\n"
        "• Писать сообщения\n"
        "• Отправлять голосовые сообщения\n"
        "• Задавать любые вопросы\n"
        "• Практиковать язык в диалогах\n\n"
        "Выберите язык для изучения:"
    )
    bot.send_message(message.chat.id, welcome_text)

def send_menu(bot, message):
    try:
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru"),
            InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"),
            InlineKeyboardButton("עברית 🇮🇱", callback_data="lang_he")
        ]
        markup.add(*buttons)
        
        bot.send_message(
            message.chat.id,
            "Выберите язык обучения / Choose language / בחר שפה",
            reply_markup=markup
        )
        logger.info(f"Menu sent to user {message.chat.id}")
    except Exception as e:
        logger.error(f"Error sending menu: {str(e)}")
        bot.send_message(message.chat.id, "Произошла ошибка при отображении меню. Попробуйте позже.")

def callback_query(bot, call):
    try:
        if call.data.startswith('lang_'):
            language = call.data.replace('lang_', '')
            user_id = call.from_user.id
            
            if language not in config.SUPPORTED_LANGUAGES:
                bot.answer_callback_query(call.id, "Этот язык не поддерживается.")
                return
            
            set_user_language(user_id, language)
            
            welcome_message = config.WELCOME_MESSAGES[language]
            
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, welcome_message)
    except Exception as e:
        logger.error(f"Error handling callback query: {str(e)}")
        bot.answer_callback_query(call.id, "Произошла ошибка при обработке запроса. Попробуйте позже.")
