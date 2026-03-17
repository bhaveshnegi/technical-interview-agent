def hr_scoring_tool(interview_data: dict):
    """
    Computes a structured HR screening scorecard based on provided interview data.
    
    Args:
        interview_data (dict): A dictionary containing 'communication', 'interest', and 'cultural_fit' assessments.
        
    Returns:
        dict: A structured scorecard with scores (0-10) and feedback for each category.
    """
    scorecard = {
        "Communication": {
            "score": interview_data.get("communication_score", 0),
            "feedback": interview_data.get("communication_feedback", "No feedback provided.")
        },
        "Interest & Motivation": {
            "score": interview_data.get("interest_score", 0),
            "feedback": interview_data.get("interest_feedback", "No feedback provided.")
        },
        "Cultural Alignment": {
            "score": interview_data.get("cultural_fit_score", 0),
            "feedback": interview_data.get("cultural_fit_feedback", "No feedback provided.")
        },
        "Overall HR Recommendation": ""
    }
    
    avg_score = (scorecard["Communication"]["score"] + 
                 scorecard["Interest & Motivation"]["score"] + 
                 scorecard["Cultural Alignment"]["score"]) / 3
                 
    if avg_score >= 8:
        scorecard["Overall HR Recommendation"] = "Strong Hire - Proceed to Technical Rounds."
    elif avg_score >= 5:
        scorecard["Overall HR Recommendation"] = "Waitlist - Consider for other roles."
    else:
        scorecard["Overall HR Recommendation"] = "Do Not Proceed - Poor fit/communication."
        
    return scorecard

if __name__ == "__main__":
    # Example usage
    data = {
        "communication_score": 8,
        "communication_feedback": "Clear and concise.",
        "interest_score": 9,
        "interest_feedback": "Very enthusiastic about the company mission.",
        "cultural_fit_score": 7,
        "cultural_fit_feedback": "Professional but seemed a bit reserved."
    }
    print(hr_scoring_tool(data))
