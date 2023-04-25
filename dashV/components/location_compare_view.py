from datetime import datetime

from dash import html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

from data_transformation.data import df2, dates

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
        initial_date,
        currency,
        dolar=None
    ):
    if not initial_date:
        initial_date = dates[-1]
    if not currency:
        currency = "$"
    mask = (df2["date_created"] >= datetime.strptime(initial_date, "%Y-%m-%d").date()) &\
           (df2["currency"] == currency)
    mean_price = df2[mask].groupby("location")["p/m"].median().sort_values(ascending=False)
    fig = px.scatter(x=mean_price.keys(),
                     y=mean_price.values,
                     labels={"x": "location", "y": "p/m"},
                     )
    return fig
