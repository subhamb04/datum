from state import AgentState
from db import conn
from llm import complete
from charts import df_to_pil_chart

def sql_generator(state: AgentState) -> dict:
    schema = """
    Tables:
    sales(date, region, product, revenue, units_sold)
    marketing_spend(date, region, channel, spend)
    customers(customer_id, region, age, income)
    """
    prompt = f"You are a helpful SQL expert. Schema: {schema}. Question: {state['question']}. Return only a SELECT SQL query."
    sql = complete(prompt)
    if not sql.lower().startswith("select"):
        sql = "SELECT region, SUM(revenue) as total_revenue FROM sales GROUP BY region"
    return {"sql": sql}   # ✅ Only returning updated key

def sql_executor(state: AgentState) -> dict:
    df = conn.execute(state["sql"]).df()
    return {"df": df}

def chart_generator(state: AgentState) -> dict:
    pil_img = df_to_pil_chart(state["df"], state["question"])
    return {"chart_pil": pil_img}

def narrator(state: AgentState) -> dict:
    df_json = state["df"].to_dict(orient="records")
    prompt = f"Question: {state['question']}\\nResult: {df_json}\\nWrite 3-4 bullet point insights with one recommendation."
    narrative = complete(prompt)
    return {"narrative": narrative}
