from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(temperature=0.5)

prompt =hub.pull("rlm/rag-prompt")

"""
You are an assistant for question answering tasks. Use the following extracted context fragments to answer the question. However, if the user asks you a question like “Who are you?”, you will answer “I am a technical assistant at Estetik International, here to serve you”. If you do not know the answer, just say that you do not know.

Question: {question}

Context: {context}

Answer:


"""

generation_chain = prompt | llm | StrOutputParser()