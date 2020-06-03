print("Star heatmap ...")
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
import datetime as dt
from components.functions import Busday, all_tickers, column_name
from components.callbacks import heatmap_callback,porfolio_chart_callback,price_chart_callback
from components import navbar

navbar = navbar.Navbar()


layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.DatePickerSingle(
                                    id="date_picker",
                                    min_date_allowed=dt.datetime(2020, 1, 1),
                                    max_date_allowed=dt.date.today(),
                                    initial_visible_month=dt.date.today(),
                                    date=Busday(),
                                    day_size=25,
                                ),
                            ],
                            style={"display": "inline-block", "width": "13%"},
                        ),
                        html.Div(
                            [
                                dcc.RadioItems(
                                    id="select_map",
                                    options=[
                                        {"label": "Vốn hoá", "value": "Von_hoa"},
                                        {"label": "Giá trị", "value": "Gia_tri_view"},
                                        {"label": "Khối lượng", "value": "Volume_view"},
                                        {"label": "Khối ngoại", "value": "Mb_rong_view"},
                                    ],
                                    value="Von_hoa",
                                    labelStyle={
                                        "display": "inline-block",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={"display": "inline-block", "width": "40%"},
                        ),
                        html.Div(
                            [
                                dcc.Slider(
                                    id="map_view",
                                    min=1,
                                    max=20,
                                    value=1,
                                    tooltip={"placement": "top",'always_visible':True},
                                ),
                                dcc.Graph(
                                    id="heatmap",
                                    clickData={"points": [{"customdata": ["AAA", 0]}]},
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="selected_ticker_porfolio",
                            options=[{"label": a, "value": a} for a in all_tickers],
                            multi=True,
                            value=[all_tickers[1]],
                        ),
                    ],
                    style={"width": "99%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Graph(id="porfolio_chart"),
                        dcc.Slider(
                            id="porfolio_term",
                            min=20,
                            max=1200,
                            step=None,
                            marks={
                                20: "1M",
                                60: "3M",
                                120: "6M",
                                240: "1Y",
                                720: "3Y",
                                1200: "5Y",
                            },
                            value=60,
                        ),
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Graph(id="price_chart"),
                        dcc.Slider(
                            id="price_term",
                            min=20,
                            max=1200,
                            step=None,
                            marks={
                                20: "1M",
                                60: "3M",
                                120: "6M",
                                240: "1Y",
                                720: "3Y",
                                1200: "5Y",
                            },
                            value=60,
                        ),
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
            ]
        ),
    ]
)

