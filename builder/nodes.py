from builder.state import AgentState
from datastore.db import conn
from clients.llm import complete
from utils.charts import df_to_pil_chart

def decider(state: dict) -> dict:
    """Decide whether to use SQL flow or general LLM chat."""
    
    history_text = "\n".join([
        f"{h['role'].capitalize()}: {h['content']}" 
        for h in state.get("history", [])
    ])

    prompt = f"""
    You are a router. Decide whether the user question requires SQL/database analysis 
    (tables: sales, marketing_spend, customers) OR if it can be answered directly 
    as a general conversational reply.

    Chat history so far:
    {history_text}

    Current question: {state['question']}

    Answer ONLY with one word: "sql" or "chat".
    """

    decision = complete(prompt).lower().strip()
    if "sql" in decision:
        return {"route": "sql"}
    return {"route": "chat"}


def sql_generator(state: AgentState) -> dict:
    schema = """
    Tables:
    sales(date, region, product, revenue, units_sold)
    marketing_spend(date, region, channel, spend)
    customers(customer_id, region, age, income)
    """
    prompt = f"You are a helpful SQL expert. Schema: {schema}. Question: {state['question']}. Return only a SELECT SQL query and do not wrap it with ```sql tag."
    sql = complete(prompt)
    if not sql.lower().startswith("select"):
        sql = "SELECT region, SUM(revenue) as total_revenue FROM sales GROUP BY region"
    return {"sql": sql}

def sql_executor(state: AgentState) -> dict:
    df = conn.execute(state["sql"]).df()
    return {"df": df}

def chart_generator(state: AgentState) -> dict:
    pil_img = df_to_pil_chart(state["df"], state["question"])
    return {"chart_pil": pil_img}

def narrator(state: AgentState) -> dict:
    df_json = state["df"].to_dict(orient="records")
    prompt = f"Question: {state['question']}\nResult: {df_json}\nWrite 3-4 bullet point insights with one recommendation."
    narrative = complete(prompt)
    return {"narrative": narrative}

def general_chat(state: dict) -> dict:
    """Handle general conversational queries with LLM."""
    
    history_text = "\n".join([
        f"{h['role'].capitalize()}: {h['content']}" 
        for h in state.get("history", [])
    ])

    prompt = f"""
    You are a helpful assistant. Continue the conversation naturally.

    Chat history so far:
    {history_text}

    User question: {state['question']}
    """

    response = complete(prompt)
    return {"narrative": response}
