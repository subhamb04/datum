from langgraph.graph import StateGraph
import gradio as gr
import pandas as pd
import os
from langchain_core.tracers import LangChainTracer
from langchain_core.tracers.langchain import wait_for_all_tracers
from state import AgentState
from nodes import sql_generator, sql_executor, chart_generator, narrator

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

def run_agent(question: str):
    result: AgentState = app.invoke(
        {"question": question},
        config={"callbacks": [tracer]}
    )
    return (
        result.get("df", pd.DataFrame()),
        result.get("chart_pil"),   # ✅ now PIL image
        result.get("narrative", ""),
        result.get("sql", ""),
    )


with gr.Blocks() as demo:
    gr.Markdown("# Simple Data Analysis Agent with Typed State")
    q = gr.Textbox(label="Ask a question")
    btn = gr.Button("Run")
    df_out = gr.Dataframe(label="Query Result")
    chart_out = gr.Image(label="Chart", type="pil")
    narrative_out = gr.Markdown(label="Insights")
    sql_out = gr.Code(label="SQL", language="sql")
    btn.click(run_agent, inputs=[q], outputs=[df_out, chart_out, narrative_out, sql_out])

if __name__ == "__main__":
    try:
        demo.launch()
    finally:
        wait_for_all_tracers()
