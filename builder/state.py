from typing import TypedDict, Literal
import pandas as pd
from PIL import Image

class AgentState(TypedDict, total=False):
    question: str
    sql: str
    df: pd.DataFrame
    chart_pil: Image.Image
    narrative: str
    route: Literal["sql", "chat"]
    history: list[tuple[str, str]]
