from langgraph.graph import StateGraph
import gradio as gr
import pandas as pd
import os
from langchain_core.tracers import LangChainTracer
from langchain_core.tracers.langchain import wait_for_all_tracers
from state import AgentState
from nodes import sql_generator, sql_executor, chart_generator, narrator

# --- Tracer setup ---
project = os.getenv("LANGCHAIN_PROJECT", "default-project")
tracer = LangChainTracer(project_name=project)

# --- Graph setup ---
graph = StateGraph(AgentState)
graph.add_node("sql_generator", sql_generator)
graph.add_node("sql_executor", sql_executor)
graph.add_node("chart_generator", chart_generator)
graph.add_node("narrator", narrator)

graph.set_entry_point("sql_generator")
graph.add_edge("sql_generator", "sql_executor")
graph.add_edge("sql_executor", "chart_generator")
graph.add_edge("sql_executor", "narrator")

app = graph.compile()

# --- Debug: ASCII graph ---
ascii_graph = app.get_graph().draw_ascii()
print(ascii_graph)

# --- Agent invocation ---
def run_agent(message, history):
    """
    message: str -> user's question
    history: list -> conversation history
    """
    result: AgentState = app.invoke(
        {"question": message},
        config={"callbacks": [tracer]}
    )

    # Construct agent response as Markdown
    response_md = ""
    if "narrative" in result:
        response_md += f"**Insights:**\n{result.get('narrative','')}\n\n"
    if "sql" in result:
        response_md += f"**SQL:**\n```sql\n{result.get('sql','')}\n```\n"

    # Prepare chart if exists
    chart_img = result.get("chart_pil")

    # Prepare dataframe if exists
    df_result = result.get("df", pd.DataFrame())

    # Append to history: (user, bot)
    history = history or []
    history.append((message, response_md))

    # Return updated history, chart, and dataframe
    return history, chart_img, df_result

# --- Gradio UI ---
with gr.Blocks() as demo:
    gr.Markdown("# Multi-turn Data Analysis Chatbot")
    chatbot = gr.Chatbot()
    user_input = gr.Textbox(label="Ask a question")
    submit_btn = gr.Button("Send")
    chart_out = gr.Image(label="Chart", type="pil")
    df_out = gr.Dataframe(label="Query Result")

    # Maintain conversation history
    state = gr.State([])

    submit_btn.click(
        run_agent,
        inputs=[user_input, state],
        outputs=[chatbot, chart_out, df_out]
    )

if __name__ == "__main__":
    try:
        demo.launch()
    finally:
        wait_for_all_tracers()
