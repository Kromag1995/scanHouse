from datetime import datetime

from dash import html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import numpy as np

from data import df2

dates = list(set(df2["date_created"]))
dates.sort()

df2["price_off"] = np.where(df2["currency"] == "USD", df2["price"] * 200, df2["price"])
df2["price_blue"] = np.where(df2["currency"] == "USD", df2["price"] * 400, df2["price"])
df2["price"] = np.where(df2["currency"] == "USD", df2["price_blue"], df2["price"])

df2["p/m_total_blue"] = df2["price"]/df2["m2_cub"]

df2 = df2.sort_values(by=["p/m_total_blue"])
options = list(set(df2["location"])) + ["all"]


general_view = html.Div([
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
            dcc.Dropdown(options=options, value="all", id="locations")
        ]),
        html.Div(children=[
            dcc.Dropdown(options=dates, value=dates[2], id="initial_date")
        ]),
        html.Div(children=[
            dash_table.DataTable(data=df2.to_dict("records"), page_size=10, id="table"),
            ]),
        html.Div(children=[
            dcc.Graph(figure={}, id="genera-graph")
            ])
    ])
])


@callback(
    Output(component_id="genera-graph", component_property="figure"),
    Input(component_id="locations", component_property="value"),
    Input(component_id="m2_min", component_property="value"),
    Input(component_id="m2_max", component_property="value"),
    Input(component_id="price_min", component_property="value"),
    Input(component_id="price_max", component_property="value"),
    Input(component_id="initial_date", component_property="value")
)
def update_graph_filter(
        locations,
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
    if locations != "all":
        df3 = df2[df2["location"] == locations]
    else:
        df3 = df2[:]
    if not initial_date:
        initial_date = dates[2]
    df3 = df3[
        (df3["m2_cub"] > float(m2_min)) &
        (df3["m2_cub"] < float(m2_max)) &
        (df3["price"] > float(price_min)) &
        (df3["price"] < float(price_max)) &
        (df3["date_created"] >= datetime.strptime(initial_date, "%Y-%m-%d").date())
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
    Input(component_id="locations", component_property="value"),
    Input(component_id="genera-graph", component_property="selectedData"),
    Input(component_id="initial_date", component_property="value")
)
def update_table(col, selected_data, initial_date):
    if selected_data is not None:
        points = selected_data['points']
        urls = [point['customdata'][0] for point in points]
        df3 = df2[df2["url"].isin(urls)]
    elif col != "all":
        df3 = df2[df2["location"] == col]
    else:
        df3 = df2[:]
    df3 = df3[df3["date_created"] >= datetime.strptime(initial_date, "%Y-%m-%d").date()]
    return df3.sort_values(by=["p/m_total_blue"]).to_dict("records")
