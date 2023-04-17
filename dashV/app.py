import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input

conn = sqlite3.connect("../scan_house.db")

df = pd.read_sql("SELECT * FROM props", conn)

df2 = df.loc[:, ["m2_cub", "price", "currency", "location", "url", "date_created"]]

df2 = df2[df2["price"] > 10]
df2["date_created"] = pd.to_datetime(df2["date_created"])

dates = [datetime(2023, 4, 1+7*i) for i in range(0, 3)]

df2["price_off"] = np.where(df2["currency"] == "USD", df2["price"] * 200, df2["price"])
df2["price_blue"] = np.where(df2["currency"] == "USD", df2["price"] * 400, df2["price"])
df2["price"] = np.where(df2["currency"] == "USD", df2["price_blue"], df2["price"])

df2["p/m_total_off"] = df2["price"]/df2["m2_cub"]
df2["p/m_total_blue"] = df2["price"]/df2["m2_cub"]

df2 = df2.sort_values(by=["p/m_total_blue"])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

options = list(set(df2["location"])) + ["all"]

app.layout = html.Div([
    html.Div(children=[
        html.Div(children=[
            dcc.Input(placeholder="m2_min", id="m2_min", value=""),
        ], className="three columns"),
        html.Div(children=[
            dcc.Input(placeholder="m2_max", id="m2_max", value=""),
        ], className="three columns"),
        html.Div(children=[
            dcc.Input(placeholder="price_min", id="price_min", value=""),
        ]),
        html.Div(children=[
            dcc.Input(placeholder="price_max", id="price_max", value=""),
        ]),
        html.Div(children=[
            dcc.Dropdown(options=options, value="all", id="radio_items")
        ]),
        html.Div(children=[
            dcc.Dropdown(options=dates, value=dates[2], id="initial_date")
        ]),
        html.Div(children=[
            dash_table.DataTable(data=df2.to_dict("records"), page_size=10, id="table"),
            ]),
        html.Div(children=[
            dcc.Graph(figure={}, id="graph")
            ])
    ])
])


@callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="radio_items", component_property="value"),
    Input(component_id="m2_min", component_property="value"),
    Input(component_id="m2_max", component_property="value"),
    Input(component_id="price_min", component_property="value"),
    Input(component_id="price_max", component_property="value"),
    Input(component_id="initial_date", component_property="value")
)
def update_graph_filter(
        col,
        m2_min,
        m2_max,
        price_min,
        price_max,
        initial_date
    ):
    if not m2_max:
        m2_max = 200
    if not m2_min:
        m2_min = 10
    if not price_max:
        price_max = 250_000
    if not price_min:
        price_min = 60_000
    if col != "all":
        df3 = df2[df2["location"] == col]
    else:
        df3 = df2[:]
    if not initial_date:
        initial_date = dates[2]
    df3 = df3[
        (df3["m2_cub"] > float(m2_min)) &
        (df3["m2_cub"] < float(m2_max)) &
        (df3["price"] > float(price_min)) &
        (df3["price"] < float(price_max)) &
        (df3["date_created"] > initial_date)
        ]
    fig = px.scatter(df3,
                     x="m2_cub",
                     y="price_blue",
                     labels={"m2_cub": "m2", "price_blue": "Precio"},
                     color="location",
                     hover_data=["m2_cub", "price_blue", "url"]
                     )
    return fig


@callback(
    Output(component_id="table", component_property="data"),
    Input(component_id="radio_items", component_property="value"),
    Input(component_id="graph", component_property="selectedData")
)
def update_table(col, selected_data):
    if selected_data is not None:
        points = selected_data['points']
        urls = [point['customdata'][0] for point in points]
        df3 = df2[df2["url"].isin(urls)]
    elif col != "all":
        df3 = df2[df2["location"] == col]
    else:
        df3 = df2[:]
    return df3.sort_values(by=["p/m_total_blue"]).to_dict("records")


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
