import os
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_DIR = Path(__file__).parent
TEMP_DIR = BASE_DIR / "temp"

TEMP_DIR.mkdir(exist_ok=True)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("TALKING_SERVICE")

DEFAULT_LANGUAGE = "ru"
SUPPORTED_LANGUAGES = {
    "ru": "Русский",
    "en": "English",
    "he": "עברית"
}

ERROR_MESSAGES = {
    'general_error': "Произошла ошибка при обработке вашего запроса. Попробуйте позже.",
    'voice_recognition_error': "Не удалось распознать голосовое сообщение. Попробуйте еще раз.",
}

MAX_MESSAGE_LENGTH = 4096

WELCOME_MESSAGES = {
    "ru": (
        "Здравствуйте! Я ваш персональный преподаватель русского языка.\n\n"
        "Я помогу вам:\n"
        "• Улучшить разговорную речь\n"
        "• Расширить словарный запас\n"
        "• Освоить грамматику\n"
        "• Понять культурный контекст\n\n"
        "Давайте начнем! Расскажите, почему вы решили изучать русский язык?"
    ),
    "en": (
        "Hello! I'm your personal English language teacher.\n\n"
        "I will help you:\n"
        "• Improve your speaking skills\n"
        "• Expand your vocabulary\n"
        "• Master grammar\n"
        "• Understand cultural context\n\n"
        "Let's begin! Tell me why you decided to learn English?"
    ),
    "he": (
        "שלום! אני המורה הפרטי שלך לעברית\n\n"
        ":אני אעזור לך\n"
        "• לשפר את הדיבור\n"
        "• להרחיב את המילון שלך\n"
        "• להשלים את הגרמנית\n"
        "• להבין את ההקשר הספרדי\n\n"
        "!שלום! אני המורה הפרטי שלך לעברית\n\n"
        ":אני אעזור לך\n"
        "• לשפר את הדיבור\n"
        "• להרחיב את המילון שלך\n"
        "• להשלים את הגרמנית\n"
        "• להבין את ההקשר הספרדי\n\n"
    )
}

VOICE_IDS = {
    "ru": "2EiwWnXFnvU5JabPnv8n",  # Anna
    "en": "21m00Tcm4TlvDq8ikWAM",  # Rachel
    "he": "IKne3meq5aSn9XLyUdCD"   # Josh
}

DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "Rachel")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "eleven_monolingual_v2")

VOICE_SETTINGS = {
    "ru": {
        "voice": "pNInz6obpgDQGcFmaJgB",  # Anna
        "model": "eleven_multilingual_v1"
    },
    "en": {
        "voice": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "model": "eleven_multilingual_v1"
    },
    "he": {
        "voice": "AZnzlk1XvdvUeBnXmlld",  # Adam
        "model": "eleven_multilingual_v1"
    }
}

headers = {
    "Accept": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY
}

response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
voices = response.json()
for voice in voices["voices"]:
    print(f"{voice['name']}: {voice['voice_id']}")