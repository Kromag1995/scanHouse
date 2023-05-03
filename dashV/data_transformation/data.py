import os

from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
#Connect to db
CONNECTION_STRING = f'postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'
engine = create_engine(CONNECTION_STRING)

df = pd.read_sql("SELECT * FROM props", engine)

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
