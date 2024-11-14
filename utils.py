import os
import logging
from pathlib import Path
import config

logger = logging.getLogger(__name__)

def handle_error(error: Exception) -> str:
    """Обработка ошибок и возврат сообщения для пользователя"""
    logger.error(f"Ошибка: {str(error)}", exc_info=True)
    return config.ERROR_MESSAGES['general_error']

def cleanup_temp_files(file_path: str) -> None:
    """Очистка временных файлов"""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Временный файл {file_path} удален")
    except Exception as e:
        logger.error(f"Ошибка при удалении файла {file_path}: {str(e)}")

def cleanup_old_temp_files() -> None:
    """Очистка старых временных файлов"""
    try:
        for file in config.TEMP_DIR.glob("*"):
            if file.is_file():
                file.unlink()
        logger.info("Очистка временных файлов завершена")
    except Exception as e:
        logger.error(f"Ошибка при очистке временных файлов: {str(e)}")