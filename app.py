from langgraph.graph import StateGraph
import gradio as gr
import pandas as pd
import os
from langchain_core.tracers import LangChainTracer
from langchain_core.tracers.langchain import wait_for_all_tracers
from state import AgentState
from nodes import sql_generator, sql_executor, chart_generator, narrator
from io import BytesIO
import base64

project = os.getenv("LANGCHAIN_PROJECT", "default-project")
tracer = LangChainTracer(project_name=project)

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

ascii_graph = app.get_graph().draw_ascii()
print(ascii_graph)

def df_to_html(df: pd.DataFrame):
    """Convert dataframe to HTML table string"""
    if df.empty:
        return ""
    return df.to_html(index=False)

def pil_to_base64(img):
    """Convert PIL Image to base64 string for embedding"""
    if img is None:
        return ""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"<img src='data:image/png;base64,{img_str}' style='max-width:400px;'>"

def run_agent(message, history):
    """
    message: str -> user's question
    history: list -> conversation history
    """
    result: AgentState = app.invoke(
        {"question": message},
        config={"callbacks": [tracer]}
    )

    bot_message = ""
    if "narrative" in result and result.get("narrative"):
        bot_message += f"**Insights:**\n{result.get('narrative','')}\n\n"

    if "sql" in result and result.get("sql"):
        bot_message += f"**SQL:**\n```sql\n{result.get('sql','')}\n```\n"

    chart_html = pil_to_base64(result.get("chart_pil"))
    if chart_html:
        bot_message += chart_html + "\n"

    df_html = df_to_html(result.get("df", pd.DataFrame()))
    if df_html:
        bot_message += df_html

    history = history or []
    history.append((message, bot_message))

    return history

with gr.Blocks() as demo:
    gr.Markdown("# Multi-turn Data Analysis Chatbot with Inline Charts & Tables")
    chatbot = gr.Chatbot()
    user_input = gr.Textbox(label="Ask a question")
    submit_btn = gr.Button("Send")

    state = gr.State([])

    submit_btn.click(
        run_agent,
        inputs=[user_input, state],
        outputs=[chatbot]
    )

if __name__ == "__main__":
    try:
        demo.launch()
    finally:
        wait_for_all_tracers()
