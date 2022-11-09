import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from pages.classify_tweet.classify_tweet_data import sentiment_predict, topic_predict

from layout.layout import title_chart

dash.register_page(__name__,path='/classify-tweet')

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
                    placeholder="Insert tweet here"
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
                        html.Div(id="pred-sentiment",style={"color":"white"})
                    ],
                    xl="6",
                ),
                #topic 
                dbc.Col(
                    [
                        title_chart('Topic'),
                        html.Div(id="pred-topic",style={"color":"white"})
                    ],
                    xl="6",
                ),
            ],
            class_name="mt-3"
        ),

    ], 
)

@callback(
    Output("pred-sentiment","children"),
    Input("pred-submit","n_clicks"),
    State("pred-input-tweet","value")
)
def predict_tweet(n_clicks, input_tweet):
    if n_clicks:
        return str(sentiment_predict(input_tweet))

@callback(
    Output("pred-topic","children"),
    Input("pred-submit","n_clicks"),
    State("pred-input-tweet","value")
)
def predict_topic(n_clicks, input_tweet):
    if n_clicks:
        return str(topic_predict(input_tweet))