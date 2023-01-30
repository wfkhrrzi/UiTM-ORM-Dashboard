import dash_bootstrap_components as dbc
from dash import html, callback, no_update
from dash.dependencies import Input, Output, State

from utils.constants import *

from pages.reputation import reputation
from pages.sentiment import sentiment
from pages.topics import topics
from pages.classify_tweet import classify_tweet
from pages.auth import login

from flask_login import logout_user, current_user

# @callback(
#     Output("redirect-url","data"),
#     Input("url","pathname")
# )
# def store_redirect_url(pathname):
#     if current_user.is_authenticated:
#         return ''
#     else:
#         return pathname

def is_authenticated(page_layout,page_url):
    if current_user.is_authenticated:
        return page_url,page_layout
    else:
        return f'{login_page_location}?redirect={page_url}',login.layout

@callback(
    Output("redirect-url-loc", "pathname"), 
    Output("page-content", "children"), 
    Input("url", "pathname"),
    State("redirect-url-loc", "pathname"),
)
def render_page_content(pathname, current_url):
    if pathname == reputation_page_location or pathname == '/':
        # return pathname,reputation.layout
        return is_authenticated(reputation.layout,pathname)
    elif pathname == sentiment_page_location:
        return is_authenticated(sentiment.layout,pathname)
    elif pathname == topic_page_location:
        return is_authenticated(topics.layout,pathname)
    elif pathname == classify_tweet_page_location:
        return is_authenticated(classify_tweet.layout,pathname)
    elif pathname == logout_url:
        if current_user.is_authenticated:
            logout_user()
    
        return login_page_location,login.layout

    elif pathname == login_page_location:
        if hasattr(current_user, 'is_authenticated'):
            if current_user.is_authenticated:
                # STILL TAK FIXED LOGIN REDIRECT AFTER LOGGED IN
                print('is_auth is true & current url is ',current_url)
                return (current_url, no_update)
            else:
                print('is_auth is not true')
                return (no_update, login.layout)
        else:
            return (no_update, no_update)
                    
    # If the user tries to reach a different page, return a 404 message
    else:
        return (
            no_update,       
            html.Div(
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
        )
