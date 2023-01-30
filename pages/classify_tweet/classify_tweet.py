import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from pages.classify_tweet.classify_tweet_data import sentiment_predict, topic_predict
import plotly.graph_objs as go
import pandas as pd

from layout.utils import title_chart
from pages.topics.topics_data import get_ranked_topics

# layout = dbc.Container("CLASSIFY TWEET",fluid=True,class_name="text-center text-light fw-bolder")

sentiment_colors={
    'positive':'#00ba7c',
    'neutral':'#f6b561',
    'negative':'#d90912',
}

layout = dbc.Container(
    [
        # page title
        dbc.Row(
            [
                html.H2(
                    children="Tweet Classification",
                    style={'color':'#1d9bf0',},
                    className="text-center",
                ),
            ],
            class_name="my-4"
        ),
        # input (link, text)
        dbc.Row(
            [
                dbc.Textarea(
                    id="pred-input-tweet",
                    size="md",
                    placeholder="Insert tweet here",
                    value="lecturer saya baik"
                )
            ],
            class_name="mb-3 px-3"
        ),
        # submit button
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Submit",id="pred-submit",class_name="mx-3", color="success"),
                )
            ],
            class_name="text-center mb-4"
        ),
        html.Hr(),
        # stats
        dbc.Row(
            [
                #sentiment
                dbc.Col(
                    [
                        title_chart('Sentiment'),
                        dcc.Loading(
                            id="loading-sentiment-pred",
                            type="default",
                            children=html.Div(
                                id="pred-sentiment",
                                style={
                                    "color":"white",
                                    "min-height":"400px",
                                },
                                className="pe-2 my-4",
                            ),
                        ),
                        
                    ],
                    xl="6",
                ),
                #topic 
                dbc.Col(
                    [
                        title_chart('Topic'),
                        dcc.Loading(
                            id="loading-topic-pred",
                            type="default",
                            children=html.Div(
                                id="pred-topic",
                                style={
                                    "color":"white",
                                    "min-height":"400px",
                                },
                                className="mt-2"
                            ),
                        ),
                    ],
                    xl="6",
                ),
            ],
            class_name="mt-3"
        ),

    ], 
)

def donut_chart(percent, theme_color:str):
    values = [percent,100-percent]
    colors=[theme_color,'#ffffff00','#ffffff00']

    fig = go.Figure(data=go.Pie(values=values,hole=.7))

    fig.update_layout(
        annotations=[
            dict(
                text=f"{percent}%", x=0.5, y=0.5, font_size=20,showarrow=False,
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
        autosize=False,
        width=140,
        height=140,
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
        )
    )

    return fig

@callback(
    Output("pred-sentiment","children"),
    Input("pred-submit","n_clicks"),
    State("pred-input-tweet","value")
)
def predict_tweet(n_clicks, input_tweet):
    if n_clicks:
        prediction = sentiment_predict(input_tweet)

        sentiment_stats = prediction.copy()
        sentiment_stats.pop('sentiment')
        sentiment_stats = dict(sorted(sentiment_stats.items(), key=lambda item: item[1], reverse=True))

        return [
            # prediction
            dbc.Row(
                [
                    dbc.Col(
                        html.Span(
                            prediction['sentiment'],
                            style={
                                # "font-size":"80px",
                                "font-weight":"500",
                                "color":sentiment_colors[prediction['sentiment']],
                                # "width":"fit-content",
                            },
                            className="ps-2 sentiment-prediction-text"
                        ),
                        width=7,
                        sm=8,
                        class_name="d-flex align-items-center justify-content-center"
                    ),
                    dbc.Col(
                        dcc.Graph(
                            figure=donut_chart(prediction[prediction['sentiment']],sentiment_colors[prediction['sentiment']]),
                            config={
                                'displayModeBar': False
                            },
                        ),
                        width=5,
                        sm=4,
                    )
                ],
                className="mb-3"
            ),
            # sentiment stats
            dbc.Row(
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            className="mb-2 rounded",
                                            style={
                                                "width":f"{sentiment_stats[sentiment]}%",
                                                "height":"0.25rem",
                                                "background-color":sentiment_colors[sentiment],
                                            }
                                        ),
                                        html.Span(
                                            sentiment,
                                            className="leading-snug font-monospace",
                                            style={
                                                "line-height":"1.375"
                                            }
                                        ),
                                    ],
                                    style={
                                        "flex":"1 1 0%"
                                    },
                                ),
                                html.Span(
                                    f"{sentiment_stats[sentiment]}%",
                                    className="leading-snug font-monospace ps-2"
                                )
                            ],
                            className="""
                                d-flex
                                justify-content-between
                                align-items-start
                                px-sm-5
                                py-3
                            """,
                        )

                        for sentiment in sentiment_stats
                    ],
                    class_name="mt-3"
                )
            )
        ]

ranked_topics = get_ranked_topics()
ranked_topics = ranked_topics.reset_index(drop=True)

@callback(
    Output("pred-topic","children"),
    Input("pred-submit","n_clicks"),
    State("pred-input-tweet","value")
)
def predict_topic(n_clicks, input_tweet):
    if n_clicks:
        # return str(topic_predict(input_tweet))

        prediction = topic_predict(input_tweet)


        topic_title = ranked_topics[ranked_topics['Topic'] == prediction['topic'][0]]['Name'].tolist()[0]
        topic_rank = ranked_topics[ranked_topics['Topic'] == prediction['topic'][0]].index.tolist()[0] + 1

        return dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            #topic rank
                            html.Div(
                                f"#{topic_rank}",
                                # f"#{prediction['topic']}",
                                className="trending-topic-index",
                                style={
                                    "font-size":"1.3rem"
                                }
                            ),
                            #topic title
                            html.Div(
                                # prediction['topic'],
                                " ".join(topic_title.split('_')[1:3]),
                                className="topic-prediction-text",
                                style={
                                    "font-weight":"500",
                                }
                            ),
                        ],
                        className="mt-1 px-sm-3"
                    ),
                )
            ]
        )