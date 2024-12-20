from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
from main import handle_user_input
# .env dosyasını yükle
load_dotenv()

# API anahtarını almak ve kontrol etmek
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# FastAPI uygulamasını başlat
app = FastAPI()


# Kullanıcı girdisi için veri modeli
class UserInput(BaseModel):
    name: str
    job: str
    user_input: str


def translate_text(text: str) -> str:
    # Çeviri için kullanılacak mesaj dizisi
    prompt = f"Please determine the language of the following text: {text}. The language that the words in the text belong to or the language that the whole text resembles. Just rotate the language and do not write anything else."
    response = openai.chat.completions.create(
        model="gpt-4",  # veya gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ]
    )
    language = response.choices[0].message.content
    return language




@app.post("/process-input/")
async def process_input(data: UserInput):
    try:
        # Dil algılamayı yap
        detected_language = translate_text(data.user_input)

        # Kullanıcı mesajını işleyip yanıt almak için fonksiyonu çağır
        main = handle_user_input(data.user_input, detected_language, data.name, data.job)

        return {"message": main}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Uygulama çalıştırılacak
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5353)
