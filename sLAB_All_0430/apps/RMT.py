import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dst
import pandas as pd
from sqlalchemy.types import Interval
from datetime import datetime as dt
from app import app
from flask_login import logout_user, current_user


from apps import Login

df_rmt = pd.read_csv('data/Test_Item_model_RMT.csv')
df_guide = pd.read_csv('data/Test_Item_model_Guideline.csv')
df_memory_type_list = pd.read_csv('data/RMT_guideline.csv')
pcb_name = pd.read_csv('data/PCB_Nmae.csv')
value_list = []
ID_value_list=[]
value=dt.now().strftime("%Y%m%d%H%M%S")


#=================================Page========================================================

def create_layout(app):
    return html.Div([
        dcc.Interval(
            id='interval-rmt',
            interval=5000,
            n_intervals=0
        ),
        html.H2('RMT Info.'),
        html.Label('Test ID'),
        html.Div([
            dcc.Dropdown(
                id='DataID_RMT',
                options=[{'label': i , 'value': i} for i in ID_value_list]
            )
        ]),
        html.Div(id='p2_rmt_addmessage'),
        html.Div([
            html.Label('PCB Name'),
            dcc.Dropdown(
                id='p2_rmt_pcb'
            )
        ]),
        html.Div([
            dcc.Input(
                id='pcb_input'
            ),
            html.Button('Add PCB Name', id='pcb_add', n_clicks=0),
        ]),
        html.Div([
            html.Label('Memory Part Number'),
            dcc.Dropdown(
                id='p2_rmt_mem'
            )
        ]),
        html.Div([
            html.Label('Memory Frequency'),
            dcc.Dropdown(
                id='p2_rmt_freq',
                options=[{'label': i , 'value': i} for i in df_memory_type_list['mem_list']]
            )
        ]),
        html.Div([
            html.Label('Test Set'),
            dcc.Dropdown(
                id='p2_rmt_set',
                options=[
                    {'label': '1x1x3', 'value': '1x1x3'},
                    {'label': '3x3x3', 'value': '3x3x3'},
                    {'label': '2x5x3', 'value': '2x5x3'}
                ],
                value='1x1x3',
                clearable = False
            ),
        ]),
        html.Div([
            html.Div(generate_table2(df_guide)),
        ]),
        html.Br(),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Upload RMT Reuslt',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div([
            html.Div(generate_table(df_rmt)),
        ]),
        #html.Button('Upload', id='Upload_button', style={'display': 'inline-block', 'vertical-align': 'middle'}),
        html.Div([
            dcc.ConfirmDialogProvider(
               children=html.Button(
                    'Upload',
                ),
                id='p2_provider_rmt',
                message='Do you want to update the information?'
            ),
        ]),
        html.Div(id='p2_output-provider_rmt'),
        html.Div(id='output-data-upload')    
])

#------------- Generate table --------------

def generate_table(dataframe):
    return dst.DataTable(
            id='p2_editing_table_rmt',
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


def generate_table2(dataframe):
    return dst.DataTable(
            id='p2_editing_table_guide',
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


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    value_list.clear()
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8'))) #,header=None, sep='\n', na_values='.'
            print(df)
            # Assume that the user uploaded a CSV file
            if df.columns[0] != 'Rank':
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),header=None, sep='\n', na_values='.') #
                print(df)
                print(df.columns[0])
                print(list(df.columns))
                a = list(df.columns)
                print(a[0])
                df = df[0].str.split(',', expand=True) #忽略無header
                df = df.loc[1:, [7, 6, 9, 8, 13, 12, 15, 14, 19, 18, 21, 20, 25, 24]]
                df.rename(columns={"RxDqs-":"7", "RxDqs+":"6", "RxV-":"9", "RxV+":"8", "TxDq-":"13", "TxDq+":"12", "TxV-":"15", "TxV+":"14", "Cmd-":"19", "Cmd+":"18", "CmdV-":"21", "CmdV+":"20", "Ctl-":"25", "Ctl+":"24"})
                for i in [7, 6, 9, 8, 13, 12, 15, 14, 19, 18, 21, 20, 25, 24]:
                    value_list.append(df[i].min())
                #df.abs()
                #dfa = df.min(axis = 0)
                print(value_list)
            else:
                print(df)
                print(df.columns[0])
                df = df.loc[:, ["RxDqs-","RxDqs+","RxV-","RxV+","TxDq-","TxDq+","TxV-","TxV+","Cmd-","Cmd+","CmdV-","CmdV+","Ctl-","Ctl+"]]
                for a in ["RxDqs-","RxV-","TxDq-","TxV-","Cmd-","CmdV-","Ctl-"]:
                    df[a] = df[a].astype(float)
                    df[a] = df[a].abs()

                for i in ["RxDqs-","RxDqs+","RxV-","RxV+","TxDq-","TxDq+","TxV-","TxV+","Cmd-","Cmd+","CmdV-","CmdV+","Ctl-","Ctl+"]:
                    value_list.append(df[i].min())
                print(value_list)
             
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([


        dst.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

    ])

'''
        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'

        })
'''
#新增檔案上傳功能
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    else:
        return None

#新增datatable
@app.callback([Output('p2_editing_table_rmt', 'data')],
                [Input('output-data-upload', 'children'),Input('p2_user', 'value')])
def update_value(children, name):
    if name is None:
        value_list.clear()
    data_list = []    
    dictOfvalue_list = []
    list1 = ['WorstCase']												

    #Datatable的data為list(dist)，先將資料轉成dict再存到list中
    list1.extend(value_list)
    listOfStr = ["Test Item", "RxDqs-", "RxDqs+" , "RxV-" , "RxV+" , "TxDq-" , "TxDq+", "TxV-", "TxV+" , "Cmd-", "Cmd+", "CmdV-" , "CmdV+", "Ctl-", "Ctl+"]
    zipbObj = zip(listOfStr, list1)
    dictOfvalue = dict(zipbObj) #轉dict
    dictOfvalue_list.append(dictOfvalue) #加入list
    data_list.append(dictOfvalue_list) #將table的data加入
    print(data_list)
    print(type(data_list))
    return data_list
'''
@app.callback([Output('p2_rmt_set', 'value')],
                [Input('p2_rmt_freq', 'value')])
def freq_drop(value):
    #data_list2.clear()
    if value is not None:
        return [None]
'''


#更新Guide_LineTable
@app.callback([Output('p2_editing_table_guide', 'data')],
                [Input('p2_rmt_freq', 'value'), Input('p2_rmt_set', 'value')])
def update_value(value, rmtset):
    data_list2 = [] 
    if value is not None:
      
        data_list2 = []
        dictOfvalue_list2 = []
        list2 = ['Guideline']

        #取data
        df_value = df_memory_type_list[df_memory_type_list['mem_list'] == value]
        value_list = df_value.iloc[0].tolist()
        if rmtset == 113:
            data_list0 = value_list[1:15]
        else:
            data_list0 = value_list[15:29]
        #Datatable的data為list(dist)，先將資料轉成dict再存到list中
        list2.extend(data_list0)
        listOfStr = ["Test Item", "RxDqs-.", "RxDqs+." , "RxV-." , "RxV+." , "TxDq-." , "TxDq+.", "TxV-.", "TxV+." , "Cmd-.", "Cmd+.", "CmdV-." , "CmdV+.", "Ctl-.", "Ctl+."]
        zipbObj = zip(listOfStr, list2)
        dictOfvalue = dict(zipbObj) #轉dict
        dictOfvalue_list2.append(dictOfvalue) #加入list
        data_list2.append(dictOfvalue_list2) #將table的data加入
        print(data_list2)
        print(type(data_list2))
        return data_list2
    else:
        return [[{'Test Item': 'Guideline', 'RxDqs-': None, 'RxDqs+': None, 'RxV-': None, 'RxV+': None, 'TxDq-': None, 'TxDq+': None, 'TxV-': None, 'TxV+': None, 'Cmd-': None, 'Cmd+': None, 'CmdV-': None, 'CmdV+': None, 'Ctl-': None, 'Ctl+': None}]]


#更新PCB_Name
@app.callback(
    [Output('p2_rmt_pcb', 'options'),Output('p2_rmt_pcb', 'value'), Output('p2_rmt_addmessage', 'children')],
    [Input('pcb_add', 'n_clicks')],
    [State('pcb_input','value')])
def update_options(n_clicks, value):
    if value is None:
        pcb_name = pd.read_csv('data/PCB_Nmae.csv')
        return [{'label': i , 'value': i} for i in pcb_name['Name']], value, None
    else:
        NEW_PCB_NAME = pd.read_csv('data/PCB_Nmae.csv', keep_default_na=False,dtype=str)        
        index_value_pcb = NEW_PCB_NAME[NEW_PCB_NAME['Name'] == value].index.tolist()
        print(index_value_pcb)
        NEW_PCB_NAME = NEW_PCB_NAME.drop(index_value_pcb)
        df_add = pd.DataFrame({"Name": [value]})
        NEW_PCB_NAME2 = NEW_PCB_NAME.append(df_add)
        NEW_PCB_NAME2.to_csv('data/PCB_Nmae.csv', index=False, header=True, encoding='utf-8-sig')

        PCB_list = NEW_PCB_NAME['Name'].tolist()        
        PCB_list.append(value)
        drop_list = []    
        for i in PCB_list:
            drop_list.append({'label':i, 'value': i})
        return drop_list, value, "Upload Successfully"

#更新Data_ID
@app.callback([Output('DataID_RMT','options'), Output('DataID_RMT','value')],
              [Input('p2_user', 'value')]
              )
def update_id(name):
    value=dt.now().strftime("%Y%m%d%H%M%S")
    if name is None:
        return [{'label': value , 'value': value}], value
    else:
        df_ID = pd.read_csv("data/RMT.csv")
        print(df_ID)
        ID_value = df_ID[df_ID['User'] == name]
        print(ID_value)
        ID_value_list =ID_value['Test_ID'].tolist()
        ID_value_list.append(value)
        pcb_name_list = ID_value['PCB_Name'].tolist()

        ID_list = []
        pcb_name_list.append('')
        for i, j in zip(pcb_name_list, ID_value_list):
             ID_list.append({'label': str(i)+"   "+str(j) , 'value': j})
 
        return ID_list, value


#上傳資料
@app.callback(Output('p2_output-provider_rmt', 'children'),
                  [Input('p2_provider_rmt', 'submit_n_clicks'), Input('p2_editing_table_rmt', 'data'), Input('p2_editing_table_guide', 'data')],
              [State('DataID_RMT', 'value'), State('p2_rmt_pcb', 'value'), State('p2_rmt_mem', 'value'), State('p2_rmt_freq', 'value'), State('p2_rmt_set', 'value'), State('p2_user', 'value')])
def update_output(submit_n_clicks, data, guide, data_id, pcb_name, rmt_mem, rmt_freq, testset, user):
        if not submit_n_clicks:
            return ''
        else:

            dbname = "data/RMT.csv"
            currentdb = pd.read_csv(dbname, keep_default_na=False,dtype=str)
            index_value = currentdb[currentdb['Test_ID'] == str(data_id)].index.tolist()#透過test_id找dataframe的index
            newdb = currentdb.drop(index_value)#透過index刪除重複的row
            cpu_mem = rmt_freq.split('_') 
            

            data_F = pd.DataFrame(data).drop(columns='Test Item')
            print(data_F)
            guide_F = pd.DataFrame(guide).drop(columns='Test Item')
            print(guide_F)
            result = pd.concat([data_F, guide_F], axis=1, sort=False)
            print(result)
            info_F = pd.DataFrame({'Test_ID': data_id, 'PCB_Name': pcb_name, 'Memory_Name': rmt_mem, 'Memory_Frequency': cpu_mem[1], 'Intel_code_name': cpu_mem[0], 'Sample':testset, 'User': user}, index=[0])
            print(info_F)


            newpd = pd.concat([result, info_F], axis=1, sort=False)
            print(newpd)
            
            newpd1 = pd.concat([newdb,newpd], sort=False , ignore_index=True, join_axes=[newpd.columns]) #dropdown的data與table的data dataframe合併

            newpd11 = pd.concat([newpd1,pd.DataFrame(guide)], sort=False , ignore_index=True, join_axes=[newpd1.columns])
            print(newpd11)
            newpd2 = newpd1.combine_first(newpd) #刪除重複的column
            print(newpd2)
            newpd2 = newpd2[['Test_ID', 'PCB_Name', 'Memory_Name', 'Memory_Frequency', 'Intel_code_name', 'Sample', 'RxDqs-', 'RxDqs+', 'RxV-', 'RxV+',	'TxDq-', 'TxDq+', 'TxV-', 'TxV+', 'Cmd-', 'Cmd+', 'CmdV-', 'CmdV+', 'Ctl-', 'Ctl+', 'User', 'RxDqs-.', 'RxDqs+.', 'RxV-.', 'RxV+.',	'TxDq-.', 'TxDq+.', 'TxV-.', 'TxV+.', 'Cmd-.', 'Cmd+.', 'CmdV-.', 'CmdV+.', 'Ctl-.', 'Ctl+.']]
            if newpd2.isnull().values.any():
                return "Upload Fail"
            else:
                newpd2.to_csv(dbname, index=False, header=True, encoding='utf-8-sig')
                currentdb = pd.read_csv(dbname)
                print(currentdb)
                return "Upload Successfully"


#--------------live update dropdown value-----------------------------
@app.callback(Output('p2_rmt_mem','options'),
              [Input('interval-rmt', 'n_intervals')])
def update_model_options(n):
    dfm = pd.read_csv("data/component_memory.csv")
    mems = dfm['Part Number']
    mems_id = dfm['Part Number']

    return [{'label': i3 , 'value': j3} for i3, j3 in zip(mems,mems_id)]


if __name__ == '__main__':
    app.run_server(debug=False)
