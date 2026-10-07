import json
import os

from codegen.state import GraphState


def _write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.write(content)


def finalize(state: GraphState) -> GraphState:
    """Write <query>.py, <query>_answer.txt, <query>_errors.txt and <query>_reflect.txt."""
    print("** Entering Finalize Tool **")

    query_name = state["query_name"]
    program_file = f"{query_name}.py"
    answer_file = f"{query_name}_answer.txt"

    if not os.path.exists(program_file):
        _write(program_file, state["current_program"])

    if state["last_success"] is True:
        answer_json = json.dumps(state["last_output"])
        _write(answer_file, answer_json)
        _write(f"{query_name}_errors.txt", "")
        _write(f"{query_name}_reflect.txt", "")
        print(f"Successfully generated program that computed solution. Solution in {answer_file}")
        print(f"Answer is {answer_json}")
    else:
        _write(answer_file, "")
        _write(f"{query_name}_errors.txt", state["last_error"])
        _write(f"{query_name}_reflect.txt", state["last_reflection"])
        print(f"Failed to produce a correct answer after {state['attempt']} attempt(s).")

    return state
