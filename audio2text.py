from google.cloud import speech_v1p1beta1 as speech
import os

duration = 3  # Duración de la grabación en segundos
sample_rate = 48000  # Tasa de muestreo de audio
channels = 2  # Número de canales de audio (estéreo)

def transcribe_audio(audio_file):
    # Configuración de autenticación
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Isaac\Documents\Python Scripts\translator\googlecredentials.json'
    client = speech.SpeechClient()



    # Transcribir audio a texto utilizando la API de Google Cloud Speech-to-Text
    with open(audio_file, "rb") as audio_data:
        speech_content = audio_data.read()

    audio = speech.RecognitionAudio(content=speech_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code="es-ES",audio_channel_count=2
    )

    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript

transcript = transcribe_audio(r'C:\Users\Isaac\Documents\Python Scripts\discord\recording.wav')


