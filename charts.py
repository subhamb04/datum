import matplotlib.pyplot as plt
import pandas as pd
import io
from PIL import Image

def df_to_pil_chart(df: pd.DataFrame, question: str) -> Image.Image:
    fig, ax = plt.subplots()
    if df.shape[1] >= 2:
        x = df.iloc[:,0].astype(str)
        y = df.iloc[:,1]
        ax.bar(x, y)
        ax.set_xlabel(df.columns[0])
        ax.set_ylabel(df.columns[1])
        ax.set_title(question)
        plt.xticks(rotation=45, ha='right')
    else:
        ax.text(0.5,0.5,"No chart", ha='center')
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    plt.close(fig)
    return Image.open(buf)
