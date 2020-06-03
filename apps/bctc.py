import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app
import pandas as pd
import dash_bootstrap_components as dbc
from components import navbar
from components.callbacks import bctc_callback
from components.functions import all_tickers

navbar = navbar.Navbar()
print("Star BCTC ...")

layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="selected_ticker",
                                    options=[
                                        {"label": a, "value": a} for a in all_tickers
                                    ],
                                    value=all_tickers[1],
                                ),
                            ],
                            style={"width": "20%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.RadioItems(
                                    id="data_select",
                                    options=[
                                        {"label": "Năm", "value": "A"},
                                        {"label": "Quý", "value": "Q"},
                                    ],
                                    value="A",
                                    labelStyle={
                                        "display": "inline-block",
                                        "vertical-align": "middle",
                                    },
                                ),
                            ],
                            style={
                                "width": "10%",
                                "display": "inline-block",
                                "vertical-align": "middle",
                            },
                        ),
                        html.Div(
                            [html.Button("Download_file", id="download")],
                            style={
                                "width": "10%",
                                "display": "inline-block",
                                "float": "right",
                            },
                        ),
                    ],
                ),
                dbc.Tabs(
                    [
                        dbc.Tab(
                            [
                                dbc.Table.from_dataframe(
                                    df=pd.DataFrame(),
                                    id="dbc_kqkd",
                                    striped=True,
                                    bordered=True,
                                    hover=True,
                                    responsive=True,
                                )
                            ],
                            label="Báo cáo kết quả kinh doanh",
                        ),
                        dbc.Tab(
                            [
                                dbc.Table.from_dataframe(
                                    df=pd.DataFrame(),
                                    id="dbc_lctt",
                                    striped=True,
                                    bordered=True,
                                    hover=True,
                                    responsive=True,
                                ),
                            ],
                            label="Báo cáo lưu chuyển tiền tệ",
                        ),
                        dbc.Tab(
                            [
                                dbc.Table.from_dataframe(
                                    df=pd.DataFrame(),
                                    id="dbc_cdkt",
                                    striped=True,
                                    bordered=True,
                                    hover=True,
                                    responsive=True,
                                ),
                            ],
                            label="Bảng cân đối kế toán",
                        ),
                    ],
                ),
            ]
        ),
    ]
)
