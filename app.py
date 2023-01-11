import os
import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import flask
from layout.layout import layout
from flask_login import LoginManager
from env.config import DB_NAME

server = flask.Flask(__name__)

app = Dash(__name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    # external_scripts=
)

app.layout = layout

#server config
server = app.server
# server.config['SERVER_NAME']='uitm-orm.test:8050'
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(server.instance_path, DB_NAME)}.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

from models import User, db

#initiate db
db.init_app(server)

#create db if not exist
if not os.path.exists(f"instance/{DB_NAME}.db"):
    with server.app_context():
        db.create_all()
    print(f"database '{DB_NAME}.db' created")
# else:
#     print(f"database '{DB_NAME}.db' already exists")


#setup LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#callback to change tab title
app.clientside_callback(
    """
    function(pathname) {
        if (pathname == '/'){
            pathname = '/reputation'
        } 
        else if (pathname == '/logout'){
            pathname = '/login'
        }
        title = pathname.substr(1)
        title = title.charAt(0).toUpperCase() + title.slice(1)
        document.title = title + " | UiTM Online Reputation"
    }
    """,
    Output('tab-title', 'children'),
    Input('url', 'pathname')
)