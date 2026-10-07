import json

def top_spender_answer(answer) -> bool:
    """
    Validates the answer to the top-spender query.
    Returns True if the answer is correct, False otherwise.
    """
    if isinstance(answer, str):
        try:
            answer = json.loads(answer)
        except json.JSONDecodeError:
            return False

    if not isinstance(answer, dict):
        return False

    required_fields = {"FirstName", "LastName", "City", "TotalSpent"}
    if not required_fields.issubset(answer.keys()):
        return False

    if answer.get("FirstName") != "Oren":
        return False
    if answer.get("LastName") != "Levi":
        return False
    if answer.get("City") != "Haifa":
        return False

    try:
        total = float(answer.get("TotalSpent", 0))
        if abs(total - 572.47) > 0.01:
            return False
    except (TypeError, ValueError):
        return False

    return True
