from codegen import config


def parse_query_input(path: str = config.QUERY_INPUT_FILE) -> tuple[str, list[tuple[str, str]]]:
    """Parse query_input.txt into (query_name, [(data_file, description), ...])."""
    with open(path, "r", encoding="utf-8") as query_input_file:
        lines = query_input_file.readlines()

    query_name = lines[0].split(":", 1)[1].strip()
    data_files = []
    current_filename = None
    current_description_lines = []

    for raw_line in lines[1:]:
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("data_file:"):
            if current_filename is not None:
                data_files.append((current_filename, "\n".join(current_description_lines)))
            current_filename = line.split(":", 1)[1].strip()
            current_description_lines = []
        elif current_filename is not None:
            current_description_lines.append(line)

    if current_filename is not None:
        data_files.append((current_filename, "\n".join(current_description_lines)))

    return query_name, data_files


def format_data_file_descriptions(data_files: list[tuple[str, str]]) -> str:
    return "\n\n".join(
        f"File: {filename}\nDescription: {description}"
        for filename, description in data_files
    )


def validator_names(query_name: str) -> tuple[str, str]:
    """Hyphens become underscores: top-spender -> (top_spender_validate.py, top_spender_answer)."""
    base = query_name.replace("-", "_")
    return f"{base}_validate.py", f"{base}_answer"
