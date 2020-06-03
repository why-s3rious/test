
print('import graph')
import plotly.graph_objects as go
import plotly.express as px

def layout_home(ten):
    layout = {
        "title": ten,
        "xaxis": {"title": "Date", "domain": [0, 1],},
        "yaxis": {"title": "Price", 'side':'left','overlaying':'y2','zeorline':True},
        "yaxis2": {"title": "NN_rong",'side':'right',},
        "margin": {"b": 40, "l": 60, "r": 40, "t": 25},
        'legend':{'x':0,'y':1}
    }
    return layout
def layout_faviz(ten):
    layout = {
        # "title": ten,
        "xaxis": {"domain": [0, 1],},
        "yaxis": {'side':'left','overlaying':'y2','zeorline':True},
        "yaxis2": {'side':'right',},
        "margin": {"b": 40, "l": 30, "r": 10, "t": 15},
        'height': 225
    }
    return layout
def heatmap_graph(df,map_value,color):
    fig= px.treemap(
    df,
    path=["Market", "Level1", "Level4", "Ticker_id"],
    values=map_value,
    color=color,
    hover_data=["Ticker"],
    color_continuous_scale=[
        (0.00, "rgb(246,53,56)"),
        (0.49, "rgb(79, 69, 84)"),
        (0.5, "rgb(65, 70, 84)"),
        (1.00, "rgb(48,204,90)"),
    ],
    color_continuous_midpoint=0,
    )
    fig.update_layout(
        margin = dict(
            l=20,
            r=10,
            t=10,
            b=20,
            pad=2
        )
    )

    return fig


def sector_map_graph(traces,view_xaxis,view_yaxis):
    return {
        "data": traces,
        "layout": dict(
            xaxis={"title": view_xaxis},
            yaxis={"title": view_yaxis},
            legend={"x": 0, "y": 1},
            hovermode="closest",
            transition={"duration": 500},
            margin={'l':40,'r':10,'b':30,'t':20}
        ),
    }

def time_series_graph(dff, axis_type, title):
    return {
        "data": [dict(x=dff["Lengthreport"], y=dff[axis_type], mode="lines+markers")],
        "layout": {
            "height": 225,
            "margin": {"l": 25, "b": 30, "r": 0, "t": 10},
            "annotations": [
                {
                    "x": 0,
                    "y": 0.85,
                    "xanchor": "left",
                    "yanchor": "bottom",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "align": "left",
                    "bgcolor": "rgba(255, 255, 255, 0.5)",
                    "text": title,
                }
            ],
            "xaxis": {"showgrid": False},
        },
    }

def porfolio_graph(dff_base, dff_compare, ticker_base, ticker_compare):
    data = [
        go.Scatter(name=ticker_base, x=dff_base["Ngay"], y=dff_base["Porfolio_price"],),
        go.Scatter(
            name=ticker_compare, x=dff_compare["Ngay"], y=dff_compare["Porfolio_price"],
        ),
    ]
    title = 'Porfolio vs VN30'
    layout = layout_home(title)
    return {"data": data, "layout": layout}


def price_graph(dff_base, ticker_base):
    data = [
        go.Scatter(name=ticker_base, x=dff_base["Ngay"], y=dff_base["Gia"],),
        go.Scatter(name='MB_rong', x=dff_base["Ngay"], y=dff_base["Mb_rong"],yaxis='y2',visible='legendonly',)
    ]
    ten = dff_base.Ten.unique()[0]
    layout = layout_home(ten)
    return {"data": data, "layout": layout}


def multiline_graph(dff,view_line_1,view_line_2):
    data = [
        go.Scatter(x=dff.index, y=dff[view_line_1],showlegend=False),
        go.Scatter(x=dff.index, y=dff[view_line_2],showlegend=False)
    ]
    title = ''
    layout = layout_faviz(title)
    return {
        "data": data,
        "layout": layout
    }


def stackedbar_graph(dff, stack_1, stack_2, title):
    data = [
        go.Bar(
            name=stack_1,
            x=dff["Lengthreport"],
            y=dff[stack_1],
            offsetgroup=1,
            showlegend=False,
        ),
        go.Bar(
            name=stack_2,
            x=dff["Lengthreport"],
            y=dff[stack_2],
            offsetgroup=1,
            showlegend=False,
            base=dff[stack_1],
        ),
    ]
    layout = layout_faviz(title)
    return {
        "data": data,
        "layout": layout 
    }


def barline_graph(dff, bar, line, title):
    data = [
        go.Bar(
            name=bar,
            x=dff["Lengthreport"],
            y=dff[bar],
            # offsetgroup=1,
            showlegend=False,
            # base=dff[stack_1],
        ),
        go.Scatter(
            name=line,
            x=dff["Lengthreport"],
            y=dff[line],
            # offsetgroup=1,
            showlegend=False,
        ),
    ]
    layout = layout_faviz(title)
    return {
        "data": data,
        "layout": layout
    }

def multiline_graph_go(data):
    fig = go.Figure()
    for col in data.columns:
        fig.add_trace(go.Scatter(name=col,y=data[col], x=data.index),)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=True,
        ),
        autosize=False,
        margin=dict(
            autoexpand=True,
            l=10,
            r=20,
            t=10,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )
    return fig
def funel_graph(dupont_data):
    fig = go.Figure()
    for i in range(0,dupont_data.shape[0]):
        fig.add_trace(go.Funnel(y=dupont_data.columns, x=dupont_data.iloc[i],showlegend=False,),)
    fig.update_xaxes(showgrid=False)
    fig.update_layout(
        margin=dict(
            autoexpand=True,
            l =20,
            r=10,
            t=10
        )
    )
    return fig


print('imported graph')


