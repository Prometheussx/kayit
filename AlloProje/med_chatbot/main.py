import streamlit as st
from dotenv import load_dotenv
from graph.graph import app
import time
from openai import OpenAI

client = OpenAI()
from langchain_openai import ChatOpenAI
import os

# .env dosyasını yükle
load_dotenv()

# OpenAI API anahtarını ayarla
client.api_key = os.getenv("OPENAI_API_KEY")


def translate_text(text, target_language):
    # Çeviri için kullanılacak mesaj dizisi
    prompt = f"Translate the following text to {target_language}: {text}"
    response = client.chat.completions.create(
        model="gpt-4",  # veya gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful translator.You will only translate the text you receive into Türkçeye, never changing or adding anything.If the incoming text is in Turkish, you will write directly without applying any changes without adding or subtracting in any way."},
            {"role": "user", "content": prompt}
        ]
    )
    return response


# CSS ile yazma efektleri ekleme
st.markdown("""
    <style>
    .user-message, .bot-message {
        color: white;
        background-color: #333333;
        padding: 10px;
        border-radius: 15px;
        max-width: 70%;
        margin: 5px;
    }
    .user-message {
        text-align: right;
        margin-left: auto;
    }
    .bot-message {
        text-align: left;
        margin-right: auto;
    }
    .chatbox {
        display: flex;
        align-items: flex-end;
    }
    .typing-indicator-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
    .typing-indicator {
        width: 10px;
        height: 10px;
        background-color: #ffffff;
        border-radius: 50%;
        animation: typing 1s infinite alternate;
    }
    .typing-indicator.solid {
        animation: solid 1s infinite;
    }
    .typing-indicator.fade-in-out {
        animation: fadeInOut 1s infinite;
    }
    @keyframes typing {
        0%, 100% { opacity: 0.2; }
        50% { opacity: 1; }
    }
    @keyframes solid {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    @keyframes fadeInOut {
        0% { opacity: 0; }
        50% { opacity: 1; }
        100% { opacity: 0; }
    }
    </style>
""", unsafe_allow_html=True)

# Mesajlar için başlangıç durumu
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "bot", "text": "Merhabalar! Nasıl yardımcı olabilirim?"}]

# Kullanıcıdan girdi al
user_input = st.text_input("Sorunuzu yazın ve Enter'a basın", "")

# Kullanıcı mesajı ekle
if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    st.session_state.messages.append({"role": "bot", "text": '<div class="typing-indicator-container">'
                                                             '<div class="typing-indicator"></div>'
                                                             '<div class="typing-indicator solid"></div>'
                                                             '<div class="typing-indicator fade-in-out"></div>'
                                                             '</div>'})

# Chatbox'u temizle
chat_placeholder = st.empty()

# Mesajları gösterme
with chat_placeholder.container():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chatbox">
                <div class="user-message">{message['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chatbox">
                <div class="bot-message">{message['text']}</div>
            </div>
            """, unsafe_allow_html=True)

# Bot cevabı için bekleme süresi
if user_input:
    time.sleep(2)  # Yazma efekti süresi

    # Yazma efektini kaldır ve gerçek cevabı ekle
    st.session_state.messages.pop()
    response = app.invoke(input={"question": user_input})
    api_response = response['generation']

    # Çeviriyi yap
    translated_response = translate_text(api_response, target_language="turkish")

    st.session_state.messages.append({"role": "bot", "text": translated_response})

    # Mesajları yeniden göster
    with chat_placeholder.container():
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chatbox">
                    <div class="user-message">{message['text']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chatbox">
                    <div class="bot-message">{message['text']}</div>
                </div>
                """, unsafe_allow_html=True)
