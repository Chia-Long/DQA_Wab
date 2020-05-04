from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
import pandas as pd
from pandas.core.frame import DataFrame
import dash_table as dst
from collections import OrderedDict
import numpy as np

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

models = df['Model Name']
models_id = df['ID']
projects = df['Product Name']
projects_id = df['ID']
cpus = dfc['Processor Name']
cpus_id = dfc['ID']
mems = dfm['Part Number']
mems_id = dfm['ID']


df_per_row_dropdown = pd.DataFrame(OrderedDict([
    ('Form Factor', [0]),
    ('Storage Model', [0]),
    ('Storage Number', [0]),
    ('I/O Type Bus Speed',[0]),
]))

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
            id='interval-sto',
            interval=30000,
            n_intervals=0
        ),
        html.H2('Storage Performance System Info'),
        html.Label('Test ID'),
        html.Div([
            dcc.Dropdown(
                id='p2_st_DataID',
                options=[{'label': i , 'value': i} for i in ID_value_list],
                style={'display':'inline-block', 'width':'250px', 'vertical-align': 'middle'}
            ),
            #dcc.Input( id='p2_st_DataID', value=dt.now().strftime("%Y%m%d%H%M%S"), type='number'),
            html.Button('Search', id='p2_st_search_button', n_clicks=0 , disabled=True, style={'display': 'inline-block', 'vertical-align': 'middle'}),
        ]),
        html.Label('Test Date'),
        html.Div([
            dcc.DatePickerSingle(
                id='p2_st_date',
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
                id='p2_st_product'
            )
        ], style=drop_style),
        html.Hr(),

        html.Div([
            html.Label('CPU'),
            dcc.Dropdown(
                id='p2_st_cpu',
            )
        ], style=drop_style),

        html.Div([
            html.Label('CPU數量'),
            dcc.Dropdown(
                id='p2_st_cpu_c',
                options=[
                    {'label': 1 , 'value': 1},
                    {'label': 2 , 'value': 2},
                    {'label': 4 , 'value': 4},
                ]
            )
        ], style=drop_style),

        html.Div([
            html.Label('Topology'),
            dcc.Dropdown(
                id='p2_st_cpu_ty',
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
                id='p2_st_mem'
            )
        ], style=drop_style),

        html.Div([
            html.Label('Link Speed MT/s'),
            dcc.Dropdown(
                id='p2_st_mem_sp',
                options=[
                    {'label': "2133", 'value': '2133'},
                    {'label': "2400", 'value': '2400'},
                    {'label': "2666", 'value': '2666'},
                    {'label': "2933", 'value': '2933'}
                ]
            )
        ], style=drop_style),

        html.Div([
            html.Label('Memory Location'),
            dcc.Checklist(
                id='p2_st_mem_l',
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
        html.Div([
            html.Label('Controller'),
            dcc.Dropdown(
                id='p2_st_ctl',
                options=[
                    {'label': 'CPU', 'value': 'CPU'},
                    {'label': 'PCH', 'value': 'PCH'},
                    {'label': 'LSI', 'value': 'LSI'},
                    {'label': 'Microsemi', 'value': 'Microsemi'},
                ]
            )
        ], style=drop_style),


        html.Div([
            html.Label('Structure'),
            dcc.Dropdown(
                id='p2_st_struc',
                options=[
                    {'label': 'Passthrough', 'value': 'Passthrough'},
                    {'label': 'RAID0', 'value': 'RAID0'},
                    {'label': 'RAID1', 'value': 'RAID1'},
                    {'label': 'RAID5', 'value': 'RAID5'},
                ],
            ),
        ], style=drop_style),
        html.Br(),
        html.Br(),
        html.Br(),

        html.Div([
            dst.DataTable(
                id='p2_st_dropdown_per_row',
                data=df_per_row_dropdown.to_dict('records'),
				
                style_cell={'textAlign': 'center'},
                row_deletable=True,
                columns=[
                    {'id': 'Form Factor', 'name': 'Form Factor', 'presentation': 'dropdown'},
                    {'id': 'Storage Model', 'name': 'Storage型號', 'presentation': 'dropdown'},
                    {'id': 'Storage Number', 'name': 'Storage數量', 'presentation': 'dropdown'},
                    {'id': 'I/O Type Bus Speed', 'name': 'I/O Type Bus Speed', 'presentation': 'dropdown'},
                    ],
                editable=True,
                style_cell_conditional=[
                    {'if':{'column_id':'Form Factor'},
                    'width': '25%'},
                    {'if':{'column_id':'Storage型號'},
                    'width': '25%'},
                    {'if':{'column_id':'Storage數量'},
                    'width': '25%'},
                    {'if':{'column_id':'I/O Type Bus Speed'},
                    'width': '25%'},
                ],
                style_header={
                'backgroundColor': '#3D9970',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'color': 'white'
                },
            ),
            html.Div(id='p2_st_dropdown_per_row_container'),
            html.Button('+', id='p2_st_editing-rows-button', n_clicks=0, style={'fontColor': 'blue', 'fontSize': '30px'}),

            ]),


        html.Div([
            html.Label('Comment'),
            dcc.Input(
                id='p2_st_comment',
                placeholder='Enter a value...',
                type='text',
                value='N/A',
            )
        ]),
        html.Hr(),
        html.H2('Storage Test Data'),


        html.Div([
            html.Div(generate_table(df3)),
        ]),


        html.Div([
            dcc.ConfirmDialogProvider(
                children=html.Button(
                    'Submit',
                ),
                id='p2_st_provider',
                message='Do you want to update the information?'
            ),
        ]),

        html.Div(id='p2_st_output-provider'),
        html.Br(),
        html.Div(id='select-button', children='add:0 tog:0 last:nan', style={'display': 'none'}),
    ])

#------------- Generate table --------------
def generate_table(dataframe):
    return dst.DataTable(
            id='p2_st_editing_table',
            columns=[
              {'name': c, 'id': c, 'editable': (c != 'Test Item'), 'type': 'numeric'} for c in dataframe.columns
            ],
            data=dataframe.to_dict('rows'),
			editable=True,
            style_header={
                'whiteSpace': 'normal',
                'height': 'auto',
                'minWidth': '90px',
                'width': '90px',
                'maxWidth': '90px',
                'backgroundColor': '#3D9970',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'color': 'white'
            },
            style_cell={'textAlign': 'center'},
            style_data_conditional=[
              {
                'if': {
                      'column_id': 'Test Item',
                 },
                      'backgroundColor': '#3D9970',
                      'fontWeight': 'bold',
                      'textAlign': 'center',
                      'color': 'white',
              },
           ]
        )


#------------- callback test item model Table --------------

#------------- callback test item model Table --------------

@app.callback([Output('p2_st_DataID','options'), Output('p2_st_DataID','value')],
              [Input('p2_user', 'value')]
              )
def update_id(name):
    value=dt.now().strftime("%Y%m%d%H%M%S")
    if value is None:
        return [{'label': value , 'value': value}], value
    else:
        df_ID = pd.read_csv("data/Storage_Performance.csv")
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


#------------- Write all test config and data to csv --------------

@app.callback(Output('p2_st_output-provider', 'children'),
                  [Input('p2_st_provider', 'submit_n_clicks'), Input('p2_st_dropdown_per_row', 'data'), Input('p2_st_editing_table', 'data')],
              [State('p2_st_DataID', 'value'), State('p2_st_product', 'value'), 
               State('p2_st_date', 'date'), State('p2_st_cpu', 'value'), State('p2_st_cpu_c', 'value'), State('p2_st_cpu_ty', 'value'), 
               State('p2_st_mem', 'value'), State('p2_st_mem_sp', 'value'), State('p2_st_mem_l', 'value'),State('p2_st_ctl', 'value'), 
               State('p2_st_struc', 'value'), State('p2_st_comment', 'value'), State('p2_user', 'value')])
def update_output(submit_n_clicks,cfg_rows,data_rows,data_id,prov,timev,cpuv,cpucv,cputyv,memv,memspv,memlv,stctlv,stsv,stcv,user):
        if not submit_n_clicks:
            return ''
        else:
            dbname = "data/Storage_Performance.csv"
            currentdb = pd.read_csv(dbname,keep_default_na=False,dtype=str)
            index_value = currentdb[currentdb['Test_ID'] == str(data_id)].index.tolist()#透過test_id找dataframe的index
            newdb = currentdb.drop(index_value)#透過index刪除重複的row
            newpd = newdb.append({'Test_ID': data_id, 'Model_Name': prov, 'Product_Name': prov, 'Test_Date': timev, 'CPU': cpuv, 'CPU_#':cpucv, 
            'Topology': cputyv, 'Memory': memv, 'Link_Speed': memspv, 'Memory_Location': memlv, 'Controller':stctlv, 'Structure': stsv, 'Comment': stcv, 'User':user}, ignore_index=True) #dropdown value
            print(newpd)

            #將data轉成一row的dataframe
            byte_array = []
            for i in range(2) :
                output = ''
                byte_dict = {key:val for key, val in data_rows[i].items() if len(key) > 10 }
                for key, value in byte_dict.items():
                    output += str(value) + ','
                output = output.rstrip(',')
                byte_array.append(output) #data_list            
            df_byte_array = pd.DataFrame([byte_array])
            print(df_byte_array)
            df_byte_array.columns = ["4K", "128K"]

            #讀取storage config列數產生對應的columns(st_col)和storage config填的值(pruned_rows)做結合
            df_cfg_row = pd.DataFrame(cfg_rows)
            total_cfg_row = df_cfg_row.shape[0]
            total_cfg_row1 = total_cfg_row + 1
            print(total_cfg_row1)
            st_col= []
            pruned_rows = []
            for num in range(1,total_cfg_row1):
                      st_col += [ "Form_Factor"+"_"+str(num) , "Storage_Model"+"_"+str(num) , "Storage_Number"+"_"+str(num) , "I/O_Type_Bus_Speed"+"_"+str(num) ]
            for i in range(total_cfg_row) :
                cfg_dict = {key:val for key, val in cfg_rows[i].items()}
                for key, value in cfg_dict.items():
                      pruned_rows.append(value)

            print(pruned_rows)

            df_pruned_rows = pd.DataFrame([pruned_rows])
       
            df_pruned_rows.columns = st_col

            print(df_pruned_rows)

            if total_cfg_row > 1:
                mix = ['Y']
                df_mix = pd.DataFrame(mix)
                df_mix.columns = ["Mix"]
            else:
                mix = ['N']
                df_mix = pd.DataFrame(mix)
                df_mix.columns = ["Mix"]

            #dataframe合併
            newpd1 = df_byte_array.combine_first(df_pruned_rows)
            newpd1 = newpd1.combine_first(df_mix)

            newpd1 = pd.concat([newdb, newpd1], sort=False , ignore_index=True, join_axes=[newpd.columns]) #dropdown的data與table的data dataframe合併
            newpd2 = newpd1.combine_first(newpd) #刪除重複的column
            #print(output)
            #print(type(output))
            #print(newpd2)
            if newpd2.ix[:, 0:19].isnull().values.any() or output.find('None') >= 0 or newpd2.ix[:, 56].isnull().values.any():
                return "Upload Fail"
            else:
                newpd2.to_csv(dbname, index=False, header=True, encoding='utf-8-sig')
                currentdb = pd.read_csv(dbname)
                return "Upload Successfully"

#------------- callback search button --------------
@app.callback(Output('p2_st_search_button', 'disabled'),
              [Input('p2_st_DataID', 'value')],
              )
def set_button_enabled_state(value):
    dbname2 = "data/Storage_Performance.csv"
    currentdb2 = pd.read_csv(dbname2)
    if value in currentdb2['Test_ID'].values.tolist():
       return False
    else:
       return True

#------------ add storage list --------------

@app.callback(
    Output('p2_st_dropdown_per_row', 'data'),
    [Input('select-button', 'children')],
    [State('p2_st_dropdown_per_row', 'data'),
     State('p2_st_dropdown_per_row', 'columns'),State('p2_st_DataID', 'value')])
def add_row(clicked , rows, columns, value):

    last_clicked = clicked[-3:]
    #print(last_clicked)

    if last_clicked == 'tog':
        print("toooooooooooooooooooog")
        dbname2 = "data/Storage_Performance.csv"
        currentdb2 = pd.read_csv(dbname2,keep_default_na=False)
        df_value = currentdb2[currentdb2['Test_ID'] == value]
        value_list = df_value.iloc[0].tolist()
        value_list2 = value_list[16:56]
        cfg_content = []
        cfg_list = []
        cfg_list1 = []
        for i in range(len(value_list2)):
            if i % 4 == 0 and i > 0:
               cfg_list.append(cfg_content)
               cfg_list1 += cfg_list
               if value_list2[i] == '':
                  break
               cfg_list = []
               cfg_content=[]
               cfg_content.append(str(value_list2[i]))
            else:
               cfg_content.append(str(value_list2[i]))

        listOfStr1 = ['Form Factor', 'Storage Model', 'Storage Number', 'I/O Type Bus Speed']
        df_cfg_list1 = pd.DataFrame(cfg_list1)
        df_cfg_list1.columns = listOfStr1
        print(df_cfg_list1.to_dict('rows'))
        return df_cfg_list1.to_dict('rows') 

    elif last_clicked == 'add':
           rows.append({c['id']: '' for c in columns})
    return rows


@app.callback(
    Output('select-button', 'children'),
    [Input('p2_st_editing-rows-button', 'n_clicks'), Input('p2_st_search_button', 'n_clicks')],
    [State('select-button', 'children')]
)
def updated_clicked(add_clicks, tog_clicks, prev_clicks):

    prev_clicks = dict([i.split(':') for i in prev_clicks.split(' ')])
    last_clicked = 'nan'

    if add_clicks > int(prev_clicks['add']):
        last_clicked = 'add'
    elif tog_clicks > int(prev_clicks['tog']):
        last_clicked = 'tog'

    cur_clicks = 'add:{} tog:{} last:{}'.format(add_clicks, tog_clicks, last_clicked)
    return cur_clicks



#------------- callback data from csv --------------

@app.callback([Output('p2_st_product', 'value'), Output('p2_st_date', 'date'),
               Output('p2_st_cpu', 'value'), Output('p2_st_cpu_c', 'value'), Output('p2_st_cpu_ty', 'value'), Output('p2_st_mem', 'value'),
               Output('p2_st_mem_sp', 'value'), Output('p2_st_mem_l', 'value'),Output('p2_st_ctl', 'value'), Output('p2_st_struc', 'value'),
               Output('p2_st_comment', 'value'), Output('p2_st_editing_table', 'data')],
                [Input('p2_st_search_button', 'n_clicks_timestamp')],
                [State('p2_st_DataID', 'value')])

def update_value(n_clicks_timestamp, value):
  if n_clicks_timestamp > 0:
      print(n_clicks_timestamp)
      dbname2 = "data/Storage_Performance.csv"
      currentdb2 = pd.read_csv(dbname2,keep_default_na=False)

      #取data
      df_value = currentdb2[currentdb2['Test_ID'] == value]
      value_list = df_value.iloc[0].tolist()
      data_list0 = value_list[2:9]
      data_list1 = eval(value_list[9]) #取值將str轉成list(memory location)
      data_list2 = value_list[10:13]
      data_list0.append(data_list1)

      data_list = data_list0 + data_list2

      dictOfvalue_list = []
      byte_data_list = value_list[13:15]
      byte_list = ['4K,', '128K,']
      listOfStr = ["Test Item", "sequential read BandWidth(MB/s)", "sequential read IOPS(k)", "sequential read Latency(us)", "sequential write BandWidth(MB/s)" , "sequential write IOPS(k)" , "sequential write Latency(us)", "randread BandWidth(MB/s)", "randread IOPS(k)", "randread Latency(us)", "randwrite BandWidth(MB/s)", "randwrite IOPS(k)", "randwrite Latency(us)"]
      for i, j in zip (byte_list, byte_data_list):

          a = i+j
          list_byte = a.split(',')
          zipbObj = zip(listOfStr, list_byte)
          dictOfvalue = dict(zipbObj)
          dictOfvalue_list.append(dictOfvalue)
   
      data_list.append(dictOfvalue_list)
      return data_list




#--------------live update dropdown value-----------------------------
@app.callback([Output('p2_st_product','options'), Output('p2_st_cpu','options'), Output('p2_st_mem','options'), Output('p2_st_dropdown_per_row','dropdown_conditional')],
              [Input('interval-sto', 'n_intervals')])
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

    conditional=[{
        'if': {
            'column_id': 'Form Factor',},
            'options': [{'label': p, 'value': p} for p in form_factor.unique()]},
            {
        'if': {
            'column_id': 'Storage Model',},
            'options': [{'label': i , 'value': j} for i,j in zip(storage_model,storage_id)]},
            {
        'if': {
            'column_id': 'Storage Number',},
            'options': [{'label': str(i), 'value': str(i)+".0" } for i in range(1,25)]}, 
            {
        'if': {
            'column_id': 'I/O Type Bus Speed',},
            'options': [{'label': p, 'value': p} for p in storage_speed.unique()]
    },]
    
	

    return [{'label': i1 , 'value': j1} for i1,j1 in zip(projects,projects_id)], [{'label': i2 , 'value': j2} for i2,j2 in zip(cpus,cpus_id)], [{'label': i3 , 'value': j3} for i3,j3 in zip(mems,mems_id)], conditional

