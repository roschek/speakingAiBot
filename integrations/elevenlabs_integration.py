import requests
import config
import os
import logging

logger = logging.getLogger(__name__)

def generate_voice_message(text: str, language: str = "ru") -> str:
    try:
        voice_settings = config.VOICE_SETTINGS.get(language, config.VOICE_SETTINGS['en'])
        
        url = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/stream".format(
            voice=voice_settings['voice']
        )
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": config.ELEVENLABS_API_KEY
        }
        
        data = {
            "text": text,
            "model_id": voice_settings['model'],
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            file_path = os.path.join(config.TEMP_DIR, f"response_{hash(text)}.mp3")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return file_path
        else:
            logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error generating voice message: {str(e)}")
        return None