from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore"] = Field(
        ...,
        description="Given a user question choose to route vectorstore.",
    )


llm = ChatOpenAI(temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You specialize in redirecting a user question to a vector repository.\n
The vector repository contains documents related to intermediaries, the life of the Prophet Muhammad, the Quran, Islamic history and the history of Islamic science.
Use the vector repository for questions on these topics."""
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router