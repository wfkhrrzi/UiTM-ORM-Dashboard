import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go

from layout.utils import title_chart
from pages.classify_tweet.classify_tweet import sentiment_colors
from pages.reputation.reputation_data import get_NBR,get_BFT


def get_color(percent):
    return sentiment_colors['positive'] if percent>0 else sentiment_colors['negative'] if percent<0 else sentiment_colors['neutral']

def donut_chart(percent, theme_color:str):
    # values = [100-abs(percent),abs(percent),]
    values = [abs(percent),100-abs(percent)]
    colors=[theme_color,'#ffffff00']

    if percent>=0:
        values = [abs(percent),100-abs(percent)]
        colors=[theme_color,'#ffffff00']
    else:
        values = [100-abs(percent),abs(percent)]
        colors=['#ffffff00',theme_color]

    fig = go.Figure(data=go.Pie(values=values,hole=.7))

    fig.update_layout(
        annotations=[
            dict(
                text=f"{percent}%", x=0.5, y=0.5, font_size=32,showarrow=False,
                font=dict(color=theme_color)
            )
        ],
        showlegend=False,
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            # pad=10
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # autosize=False,
        # width=140,
        # height=140,
    )

    fig.update_traces(
        hoverinfo='none',
        textinfo='none',
        marker=dict(
            colors=colors,
            line=dict(
                color='#d9dddc',
                width=1
            )
        ),
        # direction=direction,
        sort=False
    )

    return fig

layout = dbc.Container(
    [
        # page title
        dbc.Row(
            [
                html.H2(
                    children="Reputation Metrics",
                    style={'color':'#1d9bf0',},
                    className="text-center",
                ),
            ],
            class_name="my-4"
        ),
        # html.Hr(),
        # stats
        dbc.Row(
            [
                #nbr
                dbc.Col(
                    [
                        title_chart('Net Brand Reputation'),
                        html.Div(
                            dcc.Graph(
                                figure=donut_chart(get_NBR(),get_color(get_NBR()))
                            ),
                            # id="pred-sentiment",
                            # style={
                            #     "color":"white",
                            #     "min-height":"400px",
                            # },
                            className="pe-2 my-4",
                        ),
                        
                    ],
                    xl="6",
                ),
                #bft 
                dbc.Col(
                    [
                        title_chart('Brand Favourable Talkability'),
                        html.Div(
                            dcc.Graph(
                                figure=donut_chart(get_BFT(),get_color(get_BFT()))
                            ),
                            # id="pred-sentiment",
                            # style={
                            #     "color":"white",
                            #     "min-height":"400px",
                            # },
                            className="pe-2 my-4",
                        ),
                    ],
                    xl="6",
                ),
            ],
            class_name="mt-3"
        ),

    ], 
)