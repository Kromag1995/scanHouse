import sqlite3
import pandas as pd

#Connect to db
conn = sqlite3.connect("./scan_house.db")

df = pd.read_sql("SELECT * FROM props", conn)

#Clean data
df2 = df.loc[:, ["m2_cub", "price", "currency", "location", "url", "date_created"]]

df2 = df2[df2["price"] > 10]
df2["date_created"] = pd.to_datetime(df2["date_created"]).dt.date
