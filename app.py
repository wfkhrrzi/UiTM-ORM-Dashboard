import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from env.config import APP_DEBUG

app = Dash(__name__,
    # server=server,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    # external_scripts=
)

navbar =  dbc.Navbar(
    dbc.Container(
        [
            
            dbc.NavbarBrand("UiTM Online Reputation", href="/"),
            
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            dbc.Collapse(
                
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink("Sentiment",href=dash.page_registry['pages.sentiment.sentiment']['path']),
                            class_name="px-md-2"
                        ),
                        dbc.NavItem(dbc.NavLink("Topic",href=dash.page_registry['pages.topics.topics']['path']),class_name="px-md-2"),
                        dbc.NavItem(dbc.NavLink("Classify Tweet",href=dash.page_registry['pages.classify_tweet.classify_tweet']['path']),class_name="px-md-2"),
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
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

app.layout = html.Div(
    [
        navbar,
        dash.page_container,
        html.Div(className="mb-5")
    ],
    # fluid=True
)

if __name__=="__main__":
    app.run(
        debug=APP_DEBUG,
        # dev_tools_hot_reload=False,
    )
