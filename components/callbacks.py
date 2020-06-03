#%%
print("Load callback")
import dash
import json
from app import app
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import datetime
from components.functions import (
    tai_chinh_tong_data,
    nganh_nghe_data,
    price_data,
    heatmap_data,
    list_vn30,
)
from components import graph
import dash_bootstrap_components as dbc

# print(nganh_nghe_data.index[1])
@app.callback(
    Output("heatmap", "figure"),
    [
        Input("select_map", "value"),
        Input("date_picker", "date"),
        Input("map_view", "value"),
    ],
)
def heatmap_callback(select_map, date, map_view):

    heatmap = (
        heatmap_data.loc[(heatmap_data.Ngay <= date) & (heatmap_data.Von_hoa > 10 * 7)]
        .groupby("Ticker")
        .tail(map_view + 3)
    )

    heatmap["Change"] = 100 * (
        heatmap.groupby("Ticker")["Gia"].pct_change(periods=1).round(1)
    )

    heatmap["Change"] = 100 * (
        heatmap.groupby("Ticker")["Gia"].pct_change(periods=map_view)
    ).round(2)
    if select_map == "Mb_rong_view":
        color = "Mua_ban"
        heatmap["Mua_ban"] = (
            heatmap.groupby("Ticker")
            .rolling(window=map_view, min_periods=1)
            .Mb_rong.sum()
            .reset_index(0, drop=True)
        ) / 10 ** 9

    else:
        heatmap["%"] = (
            heatmap["Change"]
            .where(heatmap["Change"] > -7, -7)
            .where(heatmap["Change"] < 7, 7)
        )
        color = "%"
    # rolling gap van de khi ko dung datetime dataframe
    if select_map != "Von_hoa":
        heatmap["Mb_rong"] = abs(heatmap["Mb_rong"])
        heatmap[select_map] = (
            heatmap.groupby("Ticker")
            .rolling(window=map_view, min_periods=1)[select_map[:-5]]
            .sum()
            .reset_index(0, drop=True)
        )
        heatmap = heatmap[heatmap[select_map] != 0]
    # print(heatmap.isnull().sum(axis=)
    heatmap["Ticker_id"] = (
        heatmap.Ticker
        + " "
        + (heatmap["Gia"] / 1000).round(1).astype(str)
        + " "
        + heatmap.Change.round(1).astype(str)
        + "%"
        + (heatmap.Gia.shift(map_view) / 1000).round(1).astype(str)
    )
    df = heatmap.loc[
        heatmap.Ngay == pd.to_datetime(date).strftime("%Y-%m-%d")
    ].drop_duplicates(subset=["Ticker"])
    return graph.heatmap_graph(df, select_map, color)


@app.callback([Output("level1", "value"),], [Input("selected_ticker", "value")])
def level1_value_callback(ticker):
    nganh = nganh_nghe_data[nganh_nghe_data.index == ticker]
    return list(nganh.Level1)


@app.callback(Output("sector_map", "clickData"), [Input("selected_ticker", "value")])
def clickData_calback(ticker):
    return {"points": [{"text": ticker}]}


@app.callback(
    [Output("level2", "options"),], [Input("level1", "value")],
)
def level2_options_callback(level1):
    return (
        [
            {"label": lv2, "value": lv2}
            for lv2 in nganh_nghe_data[nganh_nghe_data.Level1 == level1].Level2.unique()
        ],
    )


@app.callback(
    Output("level2", "value"), [Input("level2", "options")],
)
def level2_value_callback(options):
    return "select_level"


@app.callback(
    [Output("level3", "options"),], [Input("level2", "value")],
)
def level3_options_callback(level2):
    return (
        [
            {"label": lv3, "value": lv3}
            for lv3 in nganh_nghe_data[nganh_nghe_data.Level2 == level2].Level3.unique()
        ],
    )


@app.callback(
    Output("level3", "value"), [Input("level3", "options")],
)
def level3_value_callback(options):
    return "select_level"


@app.callback(
    [Output("level4", "options"),], [Input("level3", "value")],
)
def level4_options_callback(level3):
    return (
        [
            {"label": lv4, "value": lv4}
            for lv4 in nganh_nghe_data[nganh_nghe_data.Level3 == level3].Level4.unique()
        ],
    )


@app.callback(
    Output("level4", "value"), [Input("level4", "options")],
)
def level4_value_callback(options):
    return "select_level"


@app.callback(
    Output("sector_map", "figure"),
    [
        Input("data_select", "value"),
        Input("level1", "value"),
        Input("level2", "value"),
        Input("level3", "value"),
        Input("level4", "value"),
        Input("year_slider", "value"),
        Input("view_value_x", "value"),
        Input("view_value_y", "value"),
    ],
)
def sector_map_callback(
    select_data, level1, level2, level3, level4, selected_year, view_xaxis, view_yaxis
):
    data_selected = tai_chinh_tong_data[
        tai_chinh_tong_data.Lengthreport.str.contains(select_data)
    ]
    level_filter1 = nganh_nghe_data[nganh_nghe_data.Level1 == str(level1)].reset_index()

    if level4 in nganh_nghe_data.Level4.unique():
        level_filter = level_filter1[level_filter1.Level4 == level4]
    elif level3 in nganh_nghe_data.Level3.unique():
        level_filter = level_filter1[level_filter1.Level3 == level3]
    elif level2 in nganh_nghe_data.Level2.unique():
        level_filter = level_filter1[level_filter1.Level2 == level2]
    else:
        level_filter = level_filter1
    tickers = level_filter["Ticker"].values
    df_nganh = data_selected[data_selected["Ticker"].isin(tickers)]
    filtered_df = df_nganh[df_nganh.Lengthreport == selected_year]
    traces = []
    for i in filtered_df.San.unique():
        df_by_San = filtered_df[filtered_df["San"] == i]
        traces.append(
            dict(
                x=df_by_San[view_xaxis],
                y=df_by_San[view_yaxis],
                text=df_by_San["Ticker"],
                mode="markers+text",
                opacity=0.7,
                textposition="top center",
                marker={"size": 15, "line": {"width": 0.5, "color": "white"}},
                name=i,
            )
        )
    return graph.sector_map_graph(traces, view_xaxis, view_yaxis)


@app.callback(
    Output("x_time_series", "figure"),
    [
        Input("sector_map", "clickData"),
        Input("view_value_x", "value"),
        Input("data_select", "value"),
    ],
)
def x_time_series_callback(clickData, view_value_x, data_select):
    ticker = clickData["points"][0]["text"]
    select_data = tai_chinh_tong_data[
        tai_chinh_tong_data.Lengthreport.str.contains(data_select)
    ]
    ticker_data = select_data[select_data.Ticker == ticker].tail(10)
    title = "<b>{}</b><br>{}".format(ticker, view_value_x)
    return graph.time_series_graph(ticker_data, view_value_x, title)


@app.callback(
    Output("y_time_series", "figure"),
    [
        Input("sector_map", "clickData"),
        Input("view_value_y", "value"),
        Input("data_select", "value"),
    ],
)
def y_time_series_callback(clickData, view_value_y, data_select):
    ticker = clickData["points"][0]["text"]
    select_data = tai_chinh_tong_data[
        tai_chinh_tong_data.Lengthreport.str.contains(data_select)
    ]
    ticker_data = select_data[select_data.Ticker == ticker].tail(10)
    title = "<b>{}</b><br>{}".format(ticker, view_value_y)
    return graph.time_series_graph(ticker_data, view_value_y, title)


# multiline_callback
@app.callback(
    Output("multiline_chart", "figure"),
    [
        Input("view_line_1", "value"),
        Input("view_line_2", "value"),
        Input("sector_map", "clickData"),
        Input("data_select", "value"),
    ],
)
def multiline_chart_callback(view_line_1, view_line_2, clickData, data_select):
    ticker = clickData["points"][0]["text"]
    data = (
        tai_chinh_tong_data[
            (tai_chinh_tong_data.Ticker == ticker)
            & (tai_chinh_tong_data.Lengthreport.str.contains(data_select))
        ]
        .loc[:, ["Lengthreport", view_line_1, view_line_2]]
        .set_index("Lengthreport")
    )
    return graph.multiline_graph(data, view_line_1, view_line_2)


# stackedbar_callback
@app.callback(
    Output("stacked_bar_chart", "figure"),
    [
        Input("view_stack_1", "value"),
        Input("view_stack_2", "value"),
        Input("sector_map", "clickData"),
        Input("data_select", "value"),
    ],
)
def stacked_bar_chart_callback(view_stack_1, view_stack_2, clickData, data_select):
    selected_ticker = clickData["points"][0]["text"]
    data_tempt = tai_chinh_tong_data[tai_chinh_tong_data.Ticker == selected_ticker]
    data = data_tempt[data_tempt.Lengthreport.str.contains(data_select)]
    stack_1 = view_stack_1
    stack_2 = view_stack_2
    title = "{}".format(selected_ticker)
    return graph.stackedbar_graph(data, stack_1, stack_2, title)


# line_bar_callback
@app.callback(
    Output("line_bar_chart", "figure"),
    [
        Input("view_bar", "value"),
        Input("view_line", "value"),
        Input("sector_map", "clickData"),
        Input("data_select", "value"),
    ],
)
def line_bar_chart_callback(view_bar, view_line, clickData, data_select):
    selected_ticker = clickData["points"][0]["text"]
    data_tempt = tai_chinh_tong_data[tai_chinh_tong_data.Ticker == selected_ticker]
    data = data_tempt[data_tempt.Lengthreport.str.contains(data_select)]
    line = view_line
    bar = view_bar
    title = "{}".format(selected_ticker)
    return graph.barline_graph(data, bar, line, title)


# porfolio chart
@app.callback(
    Output("porfolio_chart", "figure"),
    [Input("porfolio_term", "value"), Input("selected_ticker_porfolio", "value")],
)
def porfolio_chart_callback(porfolio_term, tickers):
    ticker_base = "Profolio vs VN30"
    dff_base = (
        price_data.loc[price_data["Ticker"].isin(tickers)]
        .tail(porfolio_term)
        .groupby("Ngay")
        .sum()
    )
    dff_base.reset_index(inplace=True)
    dff_base["Porfolio_price"] = dff_base["Gia"].astype(float) / float(
        dff_base["Gia"][0]
    )
    ticker_compare = "VN30"

    dff_compare = (
        price_data.loc[price_data["Ticker"].isin(list_vn30)]
        .tail(porfolio_term)
        .groupby("Ngay")
        .sum()
    )
    dff_compare["Ticker"] = "VN30"
    dff_compare.reset_index(inplace=True)
    dff_compare["Porfolio_price"] = dff_compare["Gia"].astype(float) / float(
        dff_compare["Gia"][0]
    )
    return graph.porfolio_graph(dff_base, dff_compare, ticker_base, ticker_compare)


# price chart
@app.callback(
    Output("price_chart", "figure"),
    [Input("heatmap", "clickData"), Input("price_term", "value")],
)
def price_chart_callback(clickData, price_term):
    price_data_filter = price_data
    if clickData["points"][0]["customdata"][0] != "(?)":
        ticker_base = clickData["points"][0]["customdata"][0]
    else:
        raise dash.exceptions.PreventUpdate
        return ticker_base
    dff_base = price_data_filter.loc[price_data_filter["Ticker"] == ticker_base].tail(
        price_term
    )
    return graph.price_graph(dff_base, ticker_base)


# year_slider callback
@app.callback(
    Output("year_slider", "options"), [Input("data_select", "value")],
)
def year_slider_options_callback(set_select_data):
    options = [
        {"label": i, "value": i}
        for i in tai_chinh_tong_data[
            tai_chinh_tong_data.Lengthreport.str.contains(set_select_data)
        ]["Lengthreport"].unique()
    ]
    return sorted(options, key=lambda x: x["value"], reverse=True)


@app.callback(
    Output("year_slider", "value"), [Input("year_slider", "options")],
)
def year_slider_value_callback(set_select_data_options):

    return sorted(set_select_data_options, key=lambda x: x["value"])[-1]["value"]


@app.callback(
    [
        Output("dbc_kqkd", "children"),
        Output("dbc_lctt", "children"),
        Output("dbc_cdkt", "children"),
    ],
    [
        Input("selected_ticker", "value"),
        Input("data_select", "value"),
        Input("download", "n_clicks"),
    ],
)
def bctc_callback(select_ticker, data_select, n_clicks):

    tai_chinh_tong_data_table = (
        tai_chinh_tong_data.loc[tai_chinh_tong_data.Ticker == select_ticker][
            tai_chinh_tong_data["Lengthreport"].str.contains(data_select)
        ]
        .sort_values(by=["Lengthreport"], ascending=False)
        .drop_duplicates(subset=["Ticker", "Lengthreport"])
    )
    tai_chinh_tong_data_table["Yearreport"] = tai_chinh_tong_data_table[
        "Lengthreport"
    ].astype(str)
    table = tai_chinh_tong_data_table.set_index("Lengthreport").T
    table_kqkd = (table.iloc[100:124, :].astype(float) / 10 ** 9).round(1)
    for col in table_kqkd.columns:
        table_kqkd[col] = table_kqkd[col].apply(lambda x: "{:,}".format(x))
    table_kqkd.reset_index(inplace=True)
    table_kqkd.rename(columns={"index": "Kết quả kinh doanh"}, inplace=True)
    table_lctt = (table.iloc[125:170, :].astype(float) / 10 ** 9).round(1)
    for col in table_lctt.columns:
        table_lctt[col] = table_lctt[col].apply(lambda x: "{:,}".format(x))
    table_lctt.reset_index(inplace=True)
    table_lctt.rename(columns={"index": "Lưu chuyển tiền tệ"}, inplace=True)
    table_cdkt = (table.iloc[4:100, :].astype(float) / 10 ** 9).round(1)
    for col in table_cdkt.columns:
        table_cdkt[col] = table_cdkt[col].apply(lambda x: "{:,}".format(x))
    table_cdkt.reset_index(inplace=True)
    table_cdkt.rename(columns={"index": "Cân đối kế toán"}, inplace=True)
    if dash.callback_context.triggered:
        table.to_csv("download/" + select_ticker + ".csv")

    return (
        dbc.Table.from_dataframe(df=table_kqkd),
        dbc.Table.from_dataframe(df=table_lctt),
        dbc.Table.from_dataframe(df=table_cdkt),
    )


@app.callback(Output("click-data", "children"), [Input("ROE_line", "clickData")])
def display_click_data(ticker):
    # nganh = nganh_nghe_data[nganh_nghe_data.Ticker == ticker]
    # print(json.dumps(ticker, indent=2))
    return json.dumps(ticker, indent=2)


@app.callback(
    Output("year_slider_dupont", "options"), [Input("data_select_dupont", "value"),],
)
def year_slider_dupont_options_callback(set_select_data):
    options = [
        {"label": i, "value": i}
        for i in tai_chinh_tong_data[
            tai_chinh_tong_data.Lengthreport.str.contains(set_select_data)
        ]["Lengthreport"].unique()
    ]
    opt = sorted(options, key=lambda x: x["value"], reverse=True)
    return opt


@app.callback(
    Output("year_slider_dupont", "value"), [Input("year_slider_dupont", "options")],
)
def year_slider_dupont_value_callback(set_select_data_options,):

    val = sorted(set_select_data_options, key=lambda x: x["value"])[-1]["value"]
    return val


@app.callback(
    [Output("ROE_line", "figure"), Output("ROE_line", "clickData")],
    [Input("selected_ticker_dupont", "value"), Input("data_select_dupont", "value")],
)
def ROE_line_callback(ticker, data_select):
    data = (
        tai_chinh_tong_data[
            (tai_chinh_tong_data.Ticker == ticker)
            & (tai_chinh_tong_data.Lengthreport.str.contains(data_select))
        ]
        .loc[:, ["Lengthreport", "ROA", "ROE", "ROIC"]]
        .set_index("Lengthreport")
    )
    clickData = {"points": [{"x": data.index[-1]}]}
    return graph.multiline_graph_go(data), clickData


@app.callback(
    Output("dupont_funel", "figure"),
    [
        Input("selected_ticker_dupont", "value"),
        Input("data_select_dupont", "value"),
        Input("ROE_line", "clickData"),
        Input("dupont_select", "value"),
    ],
)
def dupont_funel_callback(ticker, data_selected, clickData, dupont_select):
    year = clickData["points"][0]["x"]
    data_select = tai_chinh_tong_data[
        tai_chinh_tong_data["Lengthreport"].str.contains(data_selected)
    ]
    data = data_select[
        (data_select["Ticker"] == ticker) & (data_select["Lengthreport"] == year)
    ].tail(1)
    von_chu = data.Von_gop + data.Thang_du_von_co_phan
    von_khac = data.Von_chu_so_huu - von_chu
    if dupont_select == 1:

        data_dict = {
            "Tong_tai_san": [data.Tong_cong_tai_san.values[0]],
            "Doanh_thu": [data.Doanh_so_thuan.values[0]],
            "Von_chu_so_huu": [data.Von_chu_so_huu.values[0]],
            "No_phai_tra": [data.No_phai_tra.values[0]],
            "EBIT": [data.EBIT.values[0]],
            "Lai_sau_thue": [data.Co_dong_cua_cong_ty_me.values[0]],
        }
    if dupont_select == 2:
        data_dict = {
            "Tong_tai_san": [
                data.Tai_san_dai_han.values[0],
                0,
                data.Tai_san_ngan_han.values[0],
            ],
            "Doanh_thu": [
                abs(data.Gia_von_hang_ban.values[0]),
                0,
                data.Lai_gop.values[0],
            ],
            "Von_chu_so_huu": [von_chu.values[0], 0, von_khac.values[0]],
            "No_phai_tra": [
                data.Tong_no_vay.values[0],
                0,
                (data.No_phai_tra - data.Tong_no_vay).values[0],
            ],
            "EBIT": [data.EBIT.values[0], 0, (data.EBITDA - data.EBIT).values[0]],
            "Lai_sau_thue": [
                data.Co_dong_cua_cong_ty_me.values[0],
                0,
                (data.Lai_rong_truoc_thue - data.Co_dong_cua_cong_ty_me).values[0],
            ],
        }
    if dupont_select == 3:
        data_dict = {
            "Tong_tai_san": [
                data.Tai_san_dai_han.values[0],
                0,
                data.Tai_san_ngan_han.values[0],
            ],
            "Doanh_thu": [
                abs(data.Gia_von_hang_ban.values[0]),
                data.Phai_thu_khach_hang.values[0],
                data.Lai_gop.values[0],
            ],
            "Von_chu_so_huu": [von_chu.values[0], 0, von_khac.values[0]],
            "No_phai_tra": [
                data.Tong_no_vay.values[0],
                0,
                (data.No_phai_tra - data.Tong_no_vay).values[0],
            ],
            "EBIT": [data.EBIT.values[0], 0, (data.EBITDA - data.EBIT).values[0]],
            "Lai_sau_thue": [
                data.Co_dong_cua_cong_ty_me.values[0],
                0,
                (data.Lai_rong_truoc_thue - data.Co_dong_cua_cong_ty_me).values[0],
            ],
        }
    df_dict = pd.DataFrame.from_dict(data_dict)

    dup = graph.funel_graph(df_dict)
    return dup


# print(tai_chinh_tong_data.columns)
# pd.DataFrame(tai_chinh_tong_data.columns).to_csv('column.csv')
print("loaded callback")
