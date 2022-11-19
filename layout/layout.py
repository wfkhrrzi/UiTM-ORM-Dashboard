import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from utils.constants import classify_tweet_page_location,sentiment_page_location,topic_page_location

navbar =  dbc.Navbar(
    dbc.Container(
        [
            
            dbc.NavbarBrand("UiTM Online Reputation", href=sentiment_page_location),
            
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            dbc.Collapse(
                
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink("Sentiment",href=sentiment_page_location),
                            class_name="px-md-2"
                        ),
                        dbc.NavItem(dbc.NavLink("Topic",href=topic_page_location),class_name="px-md-2"),
                        dbc.NavItem(dbc.NavLink("Classify Tweet",href=classify_tweet_page_location),class_name="px-md-2"),
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
    class_name="mb-1"
)

# add callback for toggling the collapse on small screens
@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

layout = html.Div(
    [
        dcc.Location(id="url"),
        navbar,
        html.Div(id="page-content"),
        html.Div(className="mb-5")
    ],
    # fluid=True
)