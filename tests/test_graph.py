"""End-to-end graph runs with a scripted fake LLM (no network, no API key)."""
import json
from pathlib import Path

from codegen import nodes
from codegen.graph import build_graph
from codegen.state import initial_state

GOOD_PROGRAM = (Path(__file__).resolve().parent.parent
                / "examples" / "top-spender" / "top-spender.py").read_text(encoding="utf-8")
WRONG_PROGRAM = (
    'import json\n'
    'print(json.dumps({"FirstName": "X", "LastName": "Y", "City": "Z", "TotalSpent": 1.0}))'
)


def fake_llm(replies):
    """Return an ask_llm replacement that yields the given replies in order."""
    queue = list(replies)
    prompts = []

    def ask(prompt):
        prompts.append(prompt)
        return queue.pop(0)

    ask.prompts = prompts
    return ask


def test_succeeds_on_first_attempt(workdir, monkeypatch):
    monkeypatch.setattr(nodes, "ask_llm", fake_llm([f"```python\n{GOOD_PROGRAM}\n```"]))

    final = build_graph().invoke(initial_state())

    assert final["last_success"] is True and final["attempt"] == 1
    assert json.loads((workdir / "top-spender_answer.txt").read_text())["FirstName"] == "Oren"
    assert (workdir / "top-spender_errors.txt").read_text() == ""
    assert (workdir / "top-spender_reflect.txt").read_text() == ""


def test_reflects_and_recovers_after_wrong_answer(workdir, monkeypatch):
    ask = fake_llm([WRONG_PROGRAM, "The totals ignored order status.", GOOD_PROGRAM])
    monkeypatch.setattr(nodes, "ask_llm", ask)

    final = build_graph().invoke(initial_state())

    assert final["last_success"] is True and final["attempt"] == 2
    assert "The totals ignored order status." in ask.prompts[2]
    assert "Oren" in (workdir / "top-spender_answer.txt").read_text()


def test_gives_up_after_max_iterations(workdir, monkeypatch):
    # attempt 1 generates, then 4 x (reflect, regenerate) -> 9 LLM calls
    replies = [WRONG_PROGRAM] + ["reflection", WRONG_PROGRAM] * 4
    monkeypatch.setattr(nodes, "ask_llm", fake_llm(replies))

    final = build_graph().invoke(initial_state())

    assert final["last_success"] is False and final["attempt"] == 5
    assert (workdir / "top-spender_answer.txt").read_text() == ""
    assert "INCORRECT answer" in (workdir / "top-spender_errors.txt").read_text()
    assert (workdir / "top-spender_reflect.txt").read_text() == "reflection"
