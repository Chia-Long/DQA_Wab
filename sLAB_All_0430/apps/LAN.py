import dash
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
from datetime import datetime as dt
import dash_table as dst
from pandas.core.frame import DataFrame
import ast
import numpy as np


dfl = pd.read_csv("data/component_lan.csv")
Controller = dfl['Controller']
lan_ID = dfl['ID']
Vender = dfl['Vendor']
Model_Name = dfl['Card Name']
Data_Rate_Per_Port = dfl['Data Rate Per Port']
System_Interface_Type = dfl['System Interface Type']

df_test_cases = pd.read_csv("./data/lan_database/LAN_PIC.csv")

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

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
    'width': '35%', 
    'height': '100%',
    'display': 'inline-block'
}
ID_value_list=[]

def create_layout(app):
    # Page layouts
    return html.Div([
        dcc.Interval(
            id='interval-lan',
            interval=5000,
            n_intervals=0
        ),
        #page1
        html.H2('LAN System Info'),
        html.Label('Test ID'),
        html.Div([
            
            dcc.Dropdown(
                id='p2_DataID_lan',
                options=[{'label': i , 'value': i} for i in ID_value_list],
                style={'display':'inline-block', 'width':'250px', 'vertical-align': 'middle'}
            ),
            #dcc.Input( id='p2_DataID_lan', value=dt.now().strftime("%Y%m%d%H%M%S"), type='number'),
            html.Button('Search', id='search_button_lan',  style={'display': 'inline-block', 'vertical-align': 'middle'}),
        ]),
        html.Label('Test Date'),
        html.Div([            
            dcc.DatePickerSingle(
                id='p2_lan_date',
                min_date_allowed=dt(2000, 1, 1),
                max_date_allowed=dt(2099, 12, 31),
                initial_visible_month=dt.today(),
                style={'width': '60%'},
            )
        ]),
        html.Hr(),

        html.Div([
            html.Label('Product Name'),
            dcc.Dropdown(
                id='p2_lan_product'
            )
        ], style=drop_style),
        html.Hr(),


        html.Div([
            html.Label('CPU'),
            dcc.Dropdown(
                id='p2_lan_cpu'
            )
        ], style=drop_style),

        html.Div([
            html.Label('CPU數量'),
            dcc.Dropdown(
                id='p2_lan_cpu_c',
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
                id='p2_lan_cpu_ty',
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
                id='p2_lan_mem'
            )
        ], style=drop_style),

        html.Div([
            html.Label('Link Speed MT/s'),
            dcc.Dropdown(
                id='p2_lan_mem_sp',
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
                id='p2_lan_mem_l',
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
        html.Hr(),

        #row1
        html.Div([            
            html.Div([
                html.Label('Card Name'),
                dcc.Dropdown(
                    id='cardname'
                )
            ], style=drop_style),
            html.Div([
                html.Label('Controller'),
                dcc.Dropdown(
                    id='controller',
                    #options=[{'label': i , 'value': j} for i,j in zip(Controller,lan_ID)],
                )
            ], style=drop_style),
            html.Div([
                html.Label('Data Rate'),
                dcc.Dropdown(
                    id='datarate',
                    options=[
                        {'label': '1Gb', 'value': '1Gb'},
                        {'label': '2.5Gb', 'value': '2.5Gb'},
                        {'label': '5Gb', 'value': '5Gb'},
                        {'label': '10Gb', 'value': '10Gb'},
                        {'label': '25Gb', 'value': '25Gb'},
                        {'label': '40Gb', 'value': '40Gb'},
                        {'label': '100Gb', 'value': '100Gb'}
                    ]
                )
            ], style=drop_style),
            html.Div([
                html.Label('Port Number'),
                dcc.Dropdown(
                    id='p2_lan_n',
                    options=[
                        {'label': '1', 'value': '1'},
                        {'label': '2', 'value': '2'},
                        {'label': '4', 'value': '4'}
                    ]
                )
            ], style=drop_style),
            html.Div([
                html.Label('Link Speed'),
                dcc.Dropdown(
                    id='linkspeedlan',
                    options=[
                        {'label': '5.0GT/s x1 lanes', 'value': '5.0GT/s x1 lanes'},
                        {'label': '5.0GT/s x2 lanes', 'value': '5.0GT/s x2 lanes'},
                        {'label': '5.0GT/s x4 lanes', 'value': '5.0GT/s x4 lanes'},
                        {'label': '5.0GT/s x8 lanes', 'value': '5.0GT/s x8 lanes'},
                        {'label': '8.0GT/s x8 lanes', 'value': '8.0GT/s x8 lanes'},
                        {'label': '8.0GT/s x16 lanes', 'value': '8.0GT/s x16 lanes'}]
                )
            ], style=drop_style)
        ]),
        html.Hr(),
        html.Div([
            html.Div([
                html.H2('Test Case'),
                dcc.Dropdown(
                    id='test_case_id',
                    options=[{'label': i, 'value': i} for i in df_test_cases['Name'].unique()],
                    placeholder="Select Test Case"
                )
            ], style={'width': '20%', 'height': '100%'}),
            html.Div([
                html.Img(id='display-image', src='children', alt='', height=250)
            ])
        ], style={'width': '100%', 'float': 'left'}),
        html.Div([
            html.Label('Comment'),
            dcc.Input(
                id = 'p2_lan_cpu_comment',
                placeholder = 'Enter comment',
                type = 'text',
                value = 'N/A'
            )
        ], style=input_style),
        html.Hr(),
        #row4
        html.H2('LAN Test Data'),
        html.Div([
            html.Div(generate_table(df4)),
        ]),
        #row5
        html.Div([
            dcc.ConfirmDialogProvider(
                children=html.Button(
                    'Submit',
                ),
                id='p2_provider_LAN',
                message='Do you want to update the information?'
            ),
        ]),
        #row5
        html.Div([
            html.Div(id='p2_output-provider_LAN')
        ]),
        html.Br(),
    ])


#------------- Generate table --------------

def generate_table(dataframe):
    return dst.DataTable(
            id='p2_editing_table_lan',
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

@app.callback(Output('p2_table-container_lan', 'children'),
              [Input('p2_item', 'value')]
              )
def update_table(value):
    if value is None:
        return ""
    elif value == 'SPECCPU2017':
        return generate_table(df1)
    elif value == 'MLC':
        return generate_table(df2)
    elif value == 'Storage Performance':
        return generate_table(df3)
    elif value == 'LAN Performance':
        return generate_table(df4)
    elif value == 'Certification':
        return generate_table(df1)
    else:
        return ""

#------------- callback test item model Table --------------

@app.callback([Output('p2_DataID_lan','options'), Output('p2_DataID_lan','value')],
              [Input('p2_user', 'value')]
              )
def update_id(name):
    value=dt.now().strftime("%Y%m%d%H%M%S")
    if value is None:
        return [{'label': value , 'value': value}], value
    else:
        df_ID = pd.read_csv("data/LAN_Performance.csv")
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


#------------- callback Card name dropdown --------------

@app.callback(
    [Output('controller', 'options')],
    [Input('cardname', 'value')]
)

def update_date_dropdown(LID):

    if LID is not None:
       print(LID)
       lan_com = pd.read_csv("data/component_lan.csv")
       df_lan_com = lan_com[lan_com['ID'] == LID]
       print(df_lan_com)
       lan_com_list = df_lan_com.iloc[0].tolist()
       print(lan_com_list)
       card_name = lan_com_list[2]
       print(card_name) 
       if card_name == 'ONBOARD':
          ctrl_name = lan_com[(lan_com['Card Name'] == 'ONBOARD')]['Controller']
          ctrl_ID = lan_com[(lan_com['Card Name'] == 'ONBOARD')]['ID']
          a= [[{'label': i, 'value': j} for i,j in zip(ctrl_name,ctrl_ID) ]]
          print(a)
          return [[{'label': i, 'value': j} for i,j in zip(ctrl_name,ctrl_ID) ]]
       else:
          ctrl_name = lan_com_list[3]
          return [[{'label': ctrl_name, 'value': LID}]]
    else:
       return [[{'label': '', 'value': ''}]] 


#------------------------------------------------------------

@app.callback(
    Output('display-image', 'src'),
    [Input('test_case_id', 'value')]
     )
def callback_image(pic):
    if pic is None:
        return ''
    else:
        path = './data/lan_database/'
        return encode_image(path+df_test_cases[(df_test_cases['Name']==pic)]['filepath'].values[0])

@app.callback(Output('p2_output-provider_LAN', 'children'),
             [Input('p2_provider_LAN', 'submit_n_clicks'), Input('p2_editing_table_lan', 'data')],
             [State('p2_DataID_lan', 'value'), State('p2_lan_product', 'value'), State('p2_lan_date', 'date'), State('p2_lan_cpu', 'value'),
              State('p2_lan_cpu_c', 'value'), State('p2_lan_cpu_ty', 'value'), State('p2_lan_mem', 'value'), State('p2_lan_mem_sp', 'value'), State('p2_lan_mem_l', 'value'),
              State('controller', 'value'), State('controller', 'value'), State('datarate', 'value'), State('p2_lan_n', 'value'), State('linkspeedlan', 'value'), 
              State('test_case_id', 'value'), State('p2_lan_cpu_comment', 'value'), State('p2_user', 'value')])
def update_output(submit_n_clicks, rows, data_id, prov, timev,cpuv,cpucv,cputyv,memv,memspv,memlv,controllerv,cardnamev,dataratev,p2_lan_nv, linkspeedlanv,test_case_idv,cpucmv,user):
        if not submit_n_clicks:
            return ''
        else:
            dbname = "data/LAN_Performance.csv"
            currentdb = pd.read_csv(dbname, keep_default_na=False,dtype=str)
            index_value = currentdb[currentdb['Test_ID'] == str(data_id)].index.tolist()#透過test_id找dataframe的index
            newdb = currentdb.drop(index_value)#透過index刪除重複的row
            print(rows)
            newpd = newdb.append({'Test_ID': data_id, 'Model_Name': prov, 'Product_Name': prov, 'Test_Date': timev, 'CPU': cpuv, 'CPU_#':cpucv, 
            'Topology': cputyv, 'Memory': memv, 'Link_Speed': memspv, 'Memory_Location': memlv, 'Controller':controllerv, 'Card_Name': cardnamev, 'Data_Rate': dataratev, 'Port_#': p2_lan_nv, 
            'Link_Speed_lan': linkspeedlanv, 'Test_Case_ID':test_case_idv, 'Comment': cpucmv, 'User': user}, ignore_index=True)

            ''' 將data轉成一row的dataframe'''
            byte_array = []
            for i in range(7) :
                output = ''
                byte_dict = {key:val for key, val in rows[i].items() if len(key) != 5}
                for key, value in byte_dict.items():
                    output += str(value) + ',' 
                output = output.rstrip(',')
                byte_array.append(output) #data_list
            df_byte_array = pd.DataFrame([byte_array])
            df_byte_array.columns = ["64_Bytes", "128_Bytes", "256_Bytes", "512_Bytes", "1024_Bytes", "1280_Bytes", "1518_Bytes"]
            print(df_byte_array)

            '''dataframe合併'''
            newpd1 = pd.concat([newdb, df_byte_array], sort=False , ignore_index=True, join_axes=[newpd.columns]) #dropdown的data與table的data dataframe合併
            newpd2 = newpd1.combine_first(newpd) #刪除重複的column
            if newpd2.ix[:, 0:16].isnull().values.any() or output.find('None') >= 0 or newpd2.ix[:, 24].isnull().values.any():
                return "Upload Fail"
            else:
                newpd2.to_csv(dbname, index=False, header=True, encoding='utf-8-sig')
                return "Upload Successfully"           

#------------- callback search button --------------
@app.callback(Output('search_button_lan', 'disabled'),
              [Input('p2_DataID_lan', 'value')],
              )
def set_button_enabled_state(value):
    dbname2 = "data/LAN_Performance.csv"
    currentdb2 = pd.read_csv(dbname2)
    if value in currentdb2['Test_ID'].values.tolist():
       return False
    else:
       return True


#------------- callback data from csv --------------
@app.callback([Output('p2_lan_product', 'value'), Output('p2_lan_date', 'date'),
               Output('p2_lan_cpu', 'value'), Output('p2_lan_cpu_c', 'value'), Output('p2_lan_cpu_ty', 'value'), Output('p2_lan_mem', 'value'), 
               Output('p2_lan_mem_sp', 'value'), Output('p2_lan_mem_l', 'value'),Output('controller', 'value'), Output('cardname', 'value'), 
               Output('datarate', 'value'), Output('p2_lan_n', 'value'), Output('linkspeedlan', 'value'), 
               Output('test_case_id', 'value'), Output('p2_lan_cpu_comment', 'value'), Output('p2_editing_table_lan', 'data')],
                [Input('search_button_lan', 'n_clicks')],
                [State('p2_DataID_lan', 'value')])
def update_value(n_clicks, value):
    if not n_clicks:
        return ''
    dictOfvalue_list = []
    
    dbname2 = "data/LAN_Performance.csv"
    currentdb2 = pd.read_csv(dbname2, keep_default_na=False)
    
    #取data
    df_value = currentdb2[currentdb2['Test_ID'] == value]
    value_list = df_value.iloc[0].tolist()
    data_list0 = value_list[2:9]
    data_list1 = eval(value_list[9]) #取值將str轉成list(memory location)
    data_list2 = value_list[10:17]
    data_list0.append(data_list1)
    data_list = data_list0 + data_list2 

    byte_data_list = value_list[17:24]


    byte_list = ['64_Bytes,', '128_Bytes,', '256_Bytes,', '512_Bytes,', '1024_Bytes,', '1280_Bytes,', '1518_Bytes,']
    
    listOfStr = ["Frame", "10%", "20%", "30%", "40%" , "50%" , "60%", "70%", "80%", "90%", "100%", "ThroughPut"]
    for i, j in zip (byte_list, byte_data_list):
        a = i+j
        print(a)
        list_byte = a.split(',')
        zipbObj = zip(listOfStr, list_byte)
        dictOfvalue = dict(zipbObj)
        dictOfvalue_list.append(dictOfvalue)
    data_list.append(dictOfvalue_list) 
    print(dictOfvalue_list)

    return data_list
   

#--------------live update dropdown value-----------------------------
@app.callback([Output('p2_lan_product','options'), Output('p2_lan_cpu','options'), Output('p2_lan_mem','options'), Output('cardname','options')],
              [Input('interval-lan', 'n_intervals')])
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
    dfl = pd.read_csv("data/component_lan.csv")
    lan_ID = dfl['ID']
    Model_Name = dfl['Card Name']
    

    return [{'label': i1 , 'value': j1} for i1,j1 in zip(projects,projects_id)], [{'label': i2 , 'value': j2} for i2,j2 in zip(cpus,cpus_id)], [{'label': i3 , 'value': j3} for i3,j3 in zip(mems,mems_id)], [{'label': i4 , 'value': j4} for i4,j4 in zip(Model_Name.unique(),lan_ID)]

