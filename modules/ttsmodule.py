"""tts module"""
from google.cloud import texttospeech

class LanguageCode:
    """tts lang code"""
    english = "en-US"
    korean = "ko-KR"
    japanese = "ja-JP"

def save_tts_file(text: str, name: str, language: LanguageCode=LanguageCode.english):
    """
    save tts file with name

    Param:
    text: str = tts text
    name: str = file name
    language: language_code = tts lang, default=language_code.english
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(name, "wb") as out:
        out.write(response.audio_content)
