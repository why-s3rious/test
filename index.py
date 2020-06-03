print('Star index ...')
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import dupont,bctc,home,faviv
import dash_bootstrap_components as dbc


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home/':
         return home.layout
    elif pathname == '/faviz/':
        return faviv.layout
    if pathname == '/dupont/':
        return dupont.layout
    elif pathname == '/bctc/':
         return bctc.layout
    else:
        return home.layout


if __name__ == "__main__":
    app.run_server(debug=False)
