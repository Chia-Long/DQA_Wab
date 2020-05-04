import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app, User
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
import pandas as pd

style=login_style = {
    #'display': 'inline-block',
    #'float': 'right',
    'margin-left': '15px',
	'margin-top': '10px',
    #'fontFamily': '微軟正黑體',
	'fontFamily': 'Arial',
    'fontWeight': 'bold',
    'fontSize': '12pt',
}
#df_user = pd.DataFrame(columns=['User'])


layout = html.Div(
    children=[
        html.Div(
            #className="container",
            children=[
                dcc.Location(id='url_login', refresh=True),
                html.Div('''Sign In''', id='h1'),
                html.Div(
                    # method='Post',
                    children=[
                        dcc.Input(
                            placeholder='Enter your username',
                            type='text',
                            id='uname-box'
                        ),
                        html.Br(),
                        html.Br(),
                        dcc.Input(
                            placeholder='Enter your password',
                            type='password',
                            id='pwd-box'
                        ),
                        html.Br(),
                        html.Br(),
                        dbc.Button(
                            "Sign In", 
                            color="primary", 
                            className="mr-1", 
                            n_clicks=0, 
                            #type='submit', 
                            id='login-button'
                        ),
                        html.Div(children='', id='output-state')
                    ]
                ),
            ], style=login_style
        )
    ]
)



@app.callback(Output('url_login', 'pathname'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def sucess(n_clicks, input1, input2):
    user = User.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/apps/WebInput'
        else:
            pass
    else:
        pass


@app.callback(Output('output-state', 'children'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
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
