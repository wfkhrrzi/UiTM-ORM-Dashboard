import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

from app import app

from utils.constants import classify_tweet_page_location,sentiment_page_location,topic_page_location

from pages.sentiment import sentiment
from pages.topics import topics
from pages.classify_tweet import classify_tweet


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == sentiment_page_location or pathname == '/sentiment':
        return sentiment.layout
    elif pathname == topic_page_location:
        return topics.layout
    elif pathname == classify_tweet_page_location:
        return classify_tweet.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )