from langgraph.graph import StateGraph
from builder.state import AgentState
from builder.nodes import sql_generator, sql_executor, chart_generator, narrator, decider, general_chat

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("decider", decider)
    graph.add_node("sql_generator", sql_generator)
    graph.add_node("sql_executor", sql_executor)
    graph.add_node("chart_generator", chart_generator)
    graph.add_node("narrator", narrator)
    graph.add_node("general_chat", general_chat)

    graph.set_entry_point("decider")

    graph.add_conditional_edges(
        "decider",
        lambda state: state["route"],
        {
            "sql": "sql_generator",
            "chat": "general_chat",
        },
    )

    graph.add_edge("sql_generator", "sql_executor")
    graph.add_edge("sql_executor", "chart_generator")
    graph.add_edge("sql_executor", "narrator")

    return graph.compile()
