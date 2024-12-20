import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import os
from graph.graph import app
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# OpenAI API anahtarını ayarla
openai.api_key = os.getenv("OPENAI_API_KEY")


def transcribe_text_to_voice(audio_location):
    audio_file= open(audio_location, "rb")
    transcript = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
    user_input = transcript.text
    return user_input



def chat_completion_call(text):
    response = app.invoke(input={"question": text})
    return response['generation']


def text_to_speech_ai(speech_file_path, api_response):
    response = openai.audio.speech.create(model="tts-1",voice="nova",input=api_response)
    response.stream_to_file(speech_file_path)



st.title("🧑‍💻 Alo Fetva 💬 Sesli Asistan")


audio_bytes = audio_recorder()
if audio_bytes:
    ##Save the Recorded File
    audio_location = "audio_file.wav"
    with open(audio_location, "wb") as f:
        f.write(audio_bytes)

    #Transcribe the saved file to text
    text = transcribe_text_to_voice(audio_location)
    st.write(text)

    #Use API to get an AI response
    api_response = chat_completion_call(text)
    st.write(api_response)

    # Read out the text response using tts
    speech_file_path = 'audio_response.mp3'
    text_to_speech_ai(speech_file_path, api_response)
    st.audio(speech_file_path)

