from dotenv import load_dotenv

from langgraph.graph import END, StateGraph

from graph.chains.answer_grader import answer_grader
from graph.chains.router import question_router, RouteQuery
from graph.node_constants import RETRIEVE, GRADE_DOCUMENTS, GENERATE
from graph.nodes import generate, grade_documents, retrieve
from graph.state import GraphState

load_dotenv()


def decide_to_generate(state):
    print("---ASSESS GRADED DOCUMENTS---")

    print("---DECISION: GENERATE---")
    return GENERATE


def grade_generation_against_question(state: GraphState) -> str:
    print("---GRADE GENERATION vs QUESTION---")
    question = state["question"]
    generation = state["generation"]

    score = answer_grader.invoke({"question": question, "generation": generation})
    if answer_grade := score.binary_score:
        print("---DECISION: GENERATION ADDRESSES QUESTION---")
        return "useful"
    else:
        print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
        return "not useful"


def route_question(state: GraphState) -> str:
    print("---ROUTE QUESTION---")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})
    return RETRIEVE


workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)

workflow.set_conditional_entry_point(
    route_question,
    {
        RETRIEVE: RETRIEVE,
    },
)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        GENERATE: GENERATE,
    },
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_against_question,
    {
        "useful": END,
        "not useful": END,
    },
)
workflow.add_edge(GENERATE, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
