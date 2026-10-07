from langgraph.graph import END, StateGraph

from codegen import config
from codegen.nodes import (
    chk4r_err,
    execute_program,
    gen_query_program,
    get_query_details,
    reflect_on_err,
    regen_query_pgm,
)
from codegen.output import finalize
from codegen.state import GraphState


def route_after_generation(state: GraphState) -> str:
    if state["last_error"].startswith(config.CONTENT_FILTER_ERROR_PREFIX):
        return "check"
    return "execute"


def route_after_check(state: GraphState) -> str:
    if state["last_success"] is True or state["attempt"] >= config.MAX_ITERATION:
        return "finalize"
    return "retry"


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("GetQueryDetails", get_query_details)
    graph.add_node("GenQueryProgram", gen_query_program)
    graph.add_node("ExecuteProgram", execute_program)
    graph.add_node("Chk4rErr", chk4r_err)
    graph.add_node("ReflectOnErr", reflect_on_err)
    graph.add_node("ReGenQueryPgm", regen_query_pgm)
    graph.add_node("Finalize", finalize)

    graph.set_entry_point("GetQueryDetails")
    graph.add_edge("GetQueryDetails", "GenQueryProgram")
    generation_routes = {"execute": "ExecuteProgram", "check": "Chk4rErr"}
    graph.add_conditional_edges("GenQueryProgram", route_after_generation, generation_routes)
    graph.add_edge("ExecuteProgram", "Chk4rErr")
    graph.add_conditional_edges(
        "Chk4rErr", route_after_check, {"retry": "ReflectOnErr", "finalize": "Finalize"}
    )
    graph.add_edge("ReflectOnErr", "ReGenQueryPgm")
    graph.add_conditional_edges("ReGenQueryPgm", route_after_generation, generation_routes)
    graph.add_edge("Finalize", END)

    return graph.compile()
