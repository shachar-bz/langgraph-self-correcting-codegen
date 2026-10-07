import importlib.util


def validate_answer(module_path: str, function_name: str, answer: dict) -> bool:
    """Load the query's validator module from disk and call its validation function."""
    module_name = module_path.replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)(answer) is True
