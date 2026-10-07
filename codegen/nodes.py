import json

from openai import BadRequestError

from codegen import config
from codegen.executor import run_program
from codegen.llm import ask_llm, strip_code_fences
from codegen.prompts import (
    GEN_QUERY_PROGRAM_PROMPT,
    REFLECT_ON_ERR_PROMPT,
    REGEN_QUERY_PROGRAM_PROMPT,
)
from codegen.query_spec import (
    format_data_file_descriptions,
    parse_query_input,
    validator_names,
)
from codegen.state import GraphState, initial_state
from codegen.validation import validate_answer


def _generate_code(prompt: str, stage: str) -> dict:
    """Ask the LLM for a program; on a content-filter block, return an error update instead."""
    try:
        code = strip_code_fences(ask_llm(prompt))
    except BadRequestError as error:
        return {
            "last_success": False,
            "last_output": None,
            "last_error": f"{config.CONTENT_FILTER_ERROR_PREFIX} during {stage}: {error}",
        }
    # Clear a stale content-filter error so routing proceeds to execution.
    return {"current_program": code, "last_error": ""}


def get_query_details(state: GraphState) -> dict:
    print("** Entering GetQueryDetails Tool **")

    query_name, data_files = parse_query_input()
    with open(f"{query_name}.txt", "r", encoding="utf-8") as query_file:
        query_text = query_file.read()
    validate_module_path, validate_function_name = validator_names(query_name)

    return {
        **initial_state(),
        "query_name": query_name,
        "query_text": query_text,
        "data_file_descriptions": format_data_file_descriptions(data_files),
        "validate_module_path": validate_module_path,
        "validate_function_name": validate_function_name,
    }


def gen_query_program(state: GraphState) -> dict:
    print("** Entering GenQueryProgram Tool **")

    prompt = GEN_QUERY_PROGRAM_PROMPT.format(
        query_text=state["query_text"],
        data_file_descriptions=state["data_file_descriptions"],
    ).strip()

    update = _generate_code(prompt, "generation")
    update.setdefault("current_program", "")
    return {"gen_prompt": prompt, **update}


def execute_program(state: GraphState) -> dict:
    print("** Entering ExecuteProgram Tool **")

    program_path = f"{state['query_name']}.py"
    with open(program_path, "w", encoding="utf-8") as program_file:
        program_file.write(state["current_program"])

    answer, error = run_program(program_path)
    if answer is None:
        return {"last_success": False, "last_output": None, "last_error": error}

    if validate_answer(state["validate_module_path"], state["validate_function_name"], answer):
        return {"last_success": True, "last_output": answer, "last_error": ""}

    return {
        "last_success": False,
        "last_output": answer,
        "last_error": (
            "The program ran successfully but produced an INCORRECT answer. "
            "The validator returned False. "
            f"The incorrect output was: {json.dumps(answer)}"
        ),
    }


def chk4r_err(state: GraphState) -> GraphState:
    print("** Entering Chk4rErr Tool **")
    return state


def reflect_on_err(state: GraphState) -> dict:
    print("** Entering ReflectOnErr Tool **")

    prompt = REFLECT_ON_ERR_PROMPT.format(
        gen_prompt=state["gen_prompt"],
        current_program=state["current_program"],
        last_error=state["last_error"],
    ).strip()

    try:
        reflection = ask_llm(prompt)
    except BadRequestError:
        reflection = (
            "The previous LLM request was blocked by Azure content filtering. "
            "Regenerate the program using neutral, task-focused wording while preserving "
            "the required JSON-only output behavior."
        )
    return {"last_reflection": reflection}


def regen_query_pgm(state: GraphState) -> dict:
    print("** Entering ReGenQueryPgm Tool **")

    prompt = REGEN_QUERY_PROGRAM_PROMPT.format(
        query_text=state["query_text"],
        data_file_descriptions=state["data_file_descriptions"],
        current_program=state["current_program"],
        last_reflection=state["last_reflection"],
    ).strip()

    return {"attempt": state["attempt"] + 1, **_generate_code(prompt, "regeneration")}
