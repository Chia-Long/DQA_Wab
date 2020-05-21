import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
#import dash
#import pandas as pd
#from datetime import datetime

from app import app
from flask_login import logout_user, current_user
from apps import WebInput, WebOutput, Systems, LAN_Detail, Login
app.config.suppress_callback_exceptions = True
#filename='component_project.csv'
#df = pd.read_csv(filename)
#proj_list = list(df['Product_Name'].unique())

app.layout = html.Div([
    dcc.Location(id='p0-url', refresh=True),
    dcc.Location(id='p0-url1', refresh=True),
    dcc.Location(id='p0-url2', refresh=True),
    dcc.Location(id='p0-url3', refresh=True),
    dcc.Location(id='p0-url4', refresh=True),
    dcc.Location(id='p0-url5', refresh=True),
    dcc.Location(id='p0-url6', refresh=True),
    dcc.Location(id='p0-url7', refresh=True),
    dcc.Location(id='p0-url8', refresh=True),
    dcc.Location(id='p0-url9', refresh=True),
    dcc.Location(id='p0-url10', refresh=True),
    dcc.Location(id='p0-url11', refresh=True),
    dcc.Location(id='p0-url12', refresh=True),
    html.A([html.Img(id='p0-logo', src='/assets/Advantech-logo-200P-color.jpg', width='150',
                     style={'display': 'inline-block', 'margin': '10px 15px',}),
    ], href='http://172.17.9.206/'),
    html.A([html.Label('CIoT DQA Database', style={'display': 'inline-block',
                                          'fontFamily': 'Arial',
                                          'fontSize': '20pt',
                                          'textAlign': 'center',
                                          'verticalAlign': 'middle',
                                          'margin': '0px'}),
    ], href='/'),
	html.A([html.Label('®', style={'display': 'inline-block',
                                          'fontFamily': 'Arial',
                                          'fontSize': '20pt',
                                          'textAlign': 'center',
                                          'verticalAlign': 'middle',
                                          'margin': '0px 0px 0px 0px'}),
    ], href='http://172.17.9.218:8000/'),
    html.A([html.Img(src='/assets/faq.png', title='User Guide',
                     style={'height': '40px',
                            'width': '40px',
                            'display': 'inline-block',
                            'float': 'right',
                            #'position': 'relative',
                            'marginTop': '10px',
                            'marginRight': '20px'})
    ], href='/assets/NCG_DQA_Database_User_Guide_V01_03-Jan-2020_release.pdf', target='_blank'),
    html.A([html.Img(src='/assets/server.png', title='Create Data',
                     style={'height': '40px',
                            'width': '40px',
                            'display': 'inline-block',
                            'float': 'right',
                            #'position': 'relative',
                            'marginTop': '10px',
                            'marginRight': '10px'})
    ], href='/apps/Login', id='login'),
    html.A([html.Img(src='/assets/output.png', title='View Data',
                     style={'height': '40px',
                            'width': '40px',
                            'display': 'inline-block',
                            'float': 'right',
                            #'position': 'relative',
                            'marginTop': '10px',
                            'marginRight': '10px'})
    ], href='/apps/WebOutput'),
	html.Div(id='logout', style={'lineHeight': '40px', 'fontFamily': 'Arial','fontSize': '12pt','textAlign': 'center','verticalAlign': 'middle','display': 'inline-block','float': 'right','marginTop': '10px','marginRight': '10px'}),
    html.Div(id='user-name', style={'lineHeight': '40px', 'fontFamily': 'Arial','fontSize': '12pt','textAlign': 'center','verticalAlign': 'middle','display': 'inline-block','float': 'right','marginTop': '10px','marginRight': '10px'}),




    
    #html.A([html.Img(src='/assets/home.png', title='Go to Home',
    #                     style={'height': '40px',
    #                            'width': '40px',
    #                            'display': 'inline-block',
    #                            'float': 'right',
    #                            #'position': 'relative',
    #                            'margin-top': '10px',
    #                            'margin-right': '10px'})
    #], href='/'),
    #dcc.Interval(id='p0-interval-component', interval=1*1000, n_intervals=0),
    #html.Hr(style={'margin': '0px 0px 10px 0px', 'lineHeight': '10px'}),
    html.Div(id='page-content'),
])

'''style={'backgroundImage': 'url(/assets/background.jpg)',
          'backgroundSize': '100%',
          'backgroundRepeat': 'no-repeat',
          'height': '1080px'})'''

@app.callback([Output('page-content', 'children'),Output("P3-tabs", "value")],
              [Input('p0-url1', 'pathname')])
def display_page(pathname):
    #print(pathname)
    if pathname is None:
        raise PreventUpdate
    elif pathname == '/':
        return WebOutput.layout, "tab-1"
        #return html.Div([
        #    dcc.Link('Go to Component Page', href='/apps/WebComponent'),
        #    html.Br(),
        #    dcc.Link('Go to System Input Page', href='/apps/WebInput'),
        #    html.Br(),
        #    dcc.Link('Go to Output Page', href='/apps/WebOutput'),
        #])
    #elif pathname == '/apps/WebComponent':
    #    return WebComponent.layout
    elif pathname == '/apps/Login':
        logout_user()
        return Login.layout, "tab-1"
    elif pathname == '/apps/WebInput':
        return WebInput.layout, "tab-1"
    elif pathname == '/apps/WebOutput':
        return WebOutput.layout, "tab-1"
    elif pathname == '/apps/WebOutput/CPU_Performance':
        return WebOutput.layout, "tab-2"
    elif pathname == '/apps/WebOutput/Memory_Performance':
        return WebOutput.layout, "tab-2"
    elif pathname == '/apps/WebOutput/Storage_Performance':
        return WebOutput.layout, "tab-2"
    elif pathname == '/apps/WebOutput/LAN_Performance':
        return WebOutput.layout, "tab-2"
    elif pathname == '/apps/WebOutput/Certification_Output':
        return WebOutput.layout, "tab-1"
    elif '/apps/System_Information' in pathname:
        return Systems.layout, "tab-1"
    elif '/apps/WebOutput/Frame_Loss' in pathname:
        return LAN_Detail.layout, "tab-1"
    #elif '/apps/WebOutput' in pathname:
    #    return WebOutput.layout
    else: 
        return 404, "tab-1"
        #return 404,['SKY-8101']


#@app.callback(Output('output-provider', 'children'),
#              [Input('url', 'pathname')],
#              [State('P3-drp1', 'value')])
#def update_output(pathname,value):
#        if pathname is None:
#            return ''
#        dbname = "datatest.csv"
#        newpd = currentdb.append({'P3-drp1': value}, ignore_index=True)
#        newpd.to_csv(dbname, index=False, header=True)
#        return "Upload Successfully"

        
if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0',port=8050)
    #app.run_server(debug=True)
   
