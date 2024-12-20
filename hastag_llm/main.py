#!/usr/bin/env python

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv

load_dotenv()

# 1. Create prompt template for both English and Turkish
system_template = (
    "Create relevant hashtags in both English and Turkish based on the profession provided. "
    "Profession: {profession}. "
    "Provide the hashtags in a mixed format, where English and Turkish hashtags are interspersed. "
    "Format: [hashtags]"
)

prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', 'Profession: {profession}')
])

# 2. Create model
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser

# 5. Define input model
class HashtagRequest(BaseModel):
    profession: str

# 6. App definition
app = FastAPI(
    title="Hashtag Generator API",
    version="1.0",
    description="A simple API server to generate hashtags in both English and Turkish based on profession using LangChain and OpenAI.",
)

# 7. Add LangServe routes
add_routes(
    app,
    chain,
    path="/generate_hashtags",  # Define the path for LangServe route
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
