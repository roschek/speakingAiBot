def send_welcome_message(bot, message):
    user_language = message.from_user.language_code
    welcome_text = {
        'en': "Hello! I am your language coach. I can help you improve your conversational skills.",
        'ru': "Привет! Я ваш языковой тренер. Я помогу вам улучшить разговорные навыки.",        
    }
    bot.send_message(message.chat.id, welcome_text.get(user_language, welcome_text['en']))