from typing import TypedDict, List, Optional, Any


class InterviewState(TypedDict):

    # resume data
    resume_text: str
    skills: List[str]
    projects: List[str]

    # interview flow
    question_list: List[str]
    resume_index: Optional[Any]
    current_question: Optional[str]

    # candidate interaction
    candidate_answer: Optional[str]

    # evaluation
    score: Optional[int]
    feedback: Optional[str]

    # conversation memory
    conversation_history: List[str]

    # interview progress
    question_index: int
    interview_complete: bool