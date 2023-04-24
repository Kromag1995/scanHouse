from datetime import datetime

from dash import html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

from data import df2

dates = list(set(df2["date_created"]))
dates.sort()

df2["p/m_cub"] = df2["price"]/df2["m2_cub"]

df2 = df2.sort_values(by=["p/m_cub"])
options = list(set(df2["location"])) + ["all"]


general_view = html.Div([
    html.Div(children=[
        dbc.Row([
            dbc.Col([
                dcc.Input(placeholder="m2_min", id="gv_m2_min", value=""),
                dcc.Input(placeholder="m2_max", id="gv_m2_max", value=""),
                dcc.Input(placeholder="price_min", id="gv_price_min", value=""),
                dcc.Input(placeholder="price_max", id="gv_price_max", value=""),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(options=options, value="all", id="gv_locations"),
            ]),
            dbc.Col([
                dcc.Dropdown(options=["USD", "$"], value="$", id="gv_currency"),
            ]),
            dbc.Col([
                dcc.Dropdown(options=dates, value=dates[-1], id="gv_initial_date"),
            ]),
            dbc.Col([
                dcc.Input(placeholder="Valor Dolar", id="gv_dolar", value="")
            ]),
        ]),
        html.Div(children=[
            dash_table.DataTable(data=df2.to_dict("records"), page_size=10, id="table"),
            ]),
        html.Div(children=[
            dcc.Graph(figure={}, id="gv_graph")
            ])
    ])
])


@callback(
    Output(component_id="gv_graph", component_property="figure"),
    Input(component_id="gv_locations", component_property="value"),
    Input(component_id="gv_m2_min", component_property="value"),
    Input(component_id="gv_m2_max", component_property="value"),
    Input(component_id="gv_price_min", component_property="value"),
    Input(component_id="gv_price_max", component_property="value"),
    Input(component_id="gv_initial_date", component_property="value"),
    Input(component_id="gv_currency", component_property="value"),
    Input(component_id="gv_dolar", component_property="value")
)
def update_graph_filter(
        locations,
        m2_min,
        m2_max,
        price_min,
        price_max,
        initial_date,
        currency,
        dolar
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
    if currency == "USD" and dolar:
        df3["price"] = df3["price"] * float(dolar)
    df3 = df3[
        (df3["m2_cub"] > float(m2_min)) &
        (df3["m2_cub"] < float(m2_max)) &
        (df3["price"] > float(price_min)) &
        (df3["price"] < float(price_max)) &
        (df3["date_created"] >= datetime.strptime(initial_date, "%Y-%m-%d").date()) &
        (df3["currency"] == currency)
        ]
    fig = px.scatter(df3,
                     x="m2_cub",
                     y="price",
                     labels={"m2_cub": "m2", "price": "Precio"},
                     color="location",
                     hover_data=["m2_cub", "price", "url"]
                     )
    return fig


@callback(
    Output(component_id="table", component_property="data"),
    Input(component_id="gv_locations", component_property="value"),
    Input(component_id="gv_graph", component_property="selectedData"),
    Input(component_id="gv_initial_date", component_property="value"),
    Input(component_id="gv_currency", component_property="value"),
    Input(component_id="gv_dolar", component_property="value")
)
def update_table(
        col,
        selected_data,
        initial_date,
        currency,
        dolar
):
    if selected_data is not None:
        points = selected_data['points']
        urls = [point['customdata'][0] for point in points]
        df3 = df2[df2["url"].isin(urls)]
    elif col != "all":
        df3 = df2[df2["location"] == col]
    else:
        df3 = df2[:]

    df3 = df3[
        (df3["date_created"] >= datetime.strptime(initial_date, "%Y-%m-%d").date()) &
        (df3["currency"] == currency)
    ]
    return df3.sort_values(by=["p/m_cub"]).to_dict("records")
