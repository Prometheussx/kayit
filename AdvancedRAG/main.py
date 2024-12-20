from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage, AIMessage
from graph.graph import app
import langid
from langdetect import detect
# Kullanıcı bilgilerini saklamak için bir sözlük
user_info = {}

# Kullanıcı adını ve mesleğini al
def get_user_info(user_input,name,job):
    """Kullanıcı adını ve mesleğini al."""

    # Kullanıcı bilgilerini sakla
    user_info['name'] = name
    user_info['job'] = job


def handle_user_input(user_input: str, language: str, name, job):
    """Kullanıcıdan gelen girdi ile yanıt üret."""
    # Kullanıcı adı ve mesleğini al
    if not user_info:
        get_user_info(user_input,name,job)

    # Kullanıcı bilgilerini prompt ile birleştir
    history_text = f"User Name: {user_info['name']}, User Job: {user_info['job']}"
    language = f"Language: {language}"
    # Modelin yanıtını al (Graph kullanarak)
    response = app.invoke(input={"question": user_input, "history": history_text, "language": language})

    # Eğer response bir liste döndüyse, listeyi string'e çevir
    if isinstance(response, list):
        response = " ".join(str(r) for r in response)
    elif not isinstance(response, str):  # Eğer başka bir tipse, string'e dönüştür
        response = str(response)

    # Modelin yanıtını döndür
    return response


