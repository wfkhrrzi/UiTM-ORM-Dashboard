import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import flask
from layout.layout import layout

from env.config import APP_DEBUG

server = flask.Flask(__name__)

app = Dash(__name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    # external_scripts=
)

app.layout = layout

server = app.server
