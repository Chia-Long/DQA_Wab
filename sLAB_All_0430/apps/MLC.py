from datetime import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dst
import pandas as pd
from dash.dependencies import Input, Output, State
from pandas.core.frame import DataFrame
from sqlalchemy.types import Interval

from app import app

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
    # Page layouts
    return html.Div([
        dcc.Interval(
            id='interval-mlc',
            interval=5000,
            n_intervals=0
        ),
        #page1
        html.H2('MLC System Info.'),
        html.Label('Test ID'),
        html.Div([            
            dcc.Dropdown(
                id='p2_DataID_mlc',
                options=[{'label': i , 'value': i} for i in ID_value_list],
                style={'display':'inline-block', 'width':'250px', 'vertical-align': 'middle'}
            ),
            #dcc.Input( id='p2_DataID_mlc', value=dt.now().strftime("%Y%m%d%H%M%S"), type='number',  style={'width': '12%', 'display': 'inline-block'}),
            html.Button('Search', id='search_button_mlc', style={'display': 'inline-block', 'vertical-align': 'middle'}),
        ]),
        html.Label('Test Date'),
        html.Div([            
            dcc.DatePickerSingle(
                id='p2_mlc_date',
                min_date_allowed=dt(2000, 1, 1),
                max_date_allowed=dt(2099, 12, 31),
                initial_visible_month=dt.today(),
                style={'width': '60%'}
            )
        ]),
        html.Hr(),


        html.Div([
            html.Label('Product Name'),
            dcc.Dropdown(
                id='p2_mlc_product'
            )
        ], style=drop_style),
        html.Hr(),
        html.Div([
            html.Label('CPU'),
            dcc.Dropdown(
                id='p2_mlc_cpu'
            )
        ], style=drop_style),

        html.Div([
            html.Label('CPU數量'),
            dcc.Dropdown(
                id='p2_mlc_cpu_c',
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
                id='p2_mlc_cpu_ty',
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
                id='p2_mlc_mem'
            )
        ], style=drop_style),

        html.Div([
            html.Label('Link Speed MT/s'),
            dcc.Dropdown(
                id='p2_mlc_mem_sp',
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
                id='p2_mlc_mem_l',
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
                labelStyle={'display': 'inline-block'},
                value=['A1']
            ),
        ], style={'width': '23%', 'height': '10%'}),
        #row1
        html.Div([
            html.Label('Balance / Unbalance'),
            dcc.Dropdown(
                id='p2_mlc_blance',
                options=[
                    {'label': 'Balance', 'value': 'Balance'},
                    {'label': 'Unbalance', 'value': 'Unbalance'}
                ]
            )
        ], style=drop_style),

        html.Div([
            html.Label('Total Channel #'),
            dcc.Dropdown(
                id='p2_mlc_ch',
                options=[
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'},
                    {'label': '4', 'value': '4'},
                    {'label': '8', 'value': '8'},
                ]
            )
        ], style=drop_style),

        html.Div([
            html.Label('Total DIMM #'),
            dcc.Dropdown(
                id='p2_mlc_dimm',
                options=[
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'},
                    {'label': '4', 'value': '4'},
                    {'label': '8', 'value': '8'},
                ]
            )
        ], style=drop_style),
        
        html.Div([
            html.Label('MLC Version'),
            dcc.Input(
                id='p2_mlc_ver',
                type='text',
                value='',
            )
        ]),
        #row3
        html.Div([
            html.Label('Comment'),
            dcc.Input(
                id = 'p2_mlc_comment',
                placeholder = 'Enter comment',
                type = 'text',
                value = 'N/A'
            )
        ]),
        html.Hr(),
        html.H2('MLC Test Data'),
        #row4
        html.Div([
            html.Div(generate_table(df2)),
        ]),
        #row5
        html.Div([
            dcc.ConfirmDialogProvider(
                children=html.Button(
                    'Submit',
                ),
                id='p2_provider_mlc',
                message='Do you want to update the information?'
            ),
        ]),
        #row5
        html.Div([
            html.Div(id='p2_output-provider_mlc')
        ]),
        html.Br(),
    ])


#------------- Generate table --------------

def generate_table(dataframe):
    return dst.DataTable(
            id='p2_editing_table_mlc',
            # table-head
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

@app.callback([Output('p2_DataID_mlc','options'), Output('p2_DataID_mlc','value')],
              [Input('p2_user', 'value')]
              )
def update_id(name):
    value=dt.now().strftime("%Y%m%d%H%M%S")
    if value is None:
        return [{'label': value , 'value': value}], value
    else:
        df_ID = pd.read_csv("data/MLC.csv")
        ID_value = df_ID[df_ID['User'] == name]
        ID_value_list =ID_value['Test_ID'].tolist()
        ID_value_list.append(value)
        projects_list = ID_value['Product_Name'].tolist()
        df_pj = pd.read_csv("data/component_project.csv",  index_col ='ID')
        pj_list = []
        for a in projects_list:
            pj_list.append(df_pj.loc[a,'Product Name'])

        pj_list.append('')
        drop_list = []
        for i, j in zip(pj_list, ID_value_list):
            drop_list.append({'label': str(j)+"   "+str(i), 'value': j})    
        return drop_list, value



@app.callback(Output('p2_output-provider_mlc', 'children'),
                  [Input('p2_provider_mlc', 'submit_n_clicks'), Input('p2_editing_table_mlc', 'data')],
              [State('p2_DataID_mlc', 'value'), State('p2_mlc_product', 'value'), State('p2_mlc_date', 'date'), State('p2_mlc_cpu', 'value'), 
              State('p2_mlc_cpu_c', 'value'), State('p2_mlc_cpu_ty', 'value'), State('p2_mlc_mem', 'value'), State('p2_mlc_mem_sp', 'value'), State('p2_mlc_mem_l', 'value'),
              State('p2_mlc_blance', 'value'), State('p2_mlc_ch', 'value'), State('p2_mlc_dimm', 'value'), State('p2_mlc_ver', 'value'), State('p2_mlc_comment', 'value'), State('p2_user', 'value')])
def update_output(submit_n_clicks, rows, data_id, prov, timev, cpuv, cpucv, cputyv, memv, memspv, memlv, blance, mlcch, mlcdimm, mlcver, cpucmv,user):
        if not submit_n_clicks:
            return ''
        else:
            dbname = "data/MLC.csv"
            currentdb = pd.read_csv(dbname, keep_default_na=False,dtype=str)
            index_value = currentdb[currentdb['Test_ID'] == str(data_id)].index.tolist()#透過test_id找dataframe的index
            newdb = currentdb.drop(index_value)#透過index刪除重複的row
            newpd = newdb.append({'Test_ID': data_id, 'Model_Name': prov, 'Product_Name': prov, 'Test_Date': timev, 'CPU': cpuv, 'CPU_#':cpucv, 
            'Topology': cputyv, 'Memory': memv, 'Link_Speed': memspv, 'Memory_Location': memlv, 'Balance/Unbalance': blance, 'Total_Channel_#': mlcch,
            'Total_DIMM_#': mlcdimm, 'MLC_Version': mlcver, 'Comment': cpucmv, 'User': user}, ignore_index=True)

            newpd1 = pd.concat([newdb,pd.DataFrame(rows)], sort=False , ignore_index=True, join_axes=[newpd.columns]) #dropdown的data與table的data dataframe合併
            newpd2 = newpd1.combine_first(newpd) #刪除重複的column
            if newpd2.isnull().values.any():
                return "Upload Fail"
            else:
                newpd2.to_csv(dbname, index=False, header=True, encoding='utf-8-sig')
                currentdb = pd.read_csv(dbname)
                print(currentdb)
                return "Upload Successfully"

#------------- callback search button --------------
@app.callback([Output('search_button_mlc', 'disabled'), Output('p2_provider_mlc', 'message')],
              [Input('p2_DataID_mlc', 'value')],
              )
def set_button_enabled_state(value):
    dbname2 = "data/MLC.csv"
    currentdb2 = pd.read_csv(dbname2)
    if value in currentdb2['Test_ID'].values.tolist():
       return False, 'Do you want to modify the test data?'
    else:
       return True, 'Do you want to add the test data?'


#------------- callback data from csv --------------
@app.callback([Output('p2_mlc_product', 'value'), Output('p2_mlc_date', 'date'),
               Output('p2_mlc_cpu', 'value'), Output('p2_mlc_cpu_c', 'value'), Output('p2_mlc_cpu_ty', 'value'), Output('p2_mlc_mem', 'value'), 
               Output('p2_mlc_mem_sp', 'value'), Output('p2_mlc_mem_l', 'value'),Output('p2_mlc_blance', 'value'), Output('p2_mlc_ch', 'value'), 
               Output('p2_mlc_dimm', 'value'), Output('p2_mlc_ver', 'value'), Output('p2_mlc_comment', 'value'), Output('p2_editing_table_mlc', 'data')],
                [Input('search_button_mlc', 'n_clicks')],
                [State('p2_DataID_mlc', 'value')])
def update_value(n_clicks, value):
    if not n_clicks:
        return ''
    dictOfvalue_list = []
    list2 = ['MLC']
    
    dbname2 = "data/MLC.csv"
    currentdb2 = pd.read_csv(dbname2,keep_default_na=False)
    
    #取data
    df_value = currentdb2[currentdb2['Test_ID'] == value]
    value_list = df_value.iloc[0].tolist()
    data_list0 = value_list[2:9]
    data_list1 = eval(value_list[9]) #取值將str轉成list(memory location)
    data_list2 = value_list[10:15]
    data_list0.append(data_list1)
    data_list = data_list0 + data_list2

    value_list2 = value_list[15:17]
    print(value_list)

    #Datatable的data為list(dist)，先將資料轉成dict再存到list中
    list2.extend(value_list2)    
    
    listOfStr = ["Test Item", "All_Reads(MB/s)", "1:1_Reads_Writes(MB/s)"]
    zipbObj = zip(listOfStr, list2)
    dictOfvalue = dict(zipbObj) #轉dict
    dictOfvalue_list.append(dictOfvalue) #加入list
    data_list.append(dictOfvalue_list) #將table的data加入
    print(data_list)
    return data_list



#--------------live update dropdown value-----------------------------
@app.callback([Output('p2_mlc_product','options'), Output('p2_mlc_cpu','options'), Output('p2_mlc_mem','options')],
              [Input('interval-mlc', 'n_intervals')])
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

    return [{'label': i1 , 'value': j1} for i1,j1 in zip(projects,projects_id)], [{'label': i2 , 'value': j2} for i2,j2 in zip(cpus,cpus_id)], [{'label': i3 , 'value': j3} for i3,j3 in zip(mems,mems_id)]
