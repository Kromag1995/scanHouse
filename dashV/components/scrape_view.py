from dash import html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

from data_transformation.data import df, dates, df2



scrape_view = html.Div([
    html.Div(children=[
        dbc.Row([
            dbc.Col([
                dbc.Label("Currency"),
            ], md=1),
            dbc.Col([
                dcc.Dropdown(options=["$", "USD", "Vs", "Both"], value="$", id="s_currency"),
            ], md=2)
        ]),
        html.Div(children=[
            dcc.Graph(
                figure={},
                id="s_graph"
            )
        ])
    ])
])


@callback(
    Output(component_id="s_graph", component_property="figure"),
    Input(component_id="s_currency", component_property="value")
)
def update_graph_filter(
        currency="$",
    ):
    if currency == "Vs":
        fig = px.histogram(
            df2,
            x="location",
            color="currency",
            barmode="group"
        ).update_xaxes(categoryorder="total descending")
        return fig
    elif currency == "Both":
        fig = px.histogram(
            df2,
            x="location",
        ).update_xaxes(categoryorder="total descending")
        return fig
    mask = df2["currency"] == currency
    fig = px.histogram(
        df2[mask],
        x="location",
    ).update_xaxes(categoryorder="total descending")
    return fig

