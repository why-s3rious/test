import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from components.functions import tai_chinh_tong_data
from components.callbacks import (
    year_slider_dupont_options_callback,
    year_slider_dupont_value_callback,
    dupont_funel_callback,
)
from components import navbar
from app import app

navbar = navbar.Navbar()
all_tickers_dupont = tai_chinh_tong_data.dropna(
    subset=["Ticker", "Doanh_so_thuan", "Co_dong_cua_cong_ty_me", "Tong_cong_tai_san"]
)["Ticker"].unique()
styles = {"pre": {"border": "thin lightgre solid", "overflowX": "scroll"}}
layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="selected_ticker_dupont",
                                            options=[
                                                {"label": a, "value": a}
                                                for a in all_tickers_dupont
                                            ],
                                            value=all_tickers_dupont[1],
                                        ),
                                    ],
                                    style={"width": "20%", "display": "inline-block"},
                                ),
                                html.Div(
                                    [
                                        dcc.RadioItems(
                                            id="data_select_dupont",
                                            options=[
                                                {"label": "Năm", "value": "A"},
                                                {"label": "Quý", "value": "Q"},
                                            ],
                                            value="A",
                                            labelStyle={
                                                "display": "inline-block",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={"width": "20%", "display": "inline-block"},
                                ),
                                html.Div(
                                    [
                                        dcc.Slider(
                                            id="dupont_select",
                                            min=1,
                                            max=3,
                                            value=1,
                                            tooltip={
                                                "placement": "bottom",
                                                "always_visible": True,
                                            },
                                        ),
                                    ],
                                    style={"width": "60%", "display": "inline-block"},
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="ROE_line",
                            # clickData={"points": [{"x": "2019A"}]},
                        )
                    ],
                    style={"display": "inline-block", "width": "40%"},
                ),
                html.Div(
                    [dcc.Graph(id="dupont_funel"),],
                    style={"display": "inline-block", "width": "60%"},
                ),
                # html.Div(
                #     [html.Pre(id="click-data", style=styles["pre"],)],style={'display':None},
                #     className="three columns",
                # ),
            ],
        ),
    ]
)
