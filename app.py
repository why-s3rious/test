import dash
import dash_bootstrap_components as dbc

print("Star app ...")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server = app.server
app.config.suppress_callback_exceptions = True
