import duckdb
import pandas as pd

conn = duckdb.connect()

sales = pd.read_csv("data/sales.csv")
marketing = pd.read_csv("data/marketing_spend.csv")
customers = pd.read_csv("data/customers.csv")

conn.register("sales", sales)
conn.register("marketing_spend", marketing)
conn.register("customers", customers)
