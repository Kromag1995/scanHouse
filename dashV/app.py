
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc


from components.general_view import general_view
from components.location_compare_view import location_compare_view
from components.scrape_view import scrape_view

#Create app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


#Add layout
app.layout = html.Div([
    dbc.CardHeader([
        html.H1("Analisis de publicaciones de Alquier sobre la ciudad de buenos aires"),
    ]),
    html.Hr(),
    dcc.Tabs([
        dcc.Tab(
            label="General View",
            children=general_view
        ),
        dcc.Tab(
            label="Compact View",
            children=location_compare_view
        ),
        dcc.Tab(
            label="Scrape View",
            children=scrape_view
        ),
    ])
])





if __name__ == '__main__':
    app.run_server(debug=True, port=8051,     dev_tools_ui=True,
    dev_tools_serve_dev_bundles=True,)
