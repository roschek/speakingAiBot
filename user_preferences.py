from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

user_preferences: Dict[int, Dict[str, str]] = {}

def get_user_language(user_id: int) -> Optional[str]:    
    return user_preferences.get(user_id, {}).get('language')

def set_user_language(user_id: int, language: str) -> None:    
    if user_id not in user_preferences:
        user_preferences[user_id] = {}
    user_preferences[user_id]['language'] = language
    logger.info(f"Установлен язык {language} для пользователя {user_id}") 