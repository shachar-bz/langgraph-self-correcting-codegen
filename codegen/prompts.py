from langchain_core.prompts import PromptTemplate

GEN_QUERY_PROGRAM_PROMPT = PromptTemplate.from_template(
    """
You are an expert Python programmer. Write a complete, standalone Python program 
that answers the following query :
{query_text}

Here are the data files, their descriptions, and structure:
{data_file_descriptions}

Each subsequent line contains values in the same order as specified at the message -  "Each line is of the form"


STRICT RULES:
- Use the data files by their name and structure as specified in the message. Do NOT assume any other structure or file names.
- Print ONLY a single JSON object to stdout as the final output.
- Do NOT print anything else — no "Loading...", no debug output, no extra text.
- Do NOT write any files — only print to stdout.
- Use csv or pandas modules to read the files.
- Import json and use json.dumps() to print the result.
- The JSON must contain exactly the fields specified in the query.
"""
)


REFLECT_ON_ERR_PROMPT = PromptTemplate.from_template(
    """
You are a Python debugging expert. Do NOT write new code yet.
Carefully analyze the error and explain in detail:
- What caused the error or incorrect output
- What needs to be changed in the program to fix it
- Be specific about line numbers or logic errors if possible.

Original code-generation prompt:
{gen_prompt}

Program that failed:
{current_program}

Error message:
{last_error}
"""
)


REGEN_QUERY_PROGRAM_PROMPT = PromptTemplate.from_template(
    """
You are an expert Python programmer. Write a complete, standalone Python program 
that answers the following query :
{query_text}

Here are the data files, their descriptions, and structure:
{data_file_descriptions}

Each subsequent line contains values in the same order as specified at the message -  "Each line is of the form"

The previous program that failed:
{current_program}

Here is the reason the previous program failed:
{last_reflection}

STRICT RULES:
- Use the data files by their name and structure as specified in the message. Do NOT assume any other structure or file names.
- Print ONLY a single JSON object to stdout as the final output.
- Do NOT print anything else — no "Loading...", no debug output, no extra text.
- Do NOT write any files — only print to stdout.
- Use csv or pandas modules to read the files.
- Import json and use json.dumps() to print the result.
- The JSON must contain exactly the fields specified in the query.
"""
)
