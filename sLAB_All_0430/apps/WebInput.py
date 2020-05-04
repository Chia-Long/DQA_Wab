#!/root/anaconda3/bin/python

import csv
import re
import time
import urllib
from datetime import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dst
#import callbacks
#import dash_auth
import pandas as pd
import plotly.graph_objs as go
from comtypes import CLSCTX_DISABLE_AAA
from dash.dependencies import ClientsideFunction, Input, Output, State
from flask import request

import users_mgt as um
from app import app
from apps import LAN, MLC, RMT, SPECCPU2017, Certification, Storage, Login
from users_mgt import add_user
from flask_login import logout_user, current_user


# VALID_USERNAME_PASSWORD_PAIRS = [
#    ['dqa', '00dqa']
# ]

# auth = dash_auth.BasicAuth(
#    app,
#    VALID_USERNAME_PASSWORD_PAIRS
# )

dfi = pd.read_csv("data/component_test_item.csv")
df1 = pd.read_csv('data/Test_Item_model_CPU.csv')
df2 = pd.read_csv("data/Test_Item_model_Memory.csv")
df3 = pd.read_csv("data/Test_Item_model_Storage.csv")
df4 = pd.read_csv("data/Test_Item_model_LAN.csv")
df5 = pd.read_csv("data/Test_Item_model_Certification.csv")

df_pro_item = pd.read_csv("data/Item_component_project.csv")
df_pro = pd.read_csv("data/component_project.csv")
pro_Name = df_pro['Product Name']

df_cpu_codename = pd.read_csv("data/cpu_codename.csv").sort_values("Code Name")
df_cpu_codename_list = df_cpu_codename['Code Name'].values.tolist()
df_memory_type = pd.read_csv("data/memory_type.csv")
df_memory_type_list = df_memory_type['Memory Types'].values.tolist()
df_storage_category = pd.read_csv("data/storage_category.csv")
df_storage_category_list = df_storage_category['Storage Device Category'].values.tolist()

# create table data
project_number = df_pro.shape[0] + 1
project_empty_data = ['', '', '']
df_pro_item['MP' + str(project_number)] = project_empty_data
df_pro_item['Example'] = ['SKY-1111','SKY-1111D','Admin']

df_cpu_item = pd.read_csv("data/Item_component_cpu.csv")
df_cpu = pd.read_csv("data/component_cpu.csv")
cpu_Name = df_cpu['Processor Name']
cpu_number = df_cpu.shape[0] + 1
cpu_empty_data = ['', '', '', '', '', '', '', '', '']
df_cpu_item['C' + str(cpu_number)] = cpu_empty_data
df_cpu_item['Example'] = ['Cascade_Lake_SP', '8260Y', '48', '48', '2.4', '3.9', '35.75', '165', 'Admin']

df_mem_item = pd.read_csv("data/Item_component_memory.csv")
df_mem = pd.read_csv("data/component_memory.csv")
mem_IDs = df_mem['Part Number']
mem_number = df_mem.shape[0] + 1
mem_empty_data = ['', '', '', '', '', '', '', '', '', '']
df_mem_item['M' + str(mem_number)] = mem_empty_data
df_mem_item['Example'] = ['Micron', 'MTA36ADS2G72PZ', 'DDR4_VLP_RDIMM', '288', 'Yes', '2133', '16', '2', '8Gb TwinDie', 'Admin']

df_sto_item = pd.read_csv("data/Item_component_storage.csv")
df_sto = pd.read_csv("data/component_storage.csv")
sto_IDs = df_sto['Storage Model Name']
sto_number = df_sto.shape[0] + 1
sto_empty_data = ['', '', '', '', '', '', '', '', '']
df_sto_item['S' + str(sto_number)] = sto_empty_data
df_sto_item['Example'] = ['M.2_NVMe_SSD', 'Intel', 'SSD_DC_P4610', '2.5" 7mm', 'PCIe Gen3 x4', '1.6TB', '3D NAND, 64-layer, TLC', 'Up to 15 Watt', 'Admin']

df_lan_item = pd.read_csv("data/Item_component_lan.csv")
df_lan = pd.read_csv("data/component_lan.csv")
lan_IDs = df_lan['Card Name']
lan_number = df_lan.shape[0] + 1
lan_empty_data = ['', '', '', '', '', '']
df_lan_item['L' + str(lan_number)] = lan_empty_data
df_lan_item['Example'] = ['Intel', 'X710-T4L', 'X710-TM4', '10Gb/5Gb/2.5Gb/1Gb/100Mb', '8.0GT/s, x8 lanes', 'Admin']

items = dfi[(dfi['ID'].apply(len) == 5)]['Name']
df_user = pd.read_csv("data/user.csv")
users = df_user['User']

tabs_styles = {
    'height': '30px'
}

tab_style = {
    'borderBottom': '',
    'padding': '1px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '1px',
    'fontWeight': 'bold'
}

drop_style = {
    'width': '20%',
    'height': '10%',
    'display': 'inline-block'
}

# --------------------layout---------------------------------
layout = html.Div([
    html.Div(
        id = 'create', children =[
        html.H1('Create User'),
        dcc.Input(
            id='user',
            type='text',
            placeholder='Enter user name'
        ),
        dcc.Input(
            id='password',
            type='text',
            placeholder='Enter password'
        ),
        dcc.Input(
            id='mail',
            type='email',
            placeholder='Enter e-mail'
        ),
        dcc.ConfirmDialogProvider(
            children=html.Button(
                'Submit'
            ),
            id='p1_create_user_sub',
            message='Do you want to Create user?'
        ),
        html.Hr()
    ], style={'width': '100%', 'height': '100%', 'float': 'left'}),
    html.H1('Create Component'),
    html.Div(id='p1_refresh_content', style={'display': 'hidden'}),
    html.Div([
        dcc.Tabs(id='p1_tabs', value='Project', children=[
            dcc.Tab(label='Project', value='Project', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='CPU', value='CPU', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Memory', value='Memory', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Storage', value='Storage', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='LAN', value='LAN', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
    ]),
    html.Div(id='tab-content'),
    html.Hr(),
    html.H1('Create Test Data'),
    html.Div([
        dcc.Dropdown(
            id='p2_item',
            options=[{'label': q, 'value': q} for q in items],
            placeholder="Select Test Item",
            clearable=False,
        ),
        dcc.Interval(
            id='interval-user',
            interval=5000,
            n_intervals=0
        ),
        dcc.Dropdown(
            id='p2_user',
            options=[{'label': q1, 'value': q1} for q1 in users],
            placeholder="Select User",
            clearable=False,
            disabled= False,
            style = {'display': 'none'}
        ),
    ], style={'width': '20%', 'height': '100%', 'float': 'left', 'display': 'inline'}),    
    html.Div(id='p1_create_user_sub_pro'),
    html.Div([
        dcc.Location(id="p2_url", refresh=False), html.Div(id="p2_page-content")
    ], style={'width': '100%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
    html.Br(),
])

#app.clientside_callback(
#    ClientsideFunction(namespace='reload', function_name='reloadPage'),
#    Output('p1_refresh_content', 'children'),
#    [Input('p1_output_pro', 'children')]
#)


@app.callback(Output('tab-content', 'children'),
              [Input('p1_tabs', 'value')])
def render_content(tab):
    if tab == 'Project':
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='p1_pro_drop',
                    options=[{'label': i, 'value': i} for i in pro_Name],
                    placeholder="Search Product Name"
                )
            ], style=drop_style),
            html.Br(),
            html.Div([
                dst.DataTable(
                    id='p1_pro_table',
                    columns=[{"name": i, "id": i, 'editable': (i != 'ID' and i != 'Example')} for i in df_pro_item.columns],
                    style_data_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c',
                    }],
                    style_header_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c'
                    }],
                    data=df_pro_item.to_dict('records'),
                    editable=True,
                    style_table={'width': '300px'},
                    style_cell={'minWidth': '150px', 'width': '150px'}
                )
            ]),

            html.Div([
                dcc.ConfirmDialogProvider(
                    children=html.Button(
                        'Submit',
                    ),
                    id='p1_pro_sub',
                    message='Do you want to update the information?'
                )
            ]),
            html.Div(id='p1_output_pro', style={'clear': 'both'})
        ])
    elif tab == 'CPU':
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='p1_cpu_drop',
                    options=[{'label': i, 'value': i} for i in cpu_Name],
                    placeholder="Search CPU Name"
                )
            ], style=drop_style),
            html.Br(),
            html.Div([
                dst.DataTable(
                    id='p1_cpu_table',
                    columns=[{"name": i, "id": i, 'editable': (i != 'ID' and i != 'Example')} for i in df_cpu_item.columns],
                    style_data_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c',
                    }],
                    style_header_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c'
                    }],
                    data=df_cpu_item.to_dict('records'),
                    editable=True,
                    style_table={'width': '300px'},
                    style_cell={'minWidth': '150px', 'width': '150px'}
                )
            ], style={'width': '50%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dst.DataTable(
                    id='p1_cpu_codename_table',
                    columns=[{"name": i, "id": i} for i in df_cpu_codename.columns],
                    data=df_cpu_codename.to_dict('records'),
                    editable=False,
                    style_table={
                        'width': '200px',
                        'maxHeight': '300px',
                        'overflowY': 'scroll'},
                    style_cell={'minWidth': '50px', 'width': '50px'}
                )
            ], style={'width': '50%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dcc.ConfirmDialogProvider(
                    children=html.Button(
                        'Submit'
                    ),
                    id='p1_cpu_sub',
                    message='Do you want to update the information?'
                )
            ], style={'width': '100%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
            html.Div(id='p1_output_cpu', style={'clear': 'both'})
        ])
    elif tab == 'Memory':
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='p1_mem_drop',
                    options=[{'label': i, 'value': i} for i in mem_IDs],
                    placeholder="Search Memory Name"
                )
            ], style=drop_style),
            html.Br(),
            html.Div([
                dst.DataTable(
                    id='p1_mem_table',
                    columns=[{"name": i, "id": i, 'editable': (i != 'ID' and i != 'Example')} for i in df_mem_item.columns],
                    style_data_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c',
                    }],
                    style_header_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c'
                    }],
                    data=df_mem_item.to_dict('records'),
                    editable=True,
                    style_table={'width': '300px'},
                    style_cell={'minWidth': '150px', 'width': '150px'}
                ),
            ], style={'width': '50%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dst.DataTable(
                    id='p1_memory_type_table',
                    columns=[{"name": i, "id": i} for i in df_memory_type.columns],
                    data=df_memory_type.to_dict('records'),
                    editable=False,
                    style_table={
                        'width': '200px',
                        'maxHeight': '300px',
                        'overflowY': 'scroll'},
                        style_cell={'minWidth': '150px', 'width': '150px'}
                )
            ], style={'width': '50%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dcc.ConfirmDialogProvider(
                    children=html.Button(
                        'Submit'
                    ),
                    id='p1_mem_sub',
                    message='Do you want to update the information?'
                )
            ], style={'width': '100%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
            html.Div(id='p1_output_mem', style={'clear':'both'})
        ])
    elif tab == 'Storage':
        return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='p1_sto_drop',
                    options=[{'label': i, 'value': i} for i in sto_IDs],
                    placeholder="Search Storage Name"
                )
            ], style=drop_style),
            html.Br(),
            html.Div([
                dst.DataTable(
                    id='p1_sto_table',
                    columns=[{"name": i, "id": i, 'editable': (i != 'ID' and i != 'Example')} for i in df_sto_item.columns],
                    style_data_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c',
                    }],
                    style_header_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c'
                    }],
                    data=df_sto_item.to_dict('records'),
                    editable=True,
                    style_table={'width': '300px'},
                    style_cell={'minWidth': '150px', 'width': '150px'}
                )
            ], style={'width': '50%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dst.DataTable(
                    id='p1_sto_category_table',
                    columns=[{"name": i, "id": i} for i in df_storage_category.columns],
                    data=df_storage_category.to_dict('records'),
                    editable=False,
                    style_table={
                        'width': '200px',
                        'maxHeight': '300px',
                        'overflowY': 'scroll'},
                    style_cell={'minWidth': '150px', 'width': '150px'}
                )
            ], style={'width': '50%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dcc.ConfirmDialogProvider(
                    children=html.Button(
                        'Submit'
                    ),
                    id='p1_sto_sub',
                    message='Do you want to update the information?'
                )
            ], style={'width': '100%', 'height': '100%', 'float': 'left', 'display': 'inline-block'}),
            #html.Div(id='p1_output_sto')
			html.Div(id='p1_output_sto', style={'clear': 'both'})
        ])
    elif tab == 'LAN':
        return html.Div([
            html.Div([
                dcc.RadioItems(
                    id='radio',
                    options=[
                        {'label': 'LAN Card', 'value': 'card'},
                        {'label': 'Onboard', 'value': 'ONBOARD'},
                    ],
                    value='card'
                ),
            ]),
            html.Div([
                dcc.Dropdown(
                    id='p1_lan_drop',
                    placeholder="Search LAN Card Name"
                    # options=[{'label': i , 'value': i} for i in lan_IDs],
                )
            ], style=drop_style),
            html.Br(),
            html.Div([
                dst.DataTable(
                    id='p1_lan_table',
                    columns=[{"name": i, "id": i, 'editable': (i != 'ID' and i != 'Example')} for i in df_lan_item.columns],
                    style_data_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c',
                    }],
                    style_header_conditional=[{
                    'if': {'column_id': 'Example'},
                    'backgroundColor': '#f2f2f2',
                    'color': '#8c8c8c'
                    }],
                    data=df_lan_item.to_dict('records'),
                    editable=True,
                    style_table={'width': '300px'},
                    style_cell={'minWidth': '150px', 'width': '150px'}
                )
            ]),
            html.Div([
                dcc.ConfirmDialogProvider(
                    children=html.Button(
                        'Submit'
                    ),
                    id='p1_lan_sub',
                    message='Do you want to update the information?'
                )
            ]),
            html.Div(id='p1_output_lan', style={'clear':'both'})
			
        ])

    # ------------- callback test item model Table --------------

# Reload page after submit button pressed
@app.callback(Output('p0-url1', 'href'),
              [Input('p1_output_pro', 'children')],)
def refresh_page(b_project):
    if b_project == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"


@app.callback(Output('p0-url2', 'href'),
              [Input('p1_output_cpu', 'children')],)
def refresh_page1(b_cpu):
    print(b_cpu)
    if b_cpu == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"


@app.callback(Output('p0-url3', 'href'),
              [Input('p1_output_mem', 'children')],)
def refresh_page2(b_memory):
    if b_memory == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"


@app.callback(Output('p0-url4', 'href'),
              [Input('p1_output_sto', 'children')], )
def refresh_page3(b_storage):
    if b_storage == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"


@app.callback(Output('p0-url5', 'href'),
              [Input('p1_output_lan', 'children')], )
def refresh_page4(b_lan):
    if b_lan == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"


@app.callback(Output('p0-url6', 'href'),
              [Input('p2_output-provider', 'children')], )
def refresh_page5(b_speccpu):
    if b_speccpu == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"


@app.callback(Output('p0-url7', 'href'),
              [Input('p2_output-provider_mlc', 'children')], )
def refresh_page6(b_mlc):
    if b_mlc == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"


@app.callback(Output('p0-url8', 'href'),
              [Input('p2_st_output-provider', 'children')], )
def refresh_page7(b_storage_perf):
    if b_storage_perf == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"


@app.callback(Output('p0-url9', 'href'),
              [Input('p2_output-provider_LAN', 'children')], )
def refresh_page8(b_lan_perf):
    if b_lan_perf == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"


@app.callback(Output('p0-url10', 'href'),
              [Input('p2_output-provider_cer', 'children')], )
def refresh_page9(b_cert):
    if b_cert == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"

@app.callback(Output('p0-url11', 'href'),
              [Input('p2_output-provider_rmt', 'children')], )
def refresh_page10(b_rmt):
    if b_rmt == "Upload Successfully":
        time.sleep(1)
        return "/apps/WebInput"

@app.callback(Output('p0-url12', 'href'),
              [Input('p1_create_user_sub_pro', 'children')], )
def refresh_page11(b_user):
    if b_user == "Upload Successfully":
        time.sleep(1)
        return "/apps/Login"

# project
@app.callback(Output('p1_output_pro', 'children'),
              [Input('p1_pro_sub', 'submit_n_clicks')],
              [State('p1_pro_table', 'data'), State('p1_pro_drop', 'value')])
def update_pro_output(submit_n_clicks, rows, value):
    global project_number, df_pro_item, pro_Name
    if not submit_n_clicks:
        return ''
    dbname_pro = "data/component_project.csv"
    currentdb_pro = pd.read_csv(dbname_pro)
    currentdb2_pro = pd.DataFrame(rows)
    index_value = currentdb_pro[currentdb_pro['Product Name'] == value].index.tolist()  # 透過test_id找dataframe的index
    currentdb_pro = currentdb_pro.drop(index_value)  # 透過index刪除重複的row
    if value is None:
        project_number = dt.now().strftime("%Y%m%d%H%M%S%f")
    df_pro1 = pd.DataFrame({"ID": ['MP' + str(project_number)], "Model Name": [currentdb2_pro.iloc[0, 1].upper()],
                            "Product Name": [currentdb2_pro.iloc[1, 1].upper()], "User": [currentdb2_pro.iloc[2, 1].title()]})
    df_pro2 = currentdb_pro.append(df_pro1, sort=False)
    df_pro3 = df_pro2.sort_values('ID')
    print(df_pro3)
    #tests = re.search('[^.a-zA-Z0-9_-]', currentdb2_pro.iloc[1, 2])

    if currentdb_pro.isin([currentdb2_pro.iloc[1, 1]]).values.any():
        return 'Upload Failed! Already has the same product'
    elif [currentdb2_pro.iloc[0, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_pro.iloc[0, 1]) is not None:
        return 'Upload Failed! - "Model Name" is empty or has special characters like @!#$%^'
    elif [currentdb2_pro.iloc[1, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_pro.iloc[1, 1]) is not None:
        return 'Upload Failed! - "Product Name" is empty or has special characters like @!#$%^'
    elif [currentdb2_pro.iloc[2, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_pro.iloc[2, 1]) is not None:
        return 'Upload Failed! - "User" is empty or has special characters like @!#$%^'
    elif df_pro3.isnull().values.any():
        return 'Upload Failed!'
    else:
        df_pro3.to_csv(dbname_pro, index=False, header=True, encoding='utf-8-sig')
        print('MP' + str(project_number))
        df_pro_item = pd.read_csv("data/Item_component_project.csv")
        df_pro = pd.read_csv("data/component_project.csv")
        print(df_pro)
        pro_Name = df_pro['Product Name']
        project_number = df_pro.shape[0] + 1
        project_empty_data = ['', '', '']
        df_pro_item['MP' + str(project_number)] = project_empty_data
        df_pro_item['Example'] = ['SKY-1111','SKY-111D','Admin']
        #dcc.Location(id='url', href='/apps/WebOutput'),
        return "Upload Successfully"


# cpu
@app.callback(Output('p1_output_cpu', 'children'),
              [Input('p1_cpu_sub', 'submit_n_clicks')],
              [State('p1_cpu_table', 'data'), State('p1_cpu_drop', 'value')])
def update_cpu_output(submit_n_clicks, rows, value):
    global cpu_number, df_cpu_item, cpu_Name
    if not submit_n_clicks:
        return ''
    dbname_cpu = "data/component_cpu.csv"
    currentdb_cpu = pd.read_csv(dbname_cpu,dtype=str)
    currentdb2_cpu = pd.DataFrame(rows)
    index_value_cpu = currentdb_cpu[
        currentdb_cpu['Processor Name'] == value].index.tolist()  # 透過test_id找dataframe的index
    currentdb_cpu = currentdb_cpu.drop(index_value_cpu)  # 透過index刪除重複的row
    if value is None:
        cpu_number = dt.now().strftime("%Y%m%d%H%M%S%f")
    print(currentdb2_cpu.iloc[1, 0].upper())
    print(type(currentdb2_cpu.iloc[1, 0]))
    #df_cpu_codename.loc[int(currentdb2_cpu.iloc[0, 1])].iat[1]
    df_cpu1 = pd.DataFrame({"ID": ['C' + str(cpu_number)], "Code Name": [currentdb2_cpu.iloc[0, 1]],
                            "Processor Name": [currentdb2_cpu.iloc[1, 1].upper()],
                            "# of cores": [currentdb2_cpu.iloc[2, 1]], "# of threads": [currentdb2_cpu.iloc[3, 1]],
                            "Processor Base Frequency(GHz)": [currentdb2_cpu.iloc[4,1]],
                            "Max Turbo Frequency(GHz)": [currentdb2_cpu.iloc[5, 1]],
                            "Cache(MB)": [currentdb2_cpu.iloc[6, 1]], "TDP(W)": [currentdb2_cpu.iloc[7, 1]],
                            "User": [currentdb2_cpu.iloc[8, 1].title()]})
    print(df_cpu1)
    df_cpu2 = currentdb_cpu.append(df_cpu1)
    df_cpu3 = df_cpu2.sort_values('ID')
    #print(df_cpu3)
    #print(currentdb2_cpu.iloc[2, 1])
    print('=====================')
    #print(currentdb2_cpu.iloc[2, -1])
    print('=====================')
    #print(currentdb2_cpu.iloc[2, 0])
    print(currentdb2_cpu.iloc[0, 1])


    if currentdb_cpu.isin([currentdb2_cpu.iloc[1, 1]]).values.any():
        return 'Upload Failed! Already has the same Processor Name'
    elif [currentdb2_cpu.iloc[0, 1]] == [''] or currentdb2_cpu.iloc[0, 1] not in df_cpu_codename_list:
        return 'Upload Failed! "Code" Name is empty or paste the correct code name'
    elif [currentdb2_cpu.iloc[1, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_cpu.iloc[1, 1]) is not None:
        return 'Upload Failed! "Processor Name" is empty or has special characters like @!#$%^'
    elif [str(currentdb2_cpu.iloc[2, 1])] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_cpu.iloc[2, 1])) is not None:
        return 'Upload Failed! "# of cores" is empty or has special characters like @!#$%^'
    elif [currentdb2_cpu.iloc[3, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_cpu.iloc[3, 1])) is not None:
        return 'Upload Failed! "# of threads" is empty or has special characters like @!#$%^'
    elif [currentdb2_cpu.iloc[4, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_cpu.iloc[4, 1])) is not None:
        print(currentdb2_cpu.iloc[4, 1])
        return 'Upload Failed! "Processor Base Frequency(GHz") is empty'
    elif [currentdb2_cpu.iloc[5, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_cpu.iloc[5, 1])) is not None:
        return 'Upload Failed! "Max Turbo Frequency(GHz)" is empty or has special characters like @!#$%^'
    elif [currentdb2_cpu.iloc[6, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_cpu.iloc[6, 1])) is not None:
        return 'Upload Failed! "Cache(MB)" is empty or has special characters like @!#$%^'
    elif [currentdb2_cpu.iloc[7, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_cpu.iloc[7, 1])) is not None:
        return 'Upload Failed! "TDP(W)" is empty or has special characters like @!#$%^'
    elif [currentdb2_cpu.iloc[8, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_cpu.iloc[8, 1]) is not None:
        return 'Upload Failed! "User" is empty or has special characters like @!#$%^'
    elif df_cpu3.isnull().values.any():
        return 'Upload Failed!'
    else:
        df_cpu3.to_csv(dbname_cpu, index=False, header=True, encoding='utf-8-sig')
        # del df_cpu_item['C'+str(cpu_number)]
        df_cpu_item = pd.read_csv("data/Item_component_cpu.csv")
        df_cpu = pd.read_csv("data/component_cpu.csv")
        print(df_cpu)
        cpu_Name = df_cpu['Processor Name']
        cpu_number = df_cpu.shape[0] + 1
        cpu_empty_data = ['', '', '', '', '', '', '', '', '']
        df_cpu_item['C' + str(cpu_number)] = cpu_empty_data
        df_cpu_item['Example'] = ['Cascade_Lake_SP', '8260Y', '48', '48', '2.4', '3.9', '35.75', '165', 'Admin']

        return "Upload Successfully"


# memory
@app.callback(Output('p1_output_mem', 'children'),
              [Input('p1_mem_sub', 'submit_n_clicks')],
              [State('p1_mem_table', 'data'), State('p1_mem_drop', 'value')])
def update_mem_output(submit_n_clicks, rows, value):
    global mem_number, df_mem_item, mem_IDs
    if not submit_n_clicks:
        return ''
    dbname_mem = "data/component_memory.csv"
    currentdb_mem = pd.read_csv(dbname_mem, dtype=str)
    currentdb2_mem = pd.DataFrame(rows)
    index_value_mem = currentdb_mem[currentdb_mem['Part Number'] == value].index.tolist()  # 透過test_id找dataframe的index
    currentdb_mem = currentdb_mem.drop(index_value_mem)  # 透過index刪除重複的row
    #df_memory_type.loc[int(currentdb2_mem.iloc[2, 1])].iat[1]
    if value is None:
        mem_number = dt.now().strftime("%Y%m%d%H%M%S%f") 
    df_mem = pd.DataFrame({"ID": ['M' + str(mem_number)], "DIMM Vendor": [currentdb2_mem.iloc[0, 1]],
                           "Part Number": [currentdb2_mem.iloc[1, 1].upper()],
                           "Memory Types": [currentdb2_mem.iloc[2, 1]], "# of Pin": [currentdb2_mem.iloc[3, 1]],
                           "ECC Support": [currentdb2_mem.iloc[4, 1]],
                           "Maximum Memory Speed": [currentdb2_mem.iloc[5, 1]],
                           "Memory Size(GB)": [currentdb2_mem.iloc[6, 1]], "# of Rank": [currentdb2_mem.iloc[7, 1]],
                           "RAM Chip": [currentdb2_mem.iloc[8, 1]], "User": [currentdb2_mem.iloc[9, 1].title()]})
    df_mem2 = currentdb_mem.append(df_mem, sort=False)
    df_mem3 = df_mem2.sort_values('ID')
    #print(currentdb2_mem.iloc[0, 2])
    print(currentdb_mem)
    print(currentdb2_mem.iloc[3, 1])

    if currentdb_mem.isin([currentdb2_mem.iloc[1, 1]]).values.any():
        return 'Upload Failed! Already has the same Part Number'
    elif [currentdb2_mem.iloc[0, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_mem.iloc[0, 1]) is not None:
        return 'Upload Failed! "DIMM Vendor" is empty or has special characters like @!#$%^'
    elif [currentdb2_mem.iloc[1, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_mem.iloc[1, 1]) is not None:
        return 'Upload Failed! "Part Number" is empty or has special characters like @!#$%^'
    elif [currentdb2_mem.iloc[2, 1]] == [''] or currentdb2_mem.iloc[2, 1] not in df_memory_type_list:
        return 'Upload Failed! "Memory Types" is empty or paste the right types'
    elif [currentdb2_mem.iloc[3, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_mem.iloc[3, 1])) is not None:
        return 'Upload Failed! "# of Pin" is empty or has special characters like @!#$%^'
    elif [currentdb2_mem.iloc[4, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_mem.iloc[4, 1])) is not None:
        return 'Upload Failed! "ECC Support" is empty or has special characters like @!#$%^'
    elif [currentdb2_mem.iloc[5, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_mem.iloc[5, 1])) is not None:
        return 'Upload Failed! "Maximum Memory Speed" is empty or has special characters like @!#$%^'
    elif [currentdb2_mem.iloc[6, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_mem.iloc[6, 1])) is not None:
        return 'Upload Failed! "Memory Size(GB)" is empty or has special characters like @!#$%^'
    elif [currentdb2_mem.iloc[7, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_mem.iloc[7, 1])) is not None:
        return 'Upload Failed! "# of Rank" is empty or has special characters like @!#$%^'
    elif [currentdb2_mem.iloc[8, 1]] == [''] or currentdb2_mem.iloc[8, 1] is None:
        return 'Upload Failed! "RAM Chip" is empty'
    elif [currentdb2_mem.iloc[9, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', str(currentdb2_mem.iloc[9, 1])) is not None:
        return 'Upload Failed! "User" is empty or has special characters like @!#$%^'
    elif df_mem3.isnull().values.any():
        return 'Upload Failed!'
    else:
        df_mem3.to_csv(dbname_mem, index=False, header=True, encoding='utf-8-sig')
        # del df_mem_item['M'+str(mem_number)]
        df_mem_item = pd.read_csv("data/Item_component_memory.csv")
        df_mem = pd.read_csv("data/component_memory.csv")
        mem_IDs = df_mem['Part Number']
        mem_number = df_mem.shape[0] + 1
        mem_empty_data = ['', '', '', '', '', '', '', '', '', '']
        df_mem_item['M' + str(mem_number)] = mem_empty_data
        df_mem_item['Example'] = ['Micron', 'MTA36ADS2G72PZ', 'DDR4_VLP_RDIMM', '288', 'Yes', '2133', '16', '2', '8Gb TwinDie', 'Admin']

        return "Upload Successfully"


# storage
@app.callback(Output('p1_output_sto', 'children'),
              [Input('p1_sto_sub', 'submit_n_clicks')],
              [State('p1_sto_table', 'data'), State('p1_sto_drop', 'value')])
def update_sto_output(submit_n_clicks, rows, value):
    global sto_number, df_sto_item, sto_IDs
    if not submit_n_clicks:
        return ''
    dbname_sto = "data/component_storage.csv"
    currentdb_sto = pd.read_csv(dbname_sto, dtype=str)
    currentdb2_sto = pd.DataFrame(rows)

    index_value_sto = currentdb_sto[
        currentdb_sto['Storage Model Name'] == value].index.tolist()  # 透過test_id找dataframe的index
    currentdb_sto = currentdb_sto.drop(index_value_sto)  # 透過index刪除重複的row
    #df_storage_category.loc[int(currentdb2_sto.iloc[0, 1])].iat[1]
    if value is None:
        sto_number = dt.now().strftime("%Y%m%d%H%M%S%f")
    df_sto = pd.DataFrame({"ID": ['S' + str(sto_number)], "Storage Device Category": [currentdb2_sto.iloc[0, 1]],
                           "Storage Vendor": [currentdb2_sto.iloc[1, 1]],
                           "Storage Model Name": [currentdb2_sto.iloc[2, 1].upper()],
                           "Form Factor": [currentdb2_sto.iloc[3, 1]], "Storage Interface": [currentdb2_sto.iloc[4, 1]],
                           "Storage Capacity": [currentdb2_sto.iloc[5, 1]],
                           "Media / Components": [currentdb2_sto.iloc[6, 1]],
                           "Power Consumption(W)": [currentdb2_sto.iloc[7, 1]], "User": [currentdb2_sto.iloc[8, 1].title()]})
    df_sto2 = currentdb_sto.append(df_sto, sort=False)
    df_sto3 = df_sto2.sort_values('ID')
    #print(currentdb2_sto.iloc[2, 2])
    print(currentdb_sto)#

    if currentdb_sto.isin([currentdb2_sto.iloc[2, 1]]).values.any():
        return 'Upload Failed! Already has the same Storage Model Name'
    elif [currentdb2_sto.iloc[0, 1]] == [''] or currentdb2_sto.iloc[0, 1] not in df_storage_category_list:
        return 'Upload Failed! "Storage Device Category" is empty or paste the correct storage_category'
    elif [currentdb2_sto.iloc[1, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_sto.iloc[1, 1]) is not None:
        return 'Upload Failed! "Storage Vendor" is empty or has special characters like @!#$%^'
    elif [currentdb2_sto.iloc[2, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_sto.iloc[2, 1]) is not None:
        return 'Upload Failed! "Storage Model Name" is empty or has special characters like @!#$%^'
    elif [currentdb2_sto.iloc[3, 1]] == [''] or currentdb2_sto.iloc[3, 1] is None:
        return 'Upload Failed! "Form Factor" is empty'
    elif [currentdb2_sto.iloc[4, 1]] == [''] or currentdb2_sto.iloc[4, 1] is None:
        return 'Upload Failed! "Storage Interface" is empty'
    elif [currentdb2_sto.iloc[5, 1]] == [''] or currentdb2_sto.iloc[5, 1] is None:
        return 'Upload Failed! "Storage Capacity" is empty'
    elif [currentdb2_sto.iloc[6, 1]] == [''] or currentdb2_sto.iloc[6, 1] is None:
        return 'Upload Failed! "Media / Components" is empty'
    elif [currentdb2_sto.iloc[7, 1]] == [''] or currentdb2_sto.iloc[7, 1] is None:
        return 'Upload Failed! "Power Consumption(W)" is empty'
    elif [currentdb2_sto.iloc[8, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_sto.iloc[8, 1]) is not None:
        return 'Upload Failed! "User" is empty or has special characters like @!#$%^ '
    elif df_sto3.isnull().values.any():
        return 'Upload Failed!'
    else:
        df_sto3.to_csv(dbname_sto, index=False, header=True, encoding='utf-8-sig')
        # del df_sto_item['S'+str(sto_number)]

        df_sto_item = pd.read_csv("data/Item_component_storage.csv")
        df_sto = pd.read_csv("data/component_storage.csv")
        sto_IDs = df_sto['Storage Model Name']
        sto_number = df_sto.shape[0] + 1
        sto_empty_data = ['', '', '', '', '', '', '', '', '']
        df_sto_item['S' + str(sto_number)] = sto_empty_data
        df_sto_item['Example'] = ['M.2_NVMe_SSD', 'Intel', 'SSD_DC_P4610', '2.5" 7mm', 'PCIe Gen3 x4', '1.6TB', '3D NAND, 64-layer, TLC', 'Up to 15 Watt', 'Admin']

        return "Upload Successfully"


# lan
@app.callback(Output('p1_output_lan', 'children'),
              [Input('p1_lan_sub', 'submit_n_clicks')],
              [State('p1_lan_table', 'data'), State('p1_lan_drop', 'value')])
def update_lan_output(submit_n_clicks, rows, value):
    global lan_number, lan_IDs, df_lan_item
    if not submit_n_clicks:
        return ''
    dbname_lan = "data/component_lan.csv"
    currentdb_lan = pd.read_csv(dbname_lan, dtype=str)
    currentdb2_lan = pd.DataFrame(rows)

    index_value_lan = currentdb_lan[currentdb_lan['ID'] == value].index.tolist()  # 透過test_id找dataframe的index
    currentdb_lan = currentdb_lan.drop(index_value_lan)  # 透過index刪除重複的row
    if value is None:
        lan_number = dt.now().strftime("%Y%m%d%H%M%S%f")
    df_lan = pd.DataFrame({"ID": ['L' + str(lan_number)], "Vendor": [currentdb2_lan.iloc[0, 1]],
                           "Card Name": [currentdb2_lan.iloc[1, 1].upper()],
                           "Controller": [currentdb2_lan.iloc[2, 1].upper()],
                           "Data Rate Per Port": [currentdb2_lan.iloc[3, 1]],
                           "System Interface Type": [currentdb2_lan.iloc[4, 1]], "User": [currentdb2_lan.iloc[5, 1].title()]})
    df_lan2 = currentdb_lan.append(df_lan, sort=False)
    df_lan3 = df_lan2.sort_values('ID')
    print(df_lan3)

    if currentdb_lan.isin([currentdb2_lan.iloc[1, 1]]).values.any():
        return 'Upload Failed! Already has the same Card Name'
    elif [currentdb2_lan.iloc[0, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_lan.iloc[0, 1]) is not None:
        return 'Upload Failed! "Vendor" is empty or has special characters like @!#$%^'
    elif [currentdb2_lan.iloc[1, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_lan.iloc[1, 1]) is not None:
        return 'Upload Failed! "Card Name" is empty or has special characters like @!#$%^'
    elif [currentdb2_lan.iloc[2, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_lan.iloc[2, 1]) is not None:
        return 'Upload Failed! "Controller" is empty or has special characters like @!#$%^'
    elif [currentdb2_lan.iloc[3, 1]] == [''] or currentdb2_lan.iloc[3, 1] is None:
        return 'Upload Failed! "Data Rate Per Port" is empty'
    elif [currentdb2_lan.iloc[4, 1]] == [''] or currentdb2_lan.iloc[4, 1] is None:
        return 'Upload Failed! "System Interface Type" is empty'
    elif [currentdb2_lan.iloc[5, 1]] == [''] or re.search('[^.a-zA-Z0-9_-]', currentdb2_lan.iloc[5, 1]) is not None:
        return 'Upload Failed! "User" is empty or has special characters like @!#$%^'
    elif df_lan3.isnull().values.any():
        return 'Upload Failed!'
    else:
        df_lan3.to_csv(dbname_lan, index=False, header=True, encoding='utf-8-sig')
        df_lan_item = pd.read_csv("data/Item_component_lan.csv")
        df_lan = pd.read_csv("data/component_lan.csv")
        lan_IDs = df_lan['Card Name']
        lan_number = df_lan.shape[0] + 1
        lan_empty_data = ['', '', '', '', '', '']
        df_lan_item['L' + str(lan_number)] = lan_empty_data
        df_lan_item['Example'] = ['Intel', 'X710-T4L', 'X710-TM4', '10Gb/5Gb/2.5Gb/1Gb/100Mb', '8.0GT/s, x8 lanes', 'Admin']

        return "Upload Successfully"


# ------------- callback data from csv --------------
# project
@app.callback([Output('p1_pro_table', 'columns'), Output('p1_pro_table', 'data')],
              [Input('p1_pro_drop', 'value')])
def update_pro_value(value):
    global project_number
    if value is None:
        df_pro = pd.read_csv("data/component_project.csv")
        # create table data
        project_number = df_pro.shape[0] + 1
        return [{"name": 'ID', "id": 'ID'}, {"name": 'MP' + str(project_number), "id": 'MP' + str(project_number)}], [
            {'ID': 'Model Name', 'MP' + str(project_number): ''},
            {'ID': 'Product Name', 'MP' + str(project_number): ''}, {'ID': 'User', 'MP' + str(project_number): ''}]
    dictOfvalue_list = []
    dbname_pro2 = "data/component_project.csv"
    currentdb2 = pd.read_csv(dbname_pro2)
    df_value = currentdb2[currentdb2['Product Name'] == value]
    pro_str = df_value.iloc[0, 0]
    pro_num = pro_str.replace('MP', '')
    project_number = int(pro_num)
    print(project_number)
    value_list = df_value.iloc[0].tolist()

    print(value_list)
    list1 = ['Model Name', value_list[1]]
    list2 = ['Product Name', value_list[2]]
    list3 = ['User', value_list[3]]
    print(list1)

    # Datatable的data為list(dist)，先將資料轉成dict再存到list中
    listOfStr = ["ID", value_list[0]]
    zipbObj1 = zip(listOfStr, list1)
    dictOfvalue1 = dict(zipbObj1)  # 轉dict
    # print(dictOfvalue)
    zipbObj2 = zip(listOfStr, list2)
    dictOfvalue2 = dict(zipbObj2)
    zipbObj3 = zip(listOfStr, list3)
    dictOfvalue3 = dict(zipbObj3)
    dictOfvalue_list.append(dictOfvalue1)
    dictOfvalue_list.append(dictOfvalue2)
    dictOfvalue_list.append(dictOfvalue3)

    return [{"name": 'ID', "id": 'ID'}, {"name": value_list[0], "id": value_list[0]}], dictOfvalue_list


# cpu
@app.callback([Output('p1_cpu_table', 'columns'), Output('p1_cpu_table', 'data')],
              [Input('p1_cpu_drop', 'value')])
def update_cpu_value(value):
    global cpu_number
    if value is None:
        df_cpu = pd.read_csv("data/component_cpu.csv")
        # create table data
        cpu_number = df_cpu.shape[0] + 1
        return [{"name": 'ID', "id": 'ID'}, {"name": 'C' + str(cpu_number), "id": 'C' + str(cpu_number)}], [
            {'ID': 'Code Name', 'C' + str(cpu_number): ''}, {'ID': 'Processor Name', 'C' + str(cpu_number): ''},
            {'ID': '# of cores', 'C' + str(cpu_number): ''}, {'ID': '# of threads', 'C' + str(cpu_number): ''},
            {'ID': 'Processor Base Frequency(GHz)', 'C' + str(cpu_number): ''},
            {'ID': 'Max Turbo Frequency(GHz)', 'C' + str(cpu_number): ''},
            {'ID': 'Cache(MB)', 'C' + str(cpu_number): ''}, {'ID': 'TDP(W)', 'C' + str(cpu_number): ''},
            {'ID': 'User', 'C' + str(cpu_number): ''}]
    dictOfvalue_list = []
    dbname_cpu2 = "data/component_cpu.csv"
    currentdb2 = pd.read_csv(dbname_cpu2)
    df_value = currentdb2[currentdb2['Processor Name'] == value]
    cpu_str = df_value.iloc[0, 0]
    cpu_num = cpu_str.replace('C', '')
    cpu_number = int(cpu_num)
    print(cpu_number)

    value_list_cpu = df_value.iloc[0].tolist()

    print(value_list_cpu)
    list1 = ['Code Name', value_list_cpu[1]]
    list2 = ['Processor Name', value_list_cpu[2]]
    list3 = ['# of cores', value_list_cpu[3]]
    list4 = ['# of threads', value_list_cpu[4]]
    list5 = ['Processor Base Frequency(GHz)', value_list_cpu[5]]
    list6 = ['Max Turbo Frequency(GHz)', value_list_cpu[6]]
    list7 = ['Cache(MB)', value_list_cpu[7]]
    list8 = ['TDP(W)', value_list_cpu[8]]
    list9 = ['User', value_list_cpu[9]]
    print(list1)

    # Datatable的data為list(dist)，先將資料轉成dict再存到list中
    listOfStr = ["ID", value_list_cpu[0]]

    zipbObj1 = zip(listOfStr, list1)
    dictOfvalue1 = dict(zipbObj1)  # 轉dict
    zipbObj2 = zip(listOfStr, list2)
    dictOfvalue2 = dict(zipbObj2)
    zipbObj3 = zip(listOfStr, list3)
    dictOfvalue3 = dict(zipbObj3)
    zipbObj4 = zip(listOfStr, list4)
    dictOfvalue4 = dict(zipbObj4)
    zipbObj5 = zip(listOfStr, list5)
    dictOfvalue5 = dict(zipbObj5)
    zipbObj6 = zip(listOfStr, list6)
    dictOfvalue6 = dict(zipbObj6)
    zipbObj7 = zip(listOfStr, list7)
    dictOfvalue7 = dict(zipbObj7)
    zipbObj8 = zip(listOfStr, list8)
    dictOfvalue8 = dict(zipbObj8)
    zipbObj9 = zip(listOfStr, list9)
    dictOfvalue9 = dict(zipbObj9)

    dictOfvalue_list.append(dictOfvalue1)
    dictOfvalue_list.append(dictOfvalue2)
    dictOfvalue_list.append(dictOfvalue3)
    dictOfvalue_list.append(dictOfvalue4)
    dictOfvalue_list.append(dictOfvalue5)
    dictOfvalue_list.append(dictOfvalue6)
    dictOfvalue_list.append(dictOfvalue7)
    dictOfvalue_list.append(dictOfvalue8)
    dictOfvalue_list.append(dictOfvalue9)
    print(dictOfvalue_list)

    return [{"name": 'ID', "id": 'ID'}, {"name": value_list_cpu[0], "id": value_list_cpu[0]}], dictOfvalue_list


# memory
@app.callback([Output('p1_mem_table', 'columns'), Output('p1_mem_table', 'data')],
              [Input('p1_mem_drop', 'value')])
def update_mem_value(value):
    global mem_number
    if value is None:
        df_mem = pd.read_csv("data/component_memory.csv")
        # create table data
        mem_number = df_mem.shape[0] + 1
        return [{"name": 'ID', "id": 'ID'}, {"name": 'M' + str(mem_number), "id": 'M' + str(mem_number)}], [
            {'ID': 'DIMM Vendor', 'M' + str(mem_number): ''}, {'ID': 'Part Number', 'M' + str(mem_number): ''},
            {'ID': 'Memory Types', 'M' + str(mem_number): ''}, {'ID': '# of Pin', 'M' + str(mem_number): ''},
            {'ID': 'ECC Support', 'M' + str(mem_number): ''}, {'ID': 'Maximum Memory Speed', 'M' + str(mem_number): ''},
            {'ID': 'Memory Size(GB)', 'M' + str(mem_number): ''}, {'ID': '# of Rank', 'M' + str(mem_number): ''},
            {'ID': 'RAM Chip', 'M' + str(mem_number): ''}, {'ID': 'User', 'M' + str(mem_number): ''}]
    dictOfvalue_list = []
    dbname_mem2 = "data/component_memory.csv"
    currentdb2 = pd.read_csv(dbname_mem2)
    df_value = currentdb2[currentdb2['Part Number'] == value]

    mem_str = df_value.iloc[0, 0]
    mem_num = mem_str.replace('M', '')
    mem_number = int(mem_num)
    print(mem_number)

    value_list_mem = df_value.iloc[0].tolist()

    print(value_list_mem)
    list1 = ['DIMM Vendor', value_list_mem[1]]
    list2 = ['Part Number', value_list_mem[2]]
    list3 = ['Memory Types', value_list_mem[3]]
    list4 = ['# of Pin', value_list_mem[4]]
    list5 = ['ECC Support', value_list_mem[5]]
    list6 = ['Maximum Memory Speed', value_list_mem[6]]
    list7 = ['Memory Size(GB)', value_list_mem[7]]
    list8 = ['# of Rank', value_list_mem[8]]
    list9 = ['RAM Chip', value_list_mem[9]]
    list10 = ['User', value_list_mem[10]]
    print(list1)

    # Datatable的data為list(dist)，先將資料轉成dict再存到list中
    listOfStr = ["ID", value_list_mem[0]]

    zipbObj1 = zip(listOfStr, list1)
    dictOfvalue1 = dict(zipbObj1)  # 轉dict
    zipbObj2 = zip(listOfStr, list2)
    dictOfvalue2 = dict(zipbObj2)
    zipbObj3 = zip(listOfStr, list3)
    dictOfvalue3 = dict(zipbObj3)
    zipbObj4 = zip(listOfStr, list4)
    dictOfvalue4 = dict(zipbObj4)
    zipbObj5 = zip(listOfStr, list5)
    dictOfvalue5 = dict(zipbObj5)
    zipbObj6 = zip(listOfStr, list6)
    dictOfvalue6 = dict(zipbObj6)
    zipbObj7 = zip(listOfStr, list7)
    dictOfvalue7 = dict(zipbObj7)
    zipbObj8 = zip(listOfStr, list8)
    dictOfvalue8 = dict(zipbObj8)
    zipbObj9 = zip(listOfStr, list9)
    dictOfvalue9 = dict(zipbObj9)
    zipbObj10 = zip(listOfStr, list10)
    dictOfvalue10 = dict(zipbObj10)

    dictOfvalue_list.append(dictOfvalue1)
    dictOfvalue_list.append(dictOfvalue2)
    dictOfvalue_list.append(dictOfvalue3)
    dictOfvalue_list.append(dictOfvalue4)
    dictOfvalue_list.append(dictOfvalue5)
    dictOfvalue_list.append(dictOfvalue6)
    dictOfvalue_list.append(dictOfvalue7)
    dictOfvalue_list.append(dictOfvalue8)
    dictOfvalue_list.append(dictOfvalue9)
    dictOfvalue_list.append(dictOfvalue10)

    return [{"name": 'ID', "id": 'ID'}, {"name": value_list_mem[0], "id": value_list_mem[0]}], dictOfvalue_list


# storage
@app.callback([Output('p1_sto_table', 'columns'), Output('p1_sto_table', 'data')],
              [Input('p1_sto_drop', 'value')])
def update_sto_value(value):
    global sto_number
    if value is None:
        df_sto = pd.read_csv("data/component_storage.csv")
        # create table data
        sto_number = df_sto.shape[0] + 1
        return [{"name": 'ID', "id": 'ID'}, {"name": 'S' + str(sto_number), "id": 'S' + str(sto_number)}], [
            {'ID': 'Storage Device Category', 'S' + str(sto_number): ''},
            {'ID': 'Storage Vendor', 'S' + str(sto_number): ''},
            {'ID': 'Storage Model Name', 'S' + str(sto_number): ''}, {'ID': 'Form Factor', 'S' + str(sto_number): ''},
            {'ID': 'Storage Interface', 'S' + str(sto_number): ''},
            {'ID': 'Storage Capacity', 'S' + str(sto_number): ''},
            {'ID': 'Media / Components', 'S' + str(sto_number): ''},
            {'ID': 'Power Consumption(W)', 'S' + str(sto_number): ''}, {'ID': 'User', 'S' + str(sto_number): ''}]
    print(value)
    dictOfvalue_list = []
    dbname_sto2 = "data/component_storage.csv"
    currentdb2 = pd.read_csv(dbname_sto2)
    df_value = currentdb2[currentdb2['Storage Model Name'] == value]
    sto_str = df_value.iloc[0, 0]
    sto_num = sto_str.replace('S', '')
    sto_number = int(sto_num)
    print(sto_number)

    value_list_sto = df_value.iloc[0].tolist()

    print(value_list_sto)
    list1 = ['Storage Device Category', value_list_sto[1]]
    list2 = ['Storage Vendor', value_list_sto[2]]
    list3 = ['Storage Model Name', value_list_sto[3]]
    list4 = ['Form Factor', value_list_sto[4]]
    list5 = ['Storage Interface', value_list_sto[5]]
    list6 = ['Storage Capacity', value_list_sto[6]]
    list7 = ['Media / Components', value_list_sto[7]]
    list8 = ['Power Consumption(W)', value_list_sto[8]]
    list9 = ['User', value_list_sto[9]]
    print(list1)

    # Datatable的data為list(dist)，先將資料轉成dict再存到list中
    listOfStr = ["ID", value_list_sto[0]]
    zipbObj1 = zip(listOfStr, list1)
    dictOfvalue1 = dict(zipbObj1)  # 轉dict
    zipbObj2 = zip(listOfStr, list2)
    dictOfvalue2 = dict(zipbObj2)
    zipbObj3 = zip(listOfStr, list3)
    dictOfvalue3 = dict(zipbObj3)
    zipbObj4 = zip(listOfStr, list4)
    dictOfvalue4 = dict(zipbObj4)
    zipbObj5 = zip(listOfStr, list5)
    dictOfvalue5 = dict(zipbObj5)
    zipbObj6 = zip(listOfStr, list6)
    dictOfvalue6 = dict(zipbObj6)
    zipbObj7 = zip(listOfStr, list7)
    dictOfvalue7 = dict(zipbObj7)
    zipbObj8 = zip(listOfStr, list8)
    dictOfvalue8 = dict(zipbObj8)
    zipbObj9 = zip(listOfStr, list9)
    dictOfvalue9 = dict(zipbObj9)
    dictOfvalue_list.append(dictOfvalue1)
    dictOfvalue_list.append(dictOfvalue2)
    dictOfvalue_list.append(dictOfvalue3)
    dictOfvalue_list.append(dictOfvalue4)
    dictOfvalue_list.append(dictOfvalue5)
    dictOfvalue_list.append(dictOfvalue6)
    dictOfvalue_list.append(dictOfvalue7)
    dictOfvalue_list.append(dictOfvalue8)
    dictOfvalue_list.append(dictOfvalue9)

    return [{"name": 'ID', "id": 'ID'}, {"name": value_list_sto[0], "id": value_list_sto[0]}], dictOfvalue_list


# lan
@app.callback([Output('p1_lan_table', 'columns'), Output('p1_lan_table', 'data')],
              [Input('p1_lan_drop', 'value')])
def update_lan_value(value):
    global lan_number
    if value is None:
        df_lan = pd.read_csv("data/component_lan.csv")
        # create table data
        lan_number = df_lan.shape[0] + 1
        return [{"name": 'ID', "id": 'ID'}, {"name": 'L' + str(lan_number), "id": 'L' + str(lan_number)}], [
            {'ID': 'Vendor', 'L' + str(lan_number): ''}, {'ID': 'Card Name(Onboard)', 'L' + str(lan_number): ''},
            {'ID': 'Controller', 'L' + str(lan_number): ''}, {'ID': 'Data Rate Per Port', 'L' + str(lan_number): ''},
            {'ID': 'System Interface Type', 'L' + str(lan_number): ''}, {'ID': 'User', 'L' + str(lan_number): ''}]
    print(value)
    dictOfvalue_list = []
    dbname_lan2 = "data/component_lan.csv"
    currentdb2 = pd.read_csv(dbname_lan2)
    df_value = currentdb2[currentdb2['ID'] == value]

    lan_str = df_value.iloc[0, 0]
    lan_num = lan_str.replace('L', '')
    lan_number = int(lan_num)
    print(lan_number)

    value_list_lan = df_value.iloc[0].tolist()

    print(value_list_lan)
    list1 = ['Vendor', value_list_lan[1]]
    list2 = ['Card Name(Onboard)', value_list_lan[2]]
    list3 = ['Controller', value_list_lan[3]]
    list4 = ['Data Rate Per Port', value_list_lan[4]]
    list5 = ['System Interface Type', value_list_lan[5]]
    list6 = ['User', value_list_lan[6]]
    print(list1)

    # Datatable的data為list(dist)，先將資料轉成dict再存到list中
    listOfStr = ["ID", value_list_lan[0]]
    zipbObj1 = zip(listOfStr, list1)
    dictOfvalue1 = dict(zipbObj1)  # 轉dict
    zipbObj2 = zip(listOfStr, list2)
    dictOfvalue2 = dict(zipbObj2)
    zipbObj3 = zip(listOfStr, list3)
    dictOfvalue3 = dict(zipbObj3)
    zipbObj4 = zip(listOfStr, list4)
    dictOfvalue4 = dict(zipbObj4)
    zipbObj5 = zip(listOfStr, list5)
    dictOfvalue5 = dict(zipbObj5)
    zipbObj6 = zip(listOfStr, list6)
    dictOfvalue6 = dict(zipbObj6)
    dictOfvalue_list.append(dictOfvalue1)
    dictOfvalue_list.append(dictOfvalue2)
    dictOfvalue_list.append(dictOfvalue3)
    dictOfvalue_list.append(dictOfvalue4)
    dictOfvalue_list.append(dictOfvalue5)
    dictOfvalue_list.append(dictOfvalue6)

    return [{"name": 'ID', "id": 'ID'}, {"name": value_list_lan[0], "id": value_list_lan[0]}], dictOfvalue_list


# ------------- LAN callback Card name dropdown --------------

@app.callback(
    [Output('p1_lan_drop', 'options')],
    [Input('radio', 'value')])
def update_lan_dropdown(lan_type):
    print(lan_type)
    lan_com = pd.read_csv("data/component_lan.csv")
    df_lan = pd.read_csv("data/component_lan.csv")
    #lan_IDs = df_lan['Card Name']
    lan_number = df_lan.shape[0] + 1
    lan_empty_data = ['', '', '', '', '', '']
    df_lan_item['L' + str(lan_number)] = lan_empty_data
    df_lan_item['Example'] = ['Intel', 'X710-T4L', 'X710-TM4', '10Gb/5Gb/2.5Gb/1Gb/100Mb', '8.0GT/s, x8 lanes', 'Admin']

    if lan_type == 'ONBOARD':
        # card_name == 'Onboard':
        ctrl_name = lan_com[(lan_com['Card Name'] == 'ONBOARD')]['Controller']
        ctrl_ID = lan_com[(lan_com['Card Name'] == 'ONBOARD')]['ID']
        a = [[{'label': i, 'value': j} for i, j in zip(ctrl_name, ctrl_ID)]]
        print(a)
        return [[{'label': i, 'value': j} for i, j in zip(ctrl_name, ctrl_ID)]]
    else:
        df_lan_com = lan_com[lan_com['Card Name'] != 'ONBOARD']['Card Name']
        ctrl_ID = lan_com[(lan_com['Card Name'] != 'ONBOARD')]['ID']
        b = [[{'label': i, 'value': j} for i, j in zip(df_lan_com, ctrl_ID)]]
        print(b)
        return [[{'label': i, 'value': j} for i, j in zip(df_lan_com, ctrl_ID)]]

#=====Create User===================
@app.callback(Output('p1_create_user_sub_pro', 'children'),
              [Input('p1_create_user_sub', 'submit_n_clicks')],
              [State('user', 'value'), State('password', 'value'), State('mail', 'value')])
def update_pro_output1(submit_n_clicks, us, pd, ml):
    if not submit_n_clicks:
        return ''
    um.add_user(us, pd, ml)
    return "Upload Successfully"



@app.callback([Output("p2_page-content", "children"), Output('p2_user', 'value')], [Input("p2_item", "value")])
def change_url(value):
    if value is None:
        return "", current_user.username
    elif value == "SPECCPU2017":
        return SPECCPU2017.create_layout(app), current_user.username
    elif value == 'MLC':
        return MLC.create_layout(app), current_user.username
    elif value == "LAN Performance":
        return LAN.create_layout(app), current_user.username
    elif value == "Certification":
        return Certification.create_layout(app), current_user.username
    elif value == "RMT":
        return RMT.create_layout(app), current_user.username
    else:
        return Storage.create_layout(app), current_user.username


@app.callback(
    [Output('user-name', 'children'), Output('p2_user', 'options'), Output('create', 'hidden')],
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        if current_user.username == 'dqa':
            return html.Div('Welcome ! ' + current_user.username), [{'label': current_user.username, 'value': current_user.username}], False
        else :
            return html.Div('Welcome ! ' + current_user.username), [{'label': current_user.username, 'value': current_user.username}], True
        # 'User authenticated' return username in get_id()
    else:
        return '', '', True


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        #logout_user()
        return html.A('Logout', href='/apps/Login')
    else:
        return ''
    

if __name__ == '__main__':
    app.run_server(debug=True)

