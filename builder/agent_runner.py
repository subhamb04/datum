import pandas as pd
from utils.insight_utils import df_to_html, pil_to_base64
from builder.state import AgentState

def run_agent(app, tracer, message, history):
    history = history or []

    result: AgentState = app.invoke(
        {"question": message, "history": history},
        config={"callbacks": [tracer]}
    )

    bot_message = ""
    if result.get("narrative"):
        bot_message += f"**Datum:**\n{result['narrative']}\n\n"

    if result.get("sql"):
        bot_message += f"**SQL:**\n```sql\n{result['sql']}\n```\n"

    if chart_html := pil_to_base64(result.get("chart_pil")):
        bot_message += chart_html + "\n"

    if df_html := df_to_html(result.get("df", pd.DataFrame())):
        bot_message += df_html

    updated_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": bot_message}
    ]

    return updated_history, updated_history, ""
