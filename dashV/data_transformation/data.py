import sqlite3
import pandas as pd

#Connect to db
conn = sqlite3.connect("./../scan_house.db")

df = pd.read_sql("SELECT * FROM props", conn)

#Clean data
mask = (df["price"] > 10) & \
       (df["m2_cub"] > 20)
df = df[mask]

#Filter data
df2 = df.loc[:, ["m2_cub", "price", "currency", "location", "url", "date_created"]]

top_locations = df2["location"].value_counts()[:20].keys()
df2 = df2[df2["location"].isin(top_locations)]
df2["date_created"] = pd.to_datetime(df2["date_created"]).dt.date
df2["p/m"] = df2["price"] / df2["m2_cub"]

dates = list(set(df2["date_created"]))
dates.sort()
