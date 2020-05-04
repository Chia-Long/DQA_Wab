import dash
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime as dt
import dash_table as dst
from pandas.core.frame import DataFrame
from collections import OrderedDict



df = pd.read_csv("data/component_project.csv")
dfc = pd.read_csv("data/component_cpu.csv")
dfm = pd.read_csv("data/component_memory.csv")
df1 = pd.read_csv('data/Test_Item_model_CPU.csv')
df2 = pd.read_csv("data/Test_Item_model_Memory.csv")
df3 = pd.read_csv("data/Test_Item_model_Storage.csv")
df4 = pd.read_csv("data/Test_Item_model_LAN.csv")
df5 = pd.read_csv("data/Certification.csv")

df5_empty = df5.iloc[0:0]
df5_empty = df5_empty.append(pd.Series(), ignore_index=True)
df_status = df5_empty.iloc[:1, 3::3]
df_link = df5_empty.iloc[:1, 4::3]
df_date = df5_empty.iloc[:1, 5::3]

#讀取column name
namelist = []
status = []
link = []
date = []
for col in df5.columns:
    namelist.append(col)
status = namelist[3::3]
link = namelist[4::3]
date = namelist[5::3]


models = df['Model Name']
models_id = df['ID']
projects = df['Product Name']
projects_id = df['ID']
cpus = dfc['Processor Name']
cpus_id = dfc['ID']


drop_style = {
    'width': '20%', 
    'height': '100%',
    'display': 'inline-block'
}



df_drop = pd.DataFrame(OrderedDict([(i, ['Y', 'D', 'A']) for i in status]))


def create_layout(app):
    # Page layouts
    return html.Div([
        #page1
        dcc.Interval(
            id='interval-cer',
            interval=5000,
            n_intervals=0
        ),
        html.H2('Certification'),
        html.Div([
            html.Label('Product Name'),
            dcc.Dropdown(
                id='p2_cer_product',
                options=[{'label': i , 'value': j} for i,j in zip(projects,projects_id)],
            )
        ], style=drop_style),
        
        html.Div([
            html.Label('Test Date'),
            dcc.DatePickerSingle(
                id='p2_cer_date',
                min_date_allowed=dt(2000, 1, 1),
                max_date_allowed=dt(2099, 12, 31),
                initial_visible_month=dt.today(),
            )
        ]),
        html.H4('Certification Status'),
        html.Div([
            html.Div(generate_dropdown_table(df_status)),
        ], style={'width': '100%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}
        ),
        html.H4('Link'),
        html.Div([
            html.Div(generate_table_link(df_link)),
        ], style={'width': '100%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}
        ),
        html.H4('Certification Date(YYYY-MM-DD)'),        
        html.Div([
            html.Div(generate_table(df_date)),
        ], style={'width': '100%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.ConfirmDialogProvider(
                children=html.Button(
                    'Submit',
                ),
                id='p2_provider_cer',
                message='Do you want to update the information?'
            ),
        ]),
        #row5
        html.Div([
            html.Div(id='p2_output-provider_cer')
        ], style={'width': '100%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
        html.Br(),
    ])


#------------- Generate table --------------

def generate_dropdown_table(dataframe):
    return dst.DataTable(
            id='p2_editing_table_cer',
            columns=[
              {'name': c, 'id': c, 'editable': (c != 'Test Item'), 'presentation': 'dropdown'} for c in dataframe.columns],
            data=dataframe.to_dict('rows'),
            editable=True,
            style_header={
                'backgroundColor': '#3D9970',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'color': 'white'
            },
            style_cell={'height': 'auto','minWidth': '150px', 'width': '150px', 'maxWidth': '150px','textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis'},
            dropdown={j : {'options': [{'label': i, 'value': i} for i in df_drop[j].unique()]} for j in status}
        )

#------------- Generate table --------------

def generate_table(dataframe):
    return dst.DataTable(
            id='p2_editing_table_cer_date',
            columns=[
              {'name': c, 'id': c, 'editable': (c != 'Test Item'), 'type': 'datetime'} for c in dataframe.columns],
            data=dataframe.to_dict('rows'),
            editable=True,
            #placeholder="Select User",
            style_header={
                'backgroundColor': '#3D9970',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'color': 'white'
            },
            style_cell={'height': '30px','minWidth': '150px', 'width': '150px', 'maxWidth': '150px','textAlign': 'center','whiteSpace': 'normal','overflow': 'hidden', 'textOverflow': 'ellipsis'},
        )


#------------- Generate table --------------

def generate_table_link(dataframe):
    return dst.DataTable(
            id='p2_editing_table_cer_link',
            columns=[
              {'name': c, 'id': c, 'editable': (c != 'Test Item')} for c in dataframe.columns],
            data=dataframe.to_dict('rows'),
            editable=True,
            style_header={
                'backgroundColor': '#3D9970',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'color': 'white'
            },
            style_cell={'height': '30px','minWidth': '150px', 'width': '150px', 'maxWidth': '150px','textAlign': 'center','whiteSpace': 'normal','overflow': 'hidden', 'textOverflow': 'ellipsis'},
        )
#------------- callback test item model Table --------------

@app.callback(Output('p2_output-provider_cer', 'children'),
                  [Input('p2_provider_cer', 'submit_n_clicks'), Input('p2_editing_table_cer', 'data'), Input('p2_editing_table_cer_link', 'data'), Input('p2_editing_table_cer_date', 'data')],
              [State('p2_cer_product', 'value'), State('p2_cer_date', 'date')])
def update_output(submit_n_clicks, rows, links, dates, prov, timev):
        if not submit_n_clicks:
            return ''
        else:
            dbname = "data/Certification.csv"
            #print(rows)
            currentdb = pd.read_csv(dbname, dtype=str)
            index_value = currentdb[currentdb['Product_Name'] == prov].index.tolist()#透過test_id找dataframe的index
            newdb = currentdb.drop(index_value)#透過index刪除重複的row
            

            status_F = pd.DataFrame(rows)
            links_F = pd.DataFrame(links)
            Date_F = pd.DataFrame(dates)
            info_F = pd.DataFrame({'Model_Name': prov, 'Product_Name': prov, 'Test_Date': timev}, index=[0])

            newpd = pd.concat([status_F, links_F, Date_F, info_F], axis=1, sort=False)
            newpd = newpd[namelist]

            newpd1 = pd.concat([newdb,newpd], sort=False , ignore_index=True, join_axes=[newpd.columns]) #dropdown的data與table的data dataframe合併
            #print(newpd1)
            #newpd2 = newpd1.combine_first(newpd) #刪除重複的column
            #print(newpd2)


            if prov is None:
                return "Upload Fail"
            else:
                newpd1.to_csv(dbname, index=False, header=True, encoding='utf-8-sig')
                currentdb = pd.read_csv(dbname)
                print(currentdb)
                return "Upload Successfully"


#------------- callback data from csv --------------
@app.callback([Output('p2_cer_date', 'date'), Output('p2_editing_table_cer', 'data'), Output('p2_editing_table_cer_link', 'data'), Output('p2_editing_table_cer_date', 'data')],
                [Input('p2_cer_product', 'value')])
def update_value(value):
    now = dt.now().strftime("%Y-%m-%d")
    dbname2 = "data/Certification.csv"
    currentdb2 = pd.read_csv(dbname2)
    status = namelist[3::3]
    link = namelist[4::3]
    date = namelist[5::3]
    #empty_test = [now, [{'RHEL_Cerification': None, 'RHEL_OpenStack_Ready': None, 'VMware_vSAN_ReadyNode': None, 'Intel_ISS_NFVI_v2': None, 'Intel_ISS_uCPE': None, 'Intel_ISS_Visual_Cloud_Delivery_Network': None, 'Intel_ISS_Microsoft_SQL_Server': None, 'Intel_ISS_VMware_vSAN': None}]]
    empty_test = [now, [{ i : None for i in status }], [{ i : None for i in link }], [{ i : None for i in date }]]
    modellist = currentdb2['Product_Name'].tolist()
    
    if value not in modellist:
        return empty_test

    dictOfvalue_status_list = []
    dictOfvalue_link_list = []
    dictOfvalue_date_list = []    
    #取data
    df_value = currentdb2[currentdb2['Product_Name'] == value]
    value_list = df_value.iloc[0].tolist()
    date_list = value_list[2:3]
    status_value_list = value_list[3::3]
    link_value_list = value_list[4::3]
    date_value_list = value_list[5::3]

    
    #Datatable的data為list(dist)，先將資料轉成dict再存到list中



    #listOfStr = ["RHEL_Cerification", "RHEL_OpenStack_Ready", "VMware_vSAN_ReadyNode", "Intel_ISS_NFVI_v2", "Intel_ISS_uCPE", "Intel_ISS_Visual_Cloud_Delivery_Network", "Intel_ISS_Microsoft_SQL_Server", "Intel_ISS_VMware_vSAN"]
    zipbObj = zip(status, status_value_list)
    dictOfvalue_status = dict(zipbObj) #轉dict
    dictOfvalue_status_list.append(dictOfvalue_status) #加入list
    date_list.append(dictOfvalue_status_list) #將table的data加入

    zipbObj2 = zip(link, link_value_list)
    dictOfvalue_status2 = dict(zipbObj2) #轉dict
    dictOfvalue_link_list.append(dictOfvalue_status2) #加入list
    date_list.append(dictOfvalue_link_list) #將table的data加入

    zipbObj3 = zip(date, date_value_list)
    dictOfvalue_status3 = dict(zipbObj3) #轉dict
    dictOfvalue_date_list.append(dictOfvalue_status3) #加入list
    date_list.append(dictOfvalue_date_list) #將table的data加入
    #print(date_list)
    return date_list



#--------------live update dropdown value-----------------------------
@app.callback([Output('p2_cer_product','options')],
              [Input('interval-cer', 'n_intervals')])
def update_model_options(n):
    df = pd.read_csv("data/component_project.csv")
    #models = df['Model Name']
    #models_id = df['ID']
    projects = df['Product Name']
    projects_id = df['ID']

    return [[{'label': i1 , 'value': j1} for i1,j1 in zip(projects,projects_id)]]
