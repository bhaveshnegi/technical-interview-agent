from langgraph.graph import StateGraph, END

from states.interview_state import InterviewState

from nodes.resume_analyzer_node import resume_analyzer_node

from agents.interviewer_agent import interviewer_agent
from agents.evaluator_agent import evaluator_agent
from agents.followup_agent import followup_agent


def build_graph():

    builder = StateGraph(InterviewState)

    builder.add_node("resume_analyzer", resume_analyzer_node)
    builder.add_node("interviewer", interviewer_agent)
    builder.add_node("evaluate", evaluator_agent)
    builder.add_node("followup", followup_agent)

    builder.set_entry_point("resume_analyzer")

    builder.add_edge("resume_analyzer", "interviewer")
    builder.add_edge("interviewer", "evaluate")
    builder.add_edge("evaluate", "followup")
    builder.add_edge("followup", "interviewer")

    return builder.compile()