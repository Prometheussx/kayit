from typing import Any, Dict

from graph.chains.generation import generation_chain
from graph.state import GraphState


def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    history = state["history"]
    language = state["language"]

    generation = generation_chain.invoke({"context": documents, "question": question, "history": history, "language": language})
    return {"documents": documents, "history": history, "language": language, "question": question, "generation": generation}
