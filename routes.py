import dash_bootstrap_components as dbc
from dash import html, callback, no_update
from dash.dependencies import Input, Output

from utils.constants import *

from pages.sentiment import sentiment
from pages.topics import topics
from pages.classify_tweet import classify_tweet
from pages.auth import login

from flask_login import logout_user, current_user

def is_authenticated(page_layout):
    if current_user.is_authenticated:
        return page_layout
    else:
        return login.layout

@callback(
    Output("redirect-url","data"),
    Input("url","pathname")
)
def store_redirect_url(pathname):
    if current_user.is_authenticated:
        return ''
    else:
        return pathname

@callback(
    Output("page-content", "children"), 
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == sentiment_page_location or pathname == '/sentiment':
        # return sentiment.layout
        return is_authenticated(sentiment.layout)
    elif pathname == topic_page_location:
        return is_authenticated(topics.layout)
    elif pathname == classify_tweet_page_location:
        return is_authenticated(classify_tweet.layout)
    elif pathname == logout_url:
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            # return html.Div('FAILED LOGOUT',style={"font-color":"white"})
            return no_update
    elif pathname == login_page_location:
        if current_user.is_authenticated:
            return no_update
        else:
            return login.layout
        
    # If the user tries to reach a different page, return a 404 message
    else:
        return html.Div(
            html.Div(
                dbc.Container(
                    [
                        html.H1("404: Not found", className="text-danger"),
                        html.Hr(),
                        html.P(f"The pathname {pathname} was not recognised..."),
                    ],
                    fluid=True,
                    className="py-3",
                ),
                className="p-3 bg-light rounded-3 mx-auto",
            ),
            className="p-3",
        )
