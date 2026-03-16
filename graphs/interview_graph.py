from langgraph.graph import StateGraph, END

from states.interview_state import InterviewState

from nodes.resume_parser_node import resume_parser_node
from nodes.question_generator_node import question_generator_node
from nodes.ask_question_node import ask_question_node
from nodes.scoring_node import scoring_node

from agents.interviewer_agent import interviewer_agent
from agents.evaluator_agent import evaluator_agent
from agents.followup_agent import followup_agent

from routing.interview_router import interview_router


def build_graph():

    builder = StateGraph(InterviewState)

    builder.add_node("resume_parser", resume_parser_node)
    builder.add_node("generate_questions", question_generator_node)
    builder.add_node("ask_question", ask_question_node)
    builder.add_node("score_answer", scoring_node)

    builder.add_node("interviewer", interviewer_agent)
    builder.add_node("evaluate", evaluator_agent)
    builder.add_node("followup", followup_agent)

    builder.set_entry_point("resume_parser")

    builder.add_edge("resume_parser", "generate_questions")
    builder.add_edge("generate_questions", "ask_question")
    builder.add_edge("ask_question", "score_answer")
     
    builder.add_edge("interviewer", "evaluate")
    builder.add_edge("evaluate", "followup")
    builder.add_edge("followup", "interviewer")

    builder.add_conditional_edges(
        "score_answer",
        interview_router,
        {
            "next_question": "ask_question",
            "end": END
        }
    )

    return builder.compile()