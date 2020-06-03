
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
import datetime as dt
from components.functions import nganh_nghe_data, Busday, all_tickers, column_name
from components.callbacks import year_slider_options_callback,year_slider_value_callback,level1_value_callback,level2_options_callback,level2_value_callback,level3_options_callback,level3_value_callback,level4_options_callback,level4_value_callback,sector_map_callback,x_time_series_callback,y_time_series_callback,multiline_chart_callback,stacked_bar_chart_callback,line_bar_chart_callback
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
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="selected_ticker",
                                            options=[
                                                {"label": a, "value": a}
                                                for a in all_tickers
                                            ],
                                            value=all_tickers[1],
                                        ),
                                        # print(all_tickers[1])
                                    ],
                                    style={"width": "50%", "display": "inline-block"},
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
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={"width": "50%", "display": "inline-block"},
                                ),
                            ],
                            style={"width": "40%", "display": "block"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="level1",
                                                    options=[
                                                        {"label": i, "value": i}
                                                        for i in nganh_nghe_data.Level1.unique()
                                                    ],
                                                ),
                                            ],
                                            style={
                                                "width": "25%",
                                                "display": "inline-block",
                                            },
                                        ),
                                        html.Div(
                                            [dcc.Dropdown(id="level2",),],
                                            style={
                                                "width": "25%",
                                                "display": "inline-block",
                                            },
                                        ),
                                        html.Div(
                                            [dcc.Dropdown(id="level3",),],
                                            style={
                                                "width": "25%",
                                                "display": "inline-block",
                                            },
                                        ),
                                        html.Div(
                                            [dcc.Dropdown(id="level4",),],
                                            style={
                                                "width": "25%",
                                                "display": "inline-block",
                                            },
                                        ),
                                    ],
                                ),
                                dcc.Dropdown(
                                    id="view_value_x",
                                    options=[
                                        {"label": x, "value": x} for x in column_name
                                    ],
                                    value="Co_dong_cua_cong_ty_me",
                                ),
                            ],
                            style={
                                "width": "48%",
                                "display": "inline-block",
                                "padding-bottom": "-4px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(id="year_slider",),
                                dcc.Dropdown(
                                    id="view_value_y",
                                    options=[
                                        {"label": y, "value": y} for y in column_name
                                    ],
                                    value="Doanh_so_thuan",
                                ),
                            ],
                            style={
                                "width": "48%",
                                "float": "right",
                                "display": "inline-block",
                            },
                        ),
                    ],
                    style={
                        "borderBottom": "thin lightgrey solid",
                        "backgroundColor": "rgb(250, 250, 250)",
                        "padding": "10px 5px",
                    },
                ),
                html.Div(
                    [dcc.Graph(id="sector_map",)],
                    style={
                        "width": "66%",
                        "display": "inline-block",
                        "padding": "0 20",
                    },
                ),
                html.Div(
                    [dcc.Graph(id="x_time_series"), dcc.Graph(id="y_time_series"),],
                    style={
                        "display": "inline-block",
                        "width": "33%",
                        "padding": "10 10",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="view_line_1",
                                    options=[
                                        {"label": i, "value": i} for i in column_name
                                    ],
                                    value="Doanh_so_thuan",
                                ),
                            ],
                            style={"width": "50%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="view_line_2",
                                    options=[
                                        {"label": i, "value": i} for i in column_name
                                    ],
                                    # multi=True,
                                    value="Co_dong_cua_cong_ty_me",
                                ),
                            ],
                            style={"width": "50%", "display": "inline-block"},
                        ),
                        html.Div([dcc.Graph(id="multiline_chart",),]),
                    ],
                    style={
                        "width": "33%",
                        "display": "inline-block",
                        "padding": "0 20",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="view_stack_1",
                                    options=[
                                        {"label": i, "value": i} for i in column_name
                                    ],
                                    value="Doanh_so_thuan",
                                ),
                            ],
                            style={"width": "50%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="view_stack_2",
                                    options=[
                                        {"label": i, "value": i} for i in column_name
                                    ],
                                    value="Tong_cong_tai_san",
                                ),
                            ],
                            style={"width": "50%", "display": "inline-block"},
                        ),
                        html.Div([dcc.Graph(id="stacked_bar_chart",),]),
                    ],
                    style={
                        "width": "33%",
                        "display": "inline-block",
                        "padding": "0 20",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="view_bar",
                                    options=[
                                        {"label": i, "value": i} for i in column_name
                                    ],
                                    value="EBIT",
                                ),
                            ],
                            style={"width": "50%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="view_line",
                                    options=[
                                        {"label": i, "value": i} for i in column_name
                                    ],
                                    value="Co_dong_cua_cong_ty_me",
                                ),
                            ],
                            style={"width": "50%", "display": "inline-block"},
                        ),
                        html.Div([dcc.Graph(id="line_bar_chart",),]),
                    ],
                    style={
                        "width": "33%",
                        "display": "inline-block",
                        "padding": "0 20",
                    },
                ),
            ]
        ),
    ]
)







