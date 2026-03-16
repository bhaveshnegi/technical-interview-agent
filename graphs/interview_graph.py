from langgraph.graph import StateGraph, END

from states.interview_state import InterviewState

from nodes.resume_analyzer_node import resume_analyzer_node
from nodes.interview_controller_node import interview_controller_node

from agents.interviewer_agent import interviewer_agent
from agents.evaluator_agent import evaluator_agent
from agents.followup_agent import followup_agent
from agents.report_agent import report_agent


def build_graph():

    builder = StateGraph(InterviewState)

    builder.add_node("resume_analyzer", resume_analyzer_node)
    builder.add_node("interviewer", interviewer_agent)
    builder.add_node("evaluate", evaluator_agent)
    builder.add_node("followup", followup_agent)
    builder.add_node("controller", interview_controller_node)
    builder.add_node("report_agent", report_agent)

    builder.set_entry_point("resume_analyzer")

    builder.add_edge("resume_analyzer", "interviewer")
    builder.add_edge("interviewer", "evaluate")
    builder.add_edge("evaluate", "followup")
    builder.add_edge("followup", "controller")

    def route_interview(state: InterviewState):
        if state.get("interview_complete"):
            return "report_agent"
        return "interviewer"

    builder.add_conditional_edges(
        "controller",
        route_interview,
        {
            "report_agent": "report_agent",
            "interviewer": "interviewer"
        }
    )

    builder.add_edge("report_agent", END)

    return builder.compile()