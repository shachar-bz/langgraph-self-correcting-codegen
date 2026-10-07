from codegen.executor import run_program
from codegen.llm import strip_code_fences
from codegen.query_spec import parse_query_input, validator_names


def test_strip_code_fences():
    assert strip_code_fences("```python\nprint(1)\n```") == "print(1)"
    assert strip_code_fences("```\nprint(1)\n```") == "print(1)"
    assert strip_code_fences("print(1)") == "print(1)"


def test_parse_query_input(workdir):
    name, files = parse_query_input()
    assert name == "top-spender"
    assert [f for f, _ in files] == ["customers.csv", "orders.csv", "products.csv"]
    assert "CustomerID" in files[0][1]


def test_validator_names():
    assert validator_names("top-spender") == ("top_spender_validate.py", "top_spender_answer")


def test_run_program_success(tmp_path):
    program = tmp_path / "p.py"
    program.write_text('import json; print(json.dumps({"a": 1}))')
    assert run_program(str(program)) == ({"a": 1}, "")


def test_run_program_crash(tmp_path):
    program = tmp_path / "p.py"
    program.write_text("raise RuntimeError('boom')")
    answer, error = run_program(str(program))
    assert answer is None and "boom" in error


def test_run_program_invalid_json(tmp_path):
    program = tmp_path / "p.py"
    program.write_text("print('not json')")
    answer, error = run_program(str(program))
    assert answer is None and "Invalid or empty JSON" in error
