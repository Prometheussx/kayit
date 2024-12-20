from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "websearch", "main"] = Field(
        ...,
        description="Determine whether the user's question is personal or objective. If the question is personal, subjective or conversational, like a conversation with you (e.g. “How are you?” “What did you do today?” “My name is Taha, nice to meet you”, “what do you think”, “what should I do today”), redirect to the main system for a more personalized response. If the question is objective and asks for verifiable information (e.g. “What is the capital of France?” or “Who won the 2020 Olympic Games?”), redirect to the vector store or web search for real answers.",
    )


llm = ChatOpenAI(temperature=1)
structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert in handling questions from users in any language correctly, directing the question to main, vector repository or web search.
If the question is personal, subjective, conversational, asked to you individually, personal information, advice, ideas, and conversational, you will answer the question with the help of main.
No matter what language the question is asked in, if the question is about Taget company (what is Taget, what does Taget do, what is its mission) and its products (what is a digital business card, what is a business card, how do I do the first installation, how do I use a business card, how do I set up a card), you will answer the question with the help of vector store. The answer will always be in the same language as the question.
If the question has the slightest connection with vector repository, you will answer the question with the help of vector repository.
Vector repository contains all kinds of information about Taget company, such as ways to contact the support department, details about one of the company's products, frequently asked questions about the initial setup of the digital business card product, how to activate digital business card features, how to use digital business card features, how to activate digital business card box contents, feature information and usage contents and all other product and company information.
Therefore, use vector repository to answer all your questions about Taget or its products.
For all other questions, use web search to provide appropriate answers."""
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router

