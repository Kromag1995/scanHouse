from dash import html, dcc, callback, Output, Input
import plotly.express as px
from datetime import datetime
import dash_bootstrap_components as dbc

from data import df2

dates = list(set(df2["date_created"]))
dates.sort()

location_compare_view = html.Div([
    html.Div(children=[
        dbc.Row([
            dbc.Col([
                dbc.Label("Initial Date"),
            ], md=1),
            dbc.Col([
                dcc.Dropdown(options=dates, value=dates[2], id="lc_initial_date"),
            ], md=2)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Currency"),
            ], md=1),
            dbc.Col([
                dcc.Dropdown(options=["USD", "$"], value="$", id="lc_currency"),
            ], md=2)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Valor Dolar"),
            ], md=1),
            dbc.Col([
                dcc.Input(placeholder="Valor Dolar", id="lc_dolar", value=""),
            ], md=2)
        ]),
        html.Div(children=[
            dcc.Graph(figure={}, id="lc_graph")
        ])
    ])
])


@callback(
    Output(component_id="lc_graph", component_property="figure"),
    Input(component_id="lc_initial_date", component_property="value"),
    Input(component_id="lc_currency", component_property="value"),
    Input(component_id="lc_dolar", component_property="value")
)
def update_graph_filter(
        initial_date=None,
        currency="$",
        dolar=None
    ):
    if not initial_date:
        initial_date = dates[-1]
    df3 = df2[
        (df2["date_created"] >= datetime.strptime(initial_date, "%Y-%m-%d").date()) &
        (df2["currency"] == currency)
    ]
    if currency == "USD" and dolar:
        df3["price"] = df3["price"]*float(dolar)
    df3.loc[:,"p/m"] = df3["price"] / df3["m2_cub"]
    mean_price = df3.groupby("location")["p/m"].median().sort_values()
    fig = px.scatter(x=mean_price.keys(),
                     y=mean_price.values,
                     labels={"x": "location", "y": "p/m"},
                     )
    fig.update_yaxes(range=[1_000, 6_000])
    return fig
