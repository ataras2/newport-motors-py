from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd

sub_asms = ["OAP1", "spherical_mirror", "knife_edge"]
configs = list(range(1,5))


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Motor Control GUI', style={'textAlign':'center'}),
    html.H3(children='Adam Taras: adam.taras@sydney.edu.au', style={'textAlign':'left'}),
    dcc.Dropdown(
        sub_asms, 
        id='subasm-selection',
        searchable = False,
        clearable = False,
        placeholder="Select a sub assembly"
    ),
    dcc.Dropdown(
        configs, 
        id='config-selection',
        searchable = False,
        clearable = False,
        placeholder="Select a config"
    ),
    html.Button('Center', id='center-button', n_clicks=0),
    html.Div(id='text-placeholder',
             children='Hit the buttons :)')
    # dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    # dcc.Graph(id='graph-content')
])

def get_motor_map(subasm, config):
    return "/dev/ttyUSBx"

@callback(
    Output('text-placeholder', 'children'),
    State('subasm-selection', 'value'),
    State('config-selection', 'value'),
    Input('center-button', 'n_clicks')
)
def update_motor(subasm, config, n_clicks):
    return f"Sending Center command to {get_motor_map(subasm, config)} a.k.a {subasm}, {config}"


if __name__ == '__main__':
    app.run_server(debug=True)