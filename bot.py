import telebot
import logging
import config
import os
from integrations.chatgpt_integration import get_chatgpt_response
from handlers.menu_handler import send_menu, callback_query, send_welcome_message
from user_preferences import get_user_language
from integrations.speech_recognition import convert_voice_to_text
from integrations.elevenlabs_integration import generate_voice_message

logger = logging.getLogger(__name__)

def handle_error(error: Exception) -> str:    
    logger.error(f"Ошибка: {str(error)}", exc_info=True)
    return config.ERROR_MESSAGES['general_error']

class Bot:
    def __init__(self):
        if not config.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения")
        
        self.bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
        self.setup_handlers()
        logger.info("Bot initialized")

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start', 'menu'])
        def welcome(message):
            logger.info(f"Command {message.text} received from user {message.from_user.id}")
            send_welcome_message(self.bot, message)
            send_menu(self.bot, message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):
            logger.info(f"Callback query {call.data} from user {call.from_user.id}")
            callback_query(self.bot, call)

        @self.bot.message_handler(content_types=['voice', 'text'])
        def handle_message(message):
            self._process_message(message)

    def _process_message(self, message):
        try:
            user_id = message.from_user.id
            user_language = get_user_language(user_id) or config.DEFAULT_LANGUAGE
            
            if message.content_type == 'voice':                
                file_info = self.bot.get_file(message.voice.file_id)
                downloaded_file = self.bot.download_file(file_info.file_path)
                voice_file_path = os.path.join(config.TEMP_DIR, f"voice_{message.voice.file_id}.ogg")
                
                with open(voice_file_path, 'wb') as voice_file:
                    voice_file.write(downloaded_file)
                
                try:
                    user_message = convert_voice_to_text(voice_file_path, user_language)                    
                    
                    response = get_chatgpt_response(user_message, language=user_language)
                    self.bot.reply_to(message, response)
                    
                    voice_response_path = generate_voice_message(response, user_language)
                    if voice_response_path:
                        with open(voice_response_path, 'rb') as voice_response:
                            self.bot.send_voice(message.chat.id, voice_response)
                        os.remove(voice_response_path)
                    
                finally:
                    if os.path.exists(voice_file_path):
                        os.remove(voice_file_path)
            
            elif message.content_type == 'text':
                response = get_chatgpt_response(message.text, language=user_language)
                self.bot.reply_to(message, response)
                
                voice_response_path = generate_voice_message(response, user_language)
                if voice_response_path:
                    with open(voice_response_path, 'rb') as voice_response:
                        self.bot.send_voice(message.chat.id, voice_response)
                    os.remove(voice_response_path)
            
        except Exception as e:            
            error_message = handle_error(e)
            self.bot.reply_to(message, error_message)

    def run(self):        
        self.bot.polling(none_stop=True)
