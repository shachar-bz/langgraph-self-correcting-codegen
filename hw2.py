"""Entry point: run from a directory containing query_input.txt and the data files.

    cd sample_data && python ../hw2.py
"""
from codegen.graph import build_graph
from codegen.state import initial_state

if __name__ == "__main__":
    build_graph().invoke(initial_state())
