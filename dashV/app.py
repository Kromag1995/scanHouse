from dash import Dash, dcc, html
from general_view import general_view
from location_compare_view import location_compare_view
import dash_bootstrap_components as dbc

#Create app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


#Add layout
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(
            label="General View",
            children=general_view
        ),
        dcc.Tab(
            label="Compact Information",
            children=location_compare_view
        ),
    ])
])





if __name__ == '__main__':
    app.run_server(debug=True, port=8051,     dev_tools_ui=True,
    dev_tools_serve_dev_bundles=True,)
