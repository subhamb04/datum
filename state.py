from typing import TypedDict, Optional
import pandas as pd
from PIL import Image

class AgentState(TypedDict, total=False):
    question: str
    sql: str
    df: pd.DataFrame
    chart_pil: Image.Image
    narrative: str

