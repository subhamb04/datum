import duckdb
import pandas as pd

conn = duckdb.connect()

sales = pd.read_csv("sample_data/sales.csv")
marketing = pd.read_csv("sample_data/marketing_spend.csv")
customers = pd.read_csv("sample_data/customers.csv")

conn.register("sales", sales)
conn.register("marketing_spend", marketing)
conn.register("customers", customers)
