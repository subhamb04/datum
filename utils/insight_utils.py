import pandas as pd
from io import BytesIO
import base64

def df_to_html(df: pd.DataFrame):
    if df.empty:
        return ""
    return df.to_html(index=False)

def pil_to_base64(img):
    if img is None:
        return ""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"<img src='data:image/png;base64,{img_str}' style='max-width:400px;'>"
