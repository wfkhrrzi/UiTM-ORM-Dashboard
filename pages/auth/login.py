import dash_bootstrap_components as dbc
from dash import html,callback,dcc, no_update
from dash.dependencies import Input, Output, State

from models import User
from flask_login import login_user
from werkzeug.security import check_password_hash

layout = html.Div(
    [
        dbc.Container(
            [
                html.Div("UiTM Online Reputation", id='h1', className="mb-3 text-center fw-bold fs-3"),
                dbc.Form(
                    [
                        html.Div(
                            [
                                dbc.Label("Username", html_for="uname-box"),
                                dbc.Input(
                                    placeholder='Enter your username',
                                    # value="jeb",
                                    n_submit=0,
                                    type='text',
                                    id='uname-box',
                                ),
                                # dbc.FormText("Are you on email? You simply have to be these days",color="secondary"),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            [
                                dbc.Label("Password", html_for="pwd-box"),
                                dbc.Input(
                                    placeholder='Enter your password',
                                    # value="pass123",
                                    n_submit=0,
                                    type='password',
                                    id='pwd-box',
                                ),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            dbc.Button(
                                children='Login',
                                n_clicks=0,
                                type='submit',
                                id='login-button',
                            ),
                            className="mb-3 text-center",
                        ),
                        html.Div(children='', id='output-state')
                    ],
                    method="post"
                ),                        
            ],
            fluid=True,
            class_name="bg-light rounded p-3",
            style={
                "max-width":"400px",
            }
        ),
    ],
    className="p-3 d-flex justify-content-center align-items-center",
    style={
        "height":"calc(100vh - 76px)",
    }
)

@callback(Output('url', 'pathname'),
    [Input('login-button', 'n_clicks'),
    Input('uname-box', 'n_submit'),
    Input('pwd-box', 'n_submit')],
    [State('uname-box', 'value'),
    State('pwd-box', 'value'),
    State("redirect-url","data")]
)
def success(n_clicks, n_submit_uname, n_submit_pwd, input1, input2, data):
    user = User.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            if data:
                return data
            else:
                return '/'
        else:
            return no_update
    else:
        return no_update


@callback(Output('output-state', 'children'),
    [Input('login-button', 'n_clicks'),
    Input('uname-box', 'n_submit'),
    Input('pwd-box', 'n_submit')],
    [State('uname-box', 'value'),
    State('pwd-box', 'value')]
)
def update_output(n_clicks, n_submit_uname, n_submit_pwd, input1, input2):
    if n_clicks > 0 or n_submit_uname > 0 or n_submit_pwd > 0:
        user = User.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''