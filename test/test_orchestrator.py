from orchestrator import decide_next_step

def test_decision_flow():
    print("Running decision engine tests...")
    
    # Test initial step
    state = {"question_index": 0, "last_action": None}
    assert decide_next_step(state) == "ask"
    print("Test 1 passed: Start -> ask")

    # Test ask -> evaluate
    state = {"question_index": 1, "last_action": "ask"}
    assert decide_next_step(state) == "evaluate"
    print("Test 2 passed: ask -> evaluate")

    # Test evaluate -> followup (low score)
    state = {
        "question_index": 1,
        "last_action": "evaluate",
        "evaluation": {
            "cat1": {"score": 2, "feedback": "bad"}
        }
    }
    assert decide_next_step(state) == "followup"
    print("Test 3 passed: evaluate (low) -> followup")

    # Test evaluate -> ask (high score, not yet 5)
    state = {
        "question_index": 2,
        "last_action": "evaluate",
        "evaluation": {
            "cat1": {"score": 8, "feedback": "good"}
        }
    }
    assert decide_next_step(state) == "ask"
    print("Test 4 passed: evaluate (high) -> ask")

    # Test evaluate -> end (reached 5)
    state = {
        "question_index": 5,
        "last_action": "evaluate",
        "evaluation": {
            "cat1": {"score": 8, "feedback": "good"}
        }
    }
    assert decide_next_step(state) == "end"
    print("Test 5 passed: evaluate (5+) -> end")

    # Test followup -> evaluate
    state = {"question_index": 1, "last_action": "followup"}
    assert decide_next_step(state) == "evaluate"
    print("Test 6 passed: followup -> evaluate")

    print("\nAll decision flow tests passed!")

if __name__ == "__main__":
    test_decision_flow()
