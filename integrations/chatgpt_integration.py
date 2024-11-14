from openai import OpenAI
import config
import logging

logger = logging.getLogger(__name__)

def get_chatgpt_response(message: str, language: str = "ru") -> str:
    """
    Получить ответ от ChatGPT
    
    Args:
        message (str): Сообщение пользователя
        language (str, optional): Язык ответа. По умолчанию "ru"
    
    Returns:
        str: Ответ от ChatGPT
    """
    try:
        # Инициализация клиента
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        # Формирование системного сообщения с указанием языка
        system_message = f"""You are a highly qualified {language} language teacher with years of experience.
        Your task is to engage in a conversational language learning dialogue with the student.

        Key aspects of your role:
        1. First, assess the student's language level through natural conversation
        2. Adapt your language complexity to match the student's level
        3. Correct mistakes gently and explain why something was wrong
        4. Encourage speaking practice through engaging dialogue
        5. Introduce new vocabulary and grammar naturally in context
        6. Always respond in {language}
        7. Keep the conversation natural and engaging
        8. Use topics relevant to daily life
        9. Provide cultural context when appropriate
        10. Remember previous context in the conversation

        If you notice mistakes:
        - Point them out politely
        - Explain the correction
        - Provide the correct form
        - Give an example of proper usage

        Teaching style:
        - Be patient and encouraging
        - Use positive reinforcement
        - Make the student feel comfortable
        - Keep the conversation flowing naturally
        - Ask follow-up questions to encourage speaking
        """
        
        # Отправка запроса к API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": message}
            ]
        )
        
        # Получение ответа
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от ChatGPT: {str(e)}")
        raise