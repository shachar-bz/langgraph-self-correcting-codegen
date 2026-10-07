from typing import Optional, TypedDict


class GraphState(TypedDict):
    query_name: str
    query_text: str
    data_file_descriptions: str
    validate_module_path: str
    validate_function_name: str
    gen_prompt: str
    current_program: str
    attempt: int
    last_success: bool
    last_output: Optional[dict]
    last_error: str
    last_reflection: str


def initial_state() -> GraphState:
    return {
        "query_name": "",
        "query_text": "",
        "data_file_descriptions": "",
        "validate_module_path": "",
        "validate_function_name": "",
        "gen_prompt": "",
        "current_program": "",
        "attempt": 1,
        "last_success": False,
        "last_output": None,
        "last_error": "",
        "last_reflection": "",
    }
