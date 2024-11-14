import os
import logging
from openai import OpenAI
import config

logger = logging.getLogger(__name__)

def convert_voice_to_text(voice_file_path: str, language: str = "ru") -> str:
    """
    Конвертирует голосовое сообщение в текст используя OpenAI Whisper
    """
    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        with open(voice_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language
            )
            
        return transcript.text
        
    except Exception as e:
        logger.error(f"Ошибка при конвертации голоса в текст: {str(e)}")
        raise 