import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
from app import app
from apps import Certification_Output, Performance, Compatibility

import pandas as pd  

filename='data/component_project.csv'
df = pd.read_csv(filename)
df.sort_values('Product Name', inplace=True)
projects = df['Product Name']
projects_id = df['ID']
#proj_list = list(df['Product_Name'].unique())
#proj_datalist = [html.Option(value=i) for i in proj_list]

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'borderRadius': '12px 12px 0px 0px',
    'backgroundColor': '#F3F3F3',
    'padding': '6px',
    'fontWeight': 'bold',
    'width': '20%',
    'fontFamily': 'Arial'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'borderRadius': '12px 12px 0px 0px',
    #'backgroundColor': '#119DFF',
    #'backgroundColor': 'rgb(83,141,213)',
    'backgroundColor': '#007BFF',
    'color': 'white',
    'padding': '6px',
    'width': '20%',
    'fontFamily': 'Arial'
}

layout = html.Div([
    #html.H3('Output Page'),
    html.Label('請輸入案件名稱：', style={'display': 'inline-block', 'fontFamily': '微軟正黑體', 'fontWeight': 'bold', 'fontSize': '14pt', 'marginLeft':  '5px', 'marginBottom': '0px', 'verticalAlign': 'middle'}),
    html.Div([
        #html.Font("Model Name："),
        dcc.Dropdown(
            id="P3-drp1",
            multi=True,
            #options=[{'label': name, 'value': name} for name in proj_list],
            options=[{'label': i, 'value': j} for i, j in zip(projects, projects_id)],
            #value="FWA-6170"
            placeholder="Select Product Name...",
            persistence=True,
            persistence_type='session',
            #style={'fontFamily': 'Arial'}
            #disabled=True
        ),
    ],style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'middle'}),
    html.Div(id="P3-test1"),
    dcc.Interval(id='P3-interval', interval=10000, n_intervals=0),
    #html.H4(children=' '),
    html.Div(style={'height': '12px'}),
    dcc.Tabs(id="P3-tabs", value='tab-1', children=[
        dcc.Tab(label='Certification', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Performance', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Compatibility', value='tab-3', style=tab_style, selected_style=tab_selected_style),
    ]),

    html.Div(id="P3-tab_content"),
    #dcc.Location(id='p3-url', refresh=False),

    #dcc.Link('Go to home', href='/')
])

#@app.callback(Output("P3-drp1", "options"),
#              [Input("P3-tabs", "value"),Input('url', 'pathname')],
#)
#def update_options(tab,pathname):
#    if tab == "tab-2":
#        if pathname == '/apps/WebOutput':
#            return [{'label': i, 'value': j, 'disabled': True } for i, j in zip(projects, projects_id)]
#        else:
#            return [{'label': i, 'value': j} for i, j in zip(projects, projects_id)]
#    else:
#        return [{'label': i, 'value': j} for i, j in zip(projects, projects_id)]
                
    
@app.callback(Output("P3-tab_content", "children"),          
             [Input("P3-tabs", "value")],)
def render_content(tab):
    """
    For user selections, return the relevant tab
    """
    #print (tab,pathname)
    if tab == "tab-1":
        return Certification_Output.layout
    elif tab == "tab-2":
        #if pathname == '/apps/WebOutput/CPU_Performance/Integer_Speed(Base)':
        #    return picperformance.layout    
        #if pathname == '/apps/WebOutput/CPU_Performance':
        #    return allperformance.layout    
        #elif pathname == '/apps/WebOutput/LAN_Performance':
        #    return lanperformance.layout  
        #elif pathname == '/apps/WebOutput':
        return Performance.layout
    elif tab == "tab-3":
        return Compatibility.layout 
    else:
        return Performance.layout

