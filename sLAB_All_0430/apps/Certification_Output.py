import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_table 
from app import app
from dash.dependencies import Input, Output, State, ClientsideFunction
import numpy as np
#app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
application = app.server

#filename='component_project.csv'
#df1 = pd.read_csv(filename, index_col="Product_Name")
#proj_list = list(df1['Product_Name'].unique())

df_pj = pd.read_csv("data/component_project.csv", index_col="ID")
product_name = df_pj['Product Name'].to_list()
project_id = df_pj.index.to_list()

df_cert = pd.read_csv("data/Certification.csv", index_col="Product_Name")
df_cert['Product_Name'] = df_cert.index
df_cert.replace(project_id, product_name, inplace=True)
#print(df_cert)
#df_c=df.ix[[0],[2]]

#讀取column name
namelist = []
status = []
link = []
date = []
for col in df_cert.columns:
    namelist.append(col)

status = namelist[0:2] +namelist[2::3]
status.remove('Product_Name') #Status column Name
link = namelist[0:2] + namelist[3::3]#Link column Name
date = namelist[0:2] + namelist[4::3]#date column Name

def generate_table(dataframe, date):
    return dash_table.DataTable(
            # table-head
            id='P3-Certification-all',
            columns=[
              {'name': ['Certification Summary', c.replace("_", " ")], 'id': c, "hideable": True} for c in dataframe.columns
            ],
            #editable=True,
            # table-row
            data=dataframe.to_dict('rows'),
            merge_duplicate_headers=True,
            row_deletable=False,
            sort_action='native',
            css=[{"selector": ".show-hide", "rule": "display: none"}],
            style_data_conditional=[
                     {
                         'if': {
                             'row_index': 'odd',
                         },
                         'backgroundColor': 'rgb(235,240,236)',
                         'color': 'black',
                         'fontSize': '15px',
                         'fontWeight': 'bold',
                         'textAlign': 'center',
                         'border': '1px solid white',
                     },
                     {
                         'if': {
                             'row_index': 'even',
                         },
                         'backgroundColor': 'rgb(213,224,214)',
                         'color': 'black',
                         'fontSize': '15px',
                         'fontWeight': 'bold',
                         'textAlign': 'center',
                         'border': '1px solid white',
                     }
            ],
            style_header=(
                     {
                         'whiteSpace': 'normal',
                         'height': 'auto',
                         'minWidth': '110px',
                         'width': '110px',
                         'maxWidth': '110px',
                         #'width': '120px',
                         'backgroundColor': 'rgb(114,164,118)',
                         'fontSize': '15px',
                         'fontWeight': 'bold',
                         'color': 'white',
                         'border': '1px solid white',
                         'textAlign': 'center',
                     }
                     ),
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}  for column, value in row.items()} for row in date.to_dict('rows')
            ],
            #tooltip_duration=None,
            )

layout = html.Div([
    html.Div([],style={'height': '12px'}),
    html.Div(
        dcc.RadioItems(
            id = 'cer_radio', 
            options=[
                {'label': 'Show All', 'value': 'all'},
                {'label': 'Certified', 'value': 'Y'},
                {'label': 'Testing', 'value': 'D'},
                {'label': 'Applied', 'value': 'A'},
            ],
            value='all',
            labelStyle = []
        ),
    ),
    html.Div(id="P3-Certification_content"),
    html.A('Y: Certified  D: Testing  A: Applied'),
])
        

@app.callback(Output("P3-Certification_content", "children"),
              [Input("P3-drp1", "value"), Input("cer_radio", "value")],
              #[State('P3-Certification-all', 'data'), ]
              )
def update_output(value,radio):
    global df_cert
    df_cert_temp = pd.read_csv("data/Certification.csv", index_col="Product_Name")
    df_cert_temp['Product_Name'] = df_cert_temp.index
    df_cert_temp.replace(project_id, product_name, inplace=True)
    df_cert = df_cert_temp.copy()
    last_column = df_cert.shape[1]-2
    column_list = [-1, 1]
    date_column_list = [-1, 1]
    
    #Status column list
    for i in range(2,last_column,3):
        column_list.append(i)

    #date column list
    for i in range(4,df_cert.shape[1],3):
        date_column_list.append(i)
    df_date = df_cert.ix[:, date_column_list] #取df_date dataframe
    df_date.columns = status #取代column name


    if radio == 'Y':
        df_cert = df_cert.replace(['D','A'],[None,None])
    elif radio == 'D':
        df_cert = df_cert.replace(['Y','A'],[None,None])
    elif radio == 'A':
        df_cert = df_cert.replace(['Y','D'],[None,None])
    else:
        pass


    if value is None:
        df_c = df_cert.ix[:, column_list]
        
        print(df_cert)
        print('========df_c==========')
        print(df_c)
        return generate_table(df_c, df_date)
    elif len(value) == 0:
        df_c = df_cert.ix[:, column_list]
        return generate_table(df_c, df_date)
    else:
        value_f = value.copy()
        for i in value:
            if i in df_cert.index.to_list():
                continue
            else:
                value_f.remove(i)
        df_c = df_cert.ix[list(value_f), column_list]
        df_date = df_cert.ix[list(value_f), date_column_list]
        df_date.columns = status
        return generate_table(df_c, df_date)


