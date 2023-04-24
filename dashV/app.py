from dash import Dash, dcc, html
from general_view import general_view
from location_compare_view import location_compare_view
#Create app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
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
    app.run_server(debug=True, port=8051)
