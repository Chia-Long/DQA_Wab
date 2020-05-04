from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import dash_table as dst
import requests

dfs = pd.read_csv("data/component_storage.csv")
form_factor = dfs['Form Factor']
storage_id = dfs['ID']
storage_model = dfs['Storage Model Name']
storage_speed = dfs['Storage Interface']

df = pd.read_csv("data/component_project.csv")
dfc = pd.read_csv("data/component_cpu.csv")
dfm = pd.read_csv("data/component_memory.csv")
df_user = pd.read_csv("data/user.csv")
df1 = pd.read_csv('data/Test_Item_model_CPU.csv')
df2 = pd.read_csv("data/Test_Item_model_Memory.csv")
df3 = pd.read_csv("data/Test_Item_model_Storage.csv")
df4 = pd.read_csv("data/Test_Item_model_LAN.csv")
df5 = pd.read_csv("data/Test_Item_model_Certification.csv")

models = df['Model Name']
models_id = df['ID']
projects = df['Product Name']
projects_id = df['ID']
cpus = dfc['Processor Name']
cpus_id = dfc['ID']
mems = dfm['Part Number']
mems_id = dfm['ID']
user = df_user['User']

drop_style = {
    'width': '20%', 
    'height': '100%',
    'display': 'inline-block'
}

input_style = {
    'width': '25%', 
    'height': '100%',
    'display': 'inline-block'
}
ID_value_list=[]

def create_layout(app):
    return html.Div([
        dcc.Interval(
            id='interval-cpu',
            interval=5000,
            n_intervals=0
        ),
        html.H2('SPECCPU2017 System Info.'),
        html.Label('Test ID'),
        html.Div([
            
            #dcc.Input(id='p2_DataID_cpu', value=dt.now().strftime("%Y%m%d%H%M%S"), type='number', style={'width': '12%', 'display': 'inline-block'}),  
            dcc.Dropdown(
                id='p2_DataID_cpu',
                options=[{'label': i , 'value': i} for i in ID_value_list],
                #[{'label': dt.now().strftime("%Y%m%d%H%M%S"), 'value': dt.now().strftime("%Y%m%d%H%M%S")},],
                #value = dt.now().strftime("%Y%m%d%H%M%S"),
                style={'display':'inline-block', 'width':'250px', 'vertical-align': 'middle'},
                clearable = False
            ),
            html.Button('Search', id='search_button', style={'display': 'inline-block', 'vertical-align': 'middle'}),
        ]),
        html.Label('Test Date'),
        html.Div([
            dcc.DatePickerSingle(
                id='p2_cpu_date',
                min_date_allowed=dt(2000, 1, 1),
                max_date_allowed=dt(2099, 12, 31),
                initial_visible_month=dt.today(),
                style={'width': '60%'}
            ),           
        ]),
        html.Hr(),

        html.Div([
            html.Label('Product Name'),
            dcc.Dropdown(
                id='p2_cpu_product'
            )
        ], style=drop_style),
        html.Hr(),
        html.Div([
            html.Label('CPU'),
            dcc.Dropdown(
                id='p2_cpu_cpu'
            )
        ], style=drop_style),

        html.Div([
            html.Label('CPU數量'),
            dcc.Dropdown(
                id='p2_cpu_cpu_c',
                options=[
                    {'label': 1 , 'value': 1},
                    {'label': 2 , 'value': 2},
                    {'label': 4 , 'value': 4},
                ],
            )
        ], style=drop_style),

        html.Div([
            html.Label('Topology'),
            dcc.Dropdown(
                id='p2_cpu_cpu_ty',
                options=[
                    {'label': "NA", 'value': 'NA'},
                    {'label': "Ring", 'value': 'Ring'},
                    {'label': "Cross", 'value': 'Cross'},
                ]
            )
        ], style=drop_style),
        html.Hr(),

        html.Div([
            html.Label('Memory'),
            dcc.Dropdown(
                id='p2_cpu_mem',
            )
        ], style=drop_style),

        html.Div([
            html.Label('Link Speed MT/s'),
            dcc.Dropdown(
                id='p2_cpu_mem_sp',
                options=[
                    {'label': "2133", 'value': '2133'},
                    {'label': "2400", 'value': '2400'},
                    {'label': "2666", 'value': '2666'},
                    {'label': "2933", 'value': '2933'}
                ],
            )
        ], style=drop_style),

        html.Div([
            html.Label('Memory Location'),
            dcc.Checklist(
                id='p2_cpu_mem_l',
                options=[
                    {'label': 'A1', 'value': 'A1'},
                    {'label': 'B1', 'value': 'B1'},
                    {'label': 'C1', 'value': 'C1'},
                    {'label': 'D1', 'value': 'D1'},
                    {'label': 'E1', 'value': 'E1'},
                    {'label': 'F1', 'value': 'F1'},
                    {'label': 'G1', 'value': 'G1'},
                    {'label': 'H1', 'value': 'H1'},
                    {'label': 'A2', 'value': 'A2'},
                    {'label': 'B2', 'value': 'B2'},
                    {'label': 'C2', 'value': 'C2'},
                    {'label': 'D2', 'value': 'D2'},
                    {'label': 'E2', 'value': 'E2'},
                    {'label': 'F2', 'value': 'F2'},
                    {'label': 'G2', 'value': 'G2'},
                    {'label': 'H2', 'value': 'H2'},
                    {'label': 'A3', 'value': 'A3'},
                    {'label': 'B3', 'value': 'B3'},
                    {'label': 'C3', 'value': 'C3'},
                    {'label': 'D3', 'value': 'D3'},
                    {'label': 'E3', 'value': 'E3'},
                    {'label': 'F3', 'value': 'F3'},
                    {'label': 'G3', 'value': 'G3'},
                    {'label': 'H3', 'value': 'H3'},
                ], 
                labelStyle={'display': 'inline-block','cursor': 'pointer'},
                value=['A1']
            ),
    ], style={'width': '23%', 'height': '10%'}),
    html.Hr(),
    html.Div([
        html.Label('Form Factor'),
        dcc.Dropdown(
            id='p2_cpu_ff',
        ),
    ], style=drop_style),

    html.Div([
        html.Label('Storage 型號'),
        dcc.Dropdown(
            id='p2_cpu_sm'
        ),
    ], style=drop_style),

    html.Div([
        html.Label('Storage數量'),
        dcc.Dropdown(
            id='p2_cpu_sn',
            options=[
                {'label': '1', 'value': '1'},
                {'label': '2', 'value': '2'},
                {'label': '4', 'value': '4'}
            ],
        ),
    ],style=drop_style),

    html.Div([
        html.Label('I/O Type Bus Speed'),
        dcc.Dropdown(
            id='p2_cpu_ss'
        ),
    ], style=drop_style),
    html.Hr(),

    html.Div([
        html.Label('File System'),
        dcc.Input(
            id='p2_cpu_fs',
            type='text',
            value='',
        )
    ], style=input_style),

    html.Div([
        html.Label('Base Pointers'),
        dcc.Input(
            id='p2_cpu_bp',
            type='text',
            value='',
        )
    ], style=input_style),

    html.Div([
        html.Label('Peak Pointers'),
        dcc.Input(
            id='p2_cpu_pp',
            type='text',
            value='',
        )
    ], style=input_style),

    html.Div([
        html.Label('OS'),
        dcc.Input(
            id='p2_cpu_os',
            type='text',
            value='',
        )
    ], style=input_style),

    html.Div([
        html.Label('Compiler C/C++ Version'),
        dcc.Input(
            id='p2_cpu_ccv',
            type='text',
            value='',
        )
    ], style=input_style),

    html.Div([
        html.Label('Compiler Fortran Version'),
        dcc.Input(
            id='p2_cpu_cfv',
            type='text',
            value='',
        )
    ], style=input_style),

    html.Div([
        html.Label('jemalloc memory allocator'),
        dcc.Input(
            id='p2_cpu_jma',
            type='text',
            value='',
        )
    ], style=input_style),
    html.Br(),

    html.Div([
        html.Label('Comment'),
        dcc.Input(
            id='p2_cpu_comment',
            placeholder='Enter a value...',
            type='text',
            value='N/A',
        )
    ], style=input_style),
    html.Hr(),
    html.H2('SPECCPU2017 Test Data'),
    html.Div([
        html.Div(generate_table(df1)),
    ]),

    html.Div([
        dcc.ConfirmDialogProvider(
            children=html.Button(
                'Submit',
            ),
            id='p2_provider',
            message='Do you want to update the information?',
        ),
    ]),
    html.Div(id='p2_output-provider'),
    html.Br(),
])



#------------- Generate table --------------

def generate_table(dataframe):
    return dst.DataTable(
            id='p2_editing_table_cpu',
            columns=[
              {'name': c, 'id': c, 'editable': (c != 'Test Item'), 'type': 'numeric'} for c in dataframe.columns
            ],

            data=dataframe.to_dict('rows'),
            editable=True,
            style_header={
                'backgroundColor': '#3D9970',
                'fontWeight': 'bold',
                'textAlign': 'left',
                'color': 'white'
            },
            style_cell={'textAlign': 'left'},

            style_data_conditional=[
              {
                'if': {
                      'column_id': 'Test Item',
                 },
                      'backgroundColor': '#3D9970',
                      'fontWeight': 'bold',
                      'textAlign': 'left',
                      'color': 'white',
              },
           ]
        )

#------------- callback test item model Table --------------

#------------- callback test item model Table --------------

@app.callback([Output('p2_DataID_cpu','options'), Output('p2_DataID_cpu','value')],
              [Input('p2_user', 'value')]
              )
def update_id(name):
    value=dt.now().strftime("%Y%m%d%H%M%S")
    if name is None:
        return [{'label': value , 'value': value}], value    
    else:
        df_ID = pd.read_csv("data/SPECCPU2017.csv")
        ID_value = df_ID[df_ID['User'] == name]
        ID_value_list = ID_value['Test_ID'].tolist()
        ID_value_list.append(value)
        projects_list = ID_value['Product_Name'].tolist()
        df_pj = pd.read_csv("data/component_project.csv",  index_col ='ID')
        pj_list = []
        #dropdwon name
        for a in projects_list:
            pj_list.append(df_pj.loc[a,'Product Name'])
            
        pj_list.append('')
        drop_list = []
        for i, j in zip(pj_list, ID_value_list):
            drop_list.append({'label': str(j)+"   "+str(i), 'value': j})
        return drop_list, value







#------------- Write all test config and data to csv --------------

@app.callback(Output('p2_output-provider', 'children'),
                  [Input('p2_provider', 'submit_n_clicks'), Input('p2_editing_table_cpu', 'data')],
              [State('p2_DataID_cpu', 'value'), State('p2_cpu_product', 'value'), State('p2_cpu_date', 'date'),
               State('p2_cpu_cpu', 'value'), State('p2_cpu_cpu_c', 'value'), State('p2_cpu_cpu_ty', 'value'), State('p2_cpu_mem', 'value'), 
               State('p2_cpu_mem_sp', 'value'), State('p2_cpu_mem_l', 'value'),State('p2_cpu_ff', 'value'), State('p2_cpu_sm', 'value'), 
               State('p2_cpu_sn', 'value'), State('p2_cpu_ss', 'value'), State('p2_cpu_fs', 'value'), State('p2_cpu_bp', 'value'), 
               State('p2_cpu_pp', 'value'), State('p2_cpu_os', 'value'), State('p2_cpu_ccv', 'value'), State('p2_cpu_cfv', 'value'), 
               State('p2_cpu_jma', 'value'), State('p2_cpu_comment', 'value'), State('p2_user', 'value')])
def update_output(submit_n_clicks,rows,data_id,prov,timev,cpuv,cpucv,cputyv,memv,memspv,memlv,cpuffv,cpusmv,cpusnv,cpussv,cpufsv,cpubpv,cpuppv,cpuosv,cpuccvv,cpucfvv,cpujmav,cpucmv,user):
        if not submit_n_clicks:
            return ''
        else:
            dbname = "data/SPECCPU2017.csv"
            currentdb = pd.read_csv(dbname, keep_default_na=False,dtype=str)
            index_value = currentdb[currentdb['Test_ID'] == str(data_id)].index.tolist()#透過test_id找dataframe的index
            newdb = currentdb.drop(index_value)#透過index刪除重複的row
            newpd = newdb.append({'Test_ID': data_id, 'Model_Name': prov, 'Product_Name': prov, 'Test_Date': timev, 'CPU': cpuv, 'CPU_#':cpucv,
                                  'Topology': cputyv, 'Memory': memv, 'Link_Speed': memspv, 'Memory_Location': memlv, 'Form_Factor':cpuffv,
                                  'Storage_Model': cpusmv, 'Storage_Number': cpusnv, 'I/O_Type_Bus_Speed': cpussv, 'File_System': cpufsv,
                                  'Base_Pointers':cpubpv, 'Peak_Pointers': cpuppv, 'OS': cpuosv, 'Compiler_C/C++_Version': cpuccvv,
                                  'Compiler_Fortran_Version': cpucfvv, 'jemalloc_memory_allocator':cpujmav,'Comment': cpucmv, 'User':user}, ignore_index=True ) #dropdown value
            #print(pd.DataFrame(rows))
            newpd1 = pd.concat([newdb,pd.DataFrame(rows)], sort=False , ignore_index=True, join_axes=[newpd.columns]) #dropdown的data與table的data dataframe合併
            print(newpd1)
            newpd2 = newpd1.combine_first(newpd) #刪除重複的column      
            if newpd2.isnull().values.any():
                return "Upload Fail"
            else:
                newpd2.to_csv(dbname, index=False, header=True, encoding='utf-8-sig')
                currentdb = pd.read_csv(dbname)                
                print(currentdb)
                return "Upload Successfully"
            
            

         


#------------- callback search button --------------
@app.callback([Output('search_button', 'disabled'), Output('p2_provider', 'message')],
              [Input('p2_DataID_cpu', 'value')],
              )
def set_button_enabled_state(value):
    dbname2 = "data/SPECCPU2017.csv"
    currentdb2 = pd.read_csv(dbname2)
    if value in currentdb2['Test_ID'].values.tolist():
       return False, 'Do you want to modify the test data?'
    else:
       return True, 'Do you want to add the test data?'

#------------- callback data from csv --------------
@app.callback([Output('p2_cpu_product', 'value'), Output('p2_cpu_date', 'date'),
               Output('p2_cpu_cpu', 'value'), Output('p2_cpu_cpu_c', 'value'), Output('p2_cpu_cpu_ty', 'value'), Output('p2_cpu_mem', 'value'), 
               Output('p2_cpu_mem_sp', 'value'), Output('p2_cpu_mem_l', 'value'),Output('p2_cpu_ff', 'value'), Output('p2_cpu_sm', 'value'), 
               Output('p2_cpu_sn', 'value'), Output('p2_cpu_ss', 'value'), Output('p2_cpu_fs', 'value'), Output('p2_cpu_bp', 'value'), 
               Output('p2_cpu_pp', 'value'), Output('p2_cpu_os', 'value'), Output('p2_cpu_ccv', 'value'), Output('p2_cpu_cfv', 'value'), 
               Output('p2_cpu_jma', 'value'), Output('p2_cpu_comment', 'value'), Output('p2_editing_table_cpu', 'data')],
                [Input('search_button', 'n_clicks')],
                [State('p2_DataID_cpu', 'value')])
def update_value(n_clicks, value):
    if not n_clicks:
        return ''
    dictOfvalue_list = []
    list2 = ['SPECCPU2017']
    dbname2 = "data/SPECCPU2017.csv"
    currentdb2 = pd.read_csv(dbname2, keep_default_na=False)
    df_value = currentdb2[currentdb2['Test_ID'] == value]
    value_list = df_value.iloc[0].tolist()
    data_list0 = value_list[2:9]
    data_list1 = eval(value_list[9]) #取值將str轉成list(memory location)
    data_list2 = value_list[10:22]
    data_list0.append(data_list1)
    data_list = data_list0 + data_list2
    value_list2 = value_list[22:30]
    print(value_list)

    #Datatable的data為list(dist)，先將資料轉成dict再存到list中
    list2.extend(value_list2)
    listOfStr = ["Test Item", "Integer_Speed(Base)", "Integer_Speed(Peak)" , "Integer_Rate(Base)" , "Integer_Rate(Peak)" , "Floating_Point_Speed(Base)" , "Floating_Point_Speed(Peak)", "Floating_Point_Rate(Base)", "Floating_Point_Rate(Peak)" ]
    zipbObj = zip(listOfStr, list2)
    dictOfvalue = dict(zipbObj) #轉dict
    dictOfvalue_list.append(dictOfvalue) #加入list
    data_list.append(dictOfvalue_list) #將table的data加入
    print(data_list)
    return data_list


#--------------live update dropdown value-----------------------------
@app.callback([Output('p2_cpu_product','options'), Output('p2_cpu_cpu','options'), Output('p2_cpu_mem','options'), Output('p2_cpu_ff','options'), Output('p2_cpu_sm','options'), Output('p2_cpu_ss','options')],
              [Input('interval-cpu', 'n_intervals')])
def update_model_options(n):
    df = pd.read_csv("data/component_project.csv")
    #models = df['Model Name']
    #models_id = df['ID']
    projects = df['Product Name']
    projects_id = df['ID']
    dfc = pd.read_csv("data/component_cpu.csv")
    cpus = dfc['Processor Name']
    cpus_id = dfc['ID']
    dfm = pd.read_csv("data/component_memory.csv")
    mems = dfm['Part Number']
    mems_id = dfm['ID']
    dfs = pd.read_csv("data/component_storage.csv")
    form_factor = dfs['Form Factor']
    storage_id = dfs['ID']
    storage_model = dfs['Storage Model Name']
    storage_speed = dfs['Storage Interface']

    return [{'label': i1 , 'value': j1} for i1,j1 in zip(projects,projects_id)], [{'label': i2 , 'value': j2} for i2,j2 in zip(cpus,cpus_id)], [{'label': i3 , 'value': j3} for i3,j3 in zip(mems,mems_id)], [{'label': p, 'value': p} for p in form_factor.unique()], [{'label': i4 , 'value': j4} for i4,j4 in zip(storage_model,storage_id)], [{'label': p2, 'value': p2} for p2 in storage_speed.unique()]
