import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from utils.constants import classify_tweet_page_location,sentiment_page_location,topic_page_location,logout_url
from flask_login import current_user

navbar =  dbc.Navbar(
    dbc.Container(
        [
            
            dbc.NavbarBrand("UiTM Online Reputation", href=sentiment_page_location),
            
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            dbc.Collapse(

                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Sentiment",href=sentiment_page_location),class_name="px-md-2"),
                        dbc.NavItem(dbc.NavLink("Topic",href=topic_page_location),class_name="px-md-2"),
                        dbc.NavItem(dbc.NavLink("Classify Tweet",href=classify_tweet_page_location),class_name="px-md-2"),
                        dbc.NavItem(dbc.NavLink("Logout",href=logout_url),id="logout-nav",class_name="px-md-2"),
                    ],
                    navbar=True,
                    class_name="ms-auto"
                ),

                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
            
        ],
    ),
    # color="dark",
    dark=True,
    class_name="mb-1",
    # id="layout-navbar",
)

layout = html.Div(
    [
        dcc.Location(id="url",refresh=False),
        dcc.Store(id="redirect-url"),
        html.Div(id='tab-title'),
        html.Div(id="layout-navbar-container"),
        html.Div(id="page-content"),
        html.Div(className="mb-5")
    ],
    # fluid=True
)

@callback(
    Output("layout-navbar-container","children"),
    Input("url","pathname")
)
def show_navbar(pathname):
    if current_user:
        if hasattr(current_user, 'is_authenticated'):
            if current_user.is_authenticated and pathname != logout_url:
                return navbar
    return None

# @callback(
#     # Output("layout-navbar","style"),
#     Output("logout-nav","style"),
#     Input("url","pathname")
# )
# def show_logout(pathname):
#     if hasattr(current_user, 'is_authenticated'):
#         if current_user.is_authenticated and pathname != logout_url:
#             return [{"display":"initial"} for i in range(2)]
#     return [{"display":"none"} for i in range(2)]

@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


