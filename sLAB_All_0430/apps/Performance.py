import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table 
from app import app
#from apps import SPECCPU2017, MLC, Storage, LAN, Certification
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import time
#import plotly.graph_objects as go

#dfx = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
#app = dash.Dash(__name__)
#app.config.suppress_callback_exceptions = True
#application = app.server

#df = pd.read_csv("Performance.csv")
# 讀取Project代碼對應表(ID v.s. Product Name)
df_pj = pd.read_csv("data/component_project.csv", index_col="ID")
df_pj.sort_values('Product Name', inplace=True)
product_name = df_pj['Product Name'].to_list()
project_id = df_pj.index.to_list()

# 讀取CPU代碼對應表(ID v.s. Code Name & Processor Name)
df_comp_cpu = pd.read_csv("data/component_cpu.csv", index_col="ID")
cpu_code_name = df_comp_cpu['Code Name'].to_list()
cpu_processor_name = df_comp_cpu['Processor Name'].to_list()
cpu_id = df_comp_cpu.index.to_list()

# 讀取Memory代碼對應表(ID v.s. Memory Types)
df_comp_memory = pd.read_csv("data/component_memory.csv", index_col="ID")
memory_types = df_comp_memory['Memory Types'].to_list()
memory_id = df_comp_memory.index.to_list()

# 讀取Storage代碼對應表(ID v.s. Category)
df_comp_storage = pd.read_csv("data/component_storage.csv", index_col="ID")
storage_category = df_comp_storage['Storage Device Category'].to_list()
storage_id = df_comp_storage.index.to_list()

# 讀取LAN代碼對應表(ID v.s. Controller)
df_comp_lan = pd.read_csv("data/component_lan.csv", index_col="ID")
lan_cnt_name = df_comp_lan['Controller'].to_list()
lan_id = df_comp_lan.index.to_list()

# 計算Performance總表數值
# 計算CPU_Performance代表性數值
df_cpu = pd.read_csv("data/SPECCPU2017.csv")
#df_cpu.replace(project_id, product_name, inplace=True)
idx_cpu = df_cpu.groupby('Product_Name')['Floating_Point_Rate(Base)'].idxmax()
#df_cpu_summary = df_cpu.iloc[idx_cpu,[2,-2]]
df_cpu_summary = df_cpu.iloc[idx_cpu,[2,-3]]
df_cpu_summary.rename(columns={'Floating_Point_Rate(Base)': 'CPU_Performance'}, inplace=True)

# 計算Memory_Performance代表性數值
#df_memory_summary = pd.DataFrame({'Product_Name': ['SKY-1234', 'VEGA-5678', 'MIC-8888', 'PAC-6666'],
#                                  'Memory_Performance': ['123', '234', '456', '889']})
df_memory = pd.read_csv("data/MLC.csv")
#df_memory.replace(project_id, product_name, inplace=True)
idx_memory = df_memory.groupby('Product_Name')['All_Reads(MB/s)'].idxmax()
#df_memory_summary = df_memory.iloc[idx_memory,[2,-2]]
df_memory_summary = df_memory.iloc[idx_memory,[2,-3]]
df_memory_summary.rename(columns={'All_Reads(MB/s)': 'Memory_Performance'}, inplace=True)

# 計算Storage_Performance代表性數值
df_storage = pd.read_csv("data/Storage_Performance.csv")
storage_col = ['128K_Sequential_Read_BandWidth(MB/s)', '128K_Sequential_Read_IOPS(k)', '128K_Sequential_Read_Latency(us)',
               '128K_Sequential_Write_BandWidth(MB/s)', '128K_Sequential_Write_IOPS(k)', '128K_Sequential_Write_Latency(us)',
               '128K_Random_Read_BandWidth(MB/s)', '128K_Random_Read_IOPS(k)', '128K_Random_Read_Latency(us)',
               '128K_Random_Write_BandWidth(MB/s)', '128K_Random_Write_IOPS(k)', '128K_Random_Write_Latency(us)']
df_storage_128k = pd.DataFrame(columns=storage_col, data=df_storage['128K'].str.split(',').to_list(), index=df_storage.index).astype('float')
df_storage_128k['Product_Name'] = df_storage['Product_Name']
idx_storage_128k = df_storage_128k.groupby('Product_Name')['128K_Sequential_Read_BandWidth(MB/s)'].idxmax()
df_storage_summary = df_storage_128k.iloc[idx_storage_128k,[-1,0]]
df_storage_summary.rename(columns={'128K_Sequential_Read_BandWidth(MB/s)': 'Storage_Performance'}, inplace=True)

# 計算LAN_Performance代表性數值
df_lan = pd.read_csv("data/LAN_Performance.csv", encoding='utf-8')
#df_lan.replace(project_id, product_name, inplace=True)
df_lan_1518 = df_lan['1518_Bytes'].str.split(',')
lan_bw = []
for i in range(len(df_lan_1518)):
    bw = str(round(((100 - float(df_lan_1518[i][9])) / 100) * int(df_lan['Port_#'][i]) * int(
        df_lan['Data_Rate'][i].replace('Gb', '')), 2))
    lan_bw.append(bw)
lan_bw_float = [float(i) for i in lan_bw]
df_lan.loc[:, 'LAN_Performance'] = lan_bw_float
idx_lan = df_lan.groupby('Product_Name')['LAN_Performance'].idxmax()
df_lan_summary = df_lan.iloc[idx_lan, [2, -1]]

# 合併Performance總表數據
df_perf_1 = pd.merge(df_cpu_summary, df_memory_summary, on='Product_Name', how='outer').fillna('---')
df_perf_2 = pd.merge(df_perf_1, df_storage_summary, on='Product_Name', how='outer').fillna('---')
df_perf_all = pd.merge(df_perf_2, df_lan_summary, on='Product_Name', how='outer').fillna('---')
#df_perf_1 = pd.merge(df_cpu_summary, df_memory_summary, on='Product_Name', how='outer')
#df_perf_2 = pd.merge(df_perf_1, df_storage_summary, on='Product_Name', how='outer')
#df_perf_all = pd.merge(df_perf_2, df_lan_summary, on='Product_Name', how='outer')
#df_perf_all_index = df_perf_all.sort_values(by=['Product_Name'])
df_perf_all_index = df_perf_all.sort_values(by=['Product_Name'])
df_perf_all_index.set_index('Product_Name', inplace=True)
df_perf_all_index['Product_Name'] = df_perf_all_index.index
df_perf_all_index.replace(project_id, product_name, inplace=True)
df_perf_all_index = df_perf_all_index[['Product_Name', 'CPU_Performance', 'Memory_Performance', 'Storage_Performance', 'LAN_Performance']]

# SPECCPU2017 Test Results
df1 = pd.read_csv("data/SPECCPU2017.csv", index_col="Product_Name")
df1['Product_Name'] = df1.index
# 將MPxxxxx代碼取代為Product Name
df1['Product_Name'].replace(project_id, product_name, inplace=True)
df1.insert(4, "Processor_Name", df1['CPU'], True)
df1.insert(4, "Code_Name", df1['CPU'], True)
df1['Code_Name'].replace(cpu_id, cpu_code_name, inplace=True)
df1['Processor_Name'].replace(cpu_id, cpu_processor_name, inplace=True)

# 計算畫Bar用的Width百分比數值
#for i in df1.columns[-9:-1].to_list():
for i in df1.columns[-10:-2].to_list():
    df1[i + '_Bar'] = df1[i] / df1[i].max() * 99


#df1_c = df1.ix[:,[2, 3, -8, -7, -6, -5, -4, -3, -2, -1]]
# MLC Test Results
df2 = pd.read_csv("data/MLC.csv", index_col="Product_Name")
df2['Product_Name'] = df2.index
df2['Product_Name'].replace(project_id, product_name, inplace=True)
df2.insert(7, "Memory_Types", df2['Memory'], True)
df2['Memory_Types'].replace(memory_id, memory_types, inplace=True)

# 計算畫Bar用的Width百分比數值
df2['All_Reads(MB/s)_Bar'] = df2['All_Reads(MB/s)'] / df2['All_Reads(MB/s)'].max() * 99
df2['1:1_Reads_Writes(MB/s)_Bar'] = df2['1:1_Reads_Writes(MB/s)'] / df2['1:1_Reads_Writes(MB/s)'].max() * 99
#df2_c = df2.iloc[:,[2, 3, -2]]


# LAN_Performance
df3 = pd.read_csv("data/LAN_Performance.csv", index_col="Product_Name")
#df3['Product_Name'] = df_lan_perf.index
#df_lan_perf.replace(project_id, product_name, inplace=True)
#df_lan_all = df3.iloc[:, [-7, -6, -5, -4, -3, -2, -1]]
df_lan_all = df3.iloc[:, [-8, -7, -6, -5, -4, -3, -2]]
for i in df_lan_all.columns.to_list():
    lan_all_bw = []
    df_lan_all_c = df_lan_all[i].str.split(',')
    for j in range(len(df_lan_all_c)):
        #print(j)
        bw = str(round(((100 - float(df_lan_all_c[j][9])) / 100) * int(df3['Port_#'][j]) * int(
            df3['Data_Rate'][j].replace('Gb', '')), 2))
        lan_all_bw.append(bw)
    lan_all_bw_float = [float(k) for k in lan_all_bw]
    #print(lan_bw_float)
    df_lan_all.loc[:, str(i + '_BW')] = lan_all_bw_float
for i in df_lan_all.columns[-7:].to_list():
    df3[i] = df_lan_all[i]
for i in df3.columns[-7:].to_list():
    df3[i + '_Bar'] = df3[i] / df3[i].max() * 99
df3['Detail'] = df3['Test_ID']
df3['Product_Name'] = df3.index
df3['Product_Name'].replace(project_id, product_name, inplace=True)
df3.replace(lan_id, lan_cnt_name, inplace=True)

# Storage_Performance
df4 = pd.read_csv("data/Storage_Performance.csv", index_col="Product_Name")
storage_col = ['128K_Sequential_Read_BandWidth(MB/s)', '128K_Sequential_Read_IOPS(k)', '128K_Sequential_Read_Latency(us)',
               '128K_Sequential_Write_BandWidth(MB/s)', '128K_Sequential_Write_IOPS(k)', '128K_Sequential_Write_Latency(us)',
               '128K_Random_Read_BandWidth(MB/s)', '128K_Random_Read_IOPS(k)', '128K_Random_Read_Latency(us)',
               '128K_Random_Write_BandWidth(MB/s)', '128K_Random_Write_IOPS(k)', '128K_Random_Write_Latency(us)']
df4_128k = pd.DataFrame(columns=storage_col, data=df4['128K'].str.split(',').to_list(), index=df4.index).astype('float')
df4 = pd.merge(df4, df4_128k, on='Product_Name', how='outer')
#for i in df4.columns[55:].to_list():
for i in df4.columns[56:].to_list():
    df4[i + '_Bar'] = df4[i] / df4[i].max() * 99
df4['Product_Name'] = df4.index
df4['Product_Name'].replace(project_id, product_name, inplace=True)
df4.insert(9, "Category", df4['Storage_Model_1'], True)
df4['Category'].replace(storage_id, storage_category, inplace=True)


def generate_summary(dataframe, title):
    return dash_table.DataTable(
            # table-head  
            id='P3-Performance-Summary',         
            columns=[
              {'name': [title, c.replace("_", " ")], 'id': c} for c in dataframe.columns
              #{"name": i, "id": i, "deletable": True, "selectable": True} for i in dataframe.columns
            ],
            data=dataframe.to_dict('records'),
            #row_deletable=True,
            #filter_action="native",
            sort_action="native",
            sort_mode="multi",
            #column_selectable="single",
            #editable=True,
            # table-row
            #fixed_rows={'headers': True},
            #page_action="native",
            #page_current= 0,
            #page_size= 15,
            merge_duplicate_headers=True,
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
                    #'width': '120px',
                    'whiteSpace': 'normal', #讓過長的Title換行顯示
                    'height': 'auto',
                    'minWidth': '110px',
                    'width': '110px',
                    'maxWidth': '110px',
                    'backgroundColor': 'rgb(114,164,118)',
                    'fontSize': '14px',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '1px solid white',
                    'textAlign': 'center',
                    #'marginTop': '12px',
                }),
            )


def generate_table(dataframe, title):
    return dash_table.DataTable(
            # table-head  
            id='P3-Performance-all',         
            columns=[
                {'name': [title, c.replace("_", " ")], 'id': c, 'type': 'text'} for c in dataframe.columns
			  #{'name': [title, c.replace("_", " ")], 'id': c, "deletable": True, "selectable": True} for c in dataframe.columns
              #{"name": i, "id": i, "deletable": True, "selectable": True} for i in dataframe.columns
            ],
            data=dataframe.to_dict('records'),
            row_deletable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            #column_selectable="single",
            #editable=True,
            # table-row
            #fixed_rows={'headers': True},
            page_action="native",
            page_current=0,
            page_size=15,
            merge_duplicate_headers=True,
            style_cell_conditional=[
                {'if': {'column_id': 'Test_ID'},
                 'display': 'none'},
                {
                    'if': {
                        'column_id': 'All_Reads(MB/s)',
                    },
                    'width': '25%'
                },
                {
                    'if': {
                        'column_id': '1:1_Reads_Writes(MB/s)',
                    },
                    'width': '25%'
                },
            ],
            style_data_conditional=[
                {
                    'if': {
                        'row_index': 'odd',
                    },
                    'backgroundColor': 'rgb(235,240,236)',
                    'color': 'black',
                    'fontSize': '15px',
                    'fontWeight': 'bold',
                    #'fontFamily': 'Arial',
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
                    #'fontFamily': 'Arial',
                    'textAlign': 'center',
                    'border': '1px solid white',
                }
            ],
            style_header=(
                {
                    #'width': '120px',
                    'whiteSpace': 'normal', #讓過長的Title換行顯示
                    'height': 'auto',
                    'minWidth': '80px',
                    #'width': '110px',
                    'maxWidth': '110px',
                    'backgroundColor': 'rgb(114,164,118)',
                    'fontSize': '15px',
                    'fontWeight': 'bold',
                    #'fontFamily': 'Arial',
                    'color': 'white',
                    'border': '1px solid white',
                    'textAlign': 'center',
                    #'marginTop': '12px',
                }),
            )


"""
def generate_table1(dataframe,selected_columns):
    return dash_table.DataTable(
            # table-head   
            id='P3-Performance-one',
            columns=[
              {'name': 'Product Name', 'id': 'Product_Name'},
              {'name': 'Test_ID', 'id': 'Test_ID'},
              {'name': 'Test Date', 'id': 'Test_Date'},
              {'name': selected_columns.replace("_", " "), 'id': selected_columns},
              {'name': selected_columns + '_Bar', 'id': selected_columns + '_Bar'}
              #{'name': 'Integer_Speed(Base)', 'id': 'Integer_Speed(Base)'}

            ],
            
            #editable=True,
            # table-row
            data=dataframe.to_dict('records'),
            #column_selectable="single",
            row_deletable=True,
            style_cell_conditional=[
                {'if': {'column_id': 'Product_Name'},
                 'width': '20%'},
                {'if': {'column_id': 'Test_Date'},
                 'width': '20%'},
                {'if': {'column_id': 'Test_ID'},
                 'display': 'none'},
                {'if': {'column_id': selected_columns + '_Bar'},
                 'display': 'none'},
                {'if': {'column_id': selected_columns.replace("_", " ")},
                 'width': '60%'},
            ],
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
                    #'width': '120px',
                    'backgroundColor': 'rgb(114,164,118)',
                    'fontSize': '15px',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '1px solid white',
                    'textAlign': 'center',
                }),
            sort_action='native'
 
        )
"""


def generate_table_storage(dataframe):
    return dash_table.DataTable(
            # table-head
            id='P3-Performance-Storage',
            columns=[
                {'name': ["Test_ID", "Test_ID", "Test_ID"], 'id': 'Test_ID'},
                {'name': ["Storage Performance", "", "Product Name"], 'id': 'Product_Name'},
                {'name': ["Storage Performance", "", "Test Date"], 'id': 'Test_Date'},
                {'name': ["Storage Performance", "", "Category"], 'id': 'Category'},
                {'name': ["Storage Performance", "", "Storage #"], 'id': 'Storage_Number_1'},
                {'name': ["Storage Performance", "", "Structure"], 'id': 'Structure'},
                {"name": ["Storage Performance", "128K Sequential Read", "BandWidth (MB/s)"],
                 "id": "128K_Sequential_Read_BandWidth(MB/s)"},
                {"name": ["Storage Performance", "128K Sequential Read", "IOPS (k)"], "id": "128K_Sequential_Read_IOPS(k)"},
                {"name": ["Storage Performance", "128K Sequential Read", "Latency (us)"], "id": "128K_Sequential_Read_Latency(us)"},
                {"name": ["Storage Performance", "128K Sequential Write", "BandWidth (MB/s)"],
                 "id": "128K_Sequential_Write_BandWidth(MB/s)"},
                {"name": ["Storage Performance", "128K Sequential Write", "IOPS (k)"], "id": "128K_Sequential_Write_IOPS(k)"},
                {"name": ["Storage Performance", "128K Sequential Write", "Latency (us)"],
                 "id": "128K_Sequential_Write_Latency(us)"},
                {"name": ["Storage Performance", "128K Random Read", "BandWidth (MB/s)"],
                 "id": "128K_Random_Read_BandWidth(MB/s)"},
                {"name": ["Storage Performance", "128K Random Read", "IOPS (k)"], "id": "128K_Random_Read_IOPS(k)"},
                {"name": ["Storage Performance", "128K Random Read", "Latency (us)"], "id": "128K_Random_Read_Latency(us)"},
                {"name": ["Storage Performance", "128K Random Write", "BandWidth (MB/s)"],
                 "id": "128K_Random_Write_BandWidth(MB/s)"},
                {"name": ["Storage Performance", "128K Random Write", "IOPS (k)"], "id": "128K_Random_Write_IOPS(k)"},
                {"name": ["Storage Performance", "128K Random Write", "Latency (us)"], "id": "128K_Random_Write_Latency(us)"},
            ],
            row_deletable=True,
            sort_action="native",
            sort_mode="multi",
            filter_action="native",
            #editable=True,
            # table-row
            page_action="native",
            page_current=0,
            page_size=15,
            data=dataframe.to_dict('rows'),
            merge_duplicate_headers=True,
            #style_header_conditional=[
            #    {'if': {'column_id': 'Product_Name'},
            #     'borderTop': 'none'},
            #],
            style_cell_conditional=[
                {'if': {'column_id': 'Test_ID'},
                 'display': 'none'},
            ],
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
                    #'width': '120px',
                    'whiteSpace': 'normal',  # 讓過長的Title換行顯示
                    'height': 'auto',
                    #'minWidth': '80px',
                    # 'width': '110px',
                    'maxWidth': '80px',
                    'backgroundColor': 'rgb(114,164,118)',
                    'fontSize': '15px',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '1px solid white',
                    'textAlign': 'center',
                    #'verticalAlign': 'bottom',
                }),
            )


back_to_previous_link_style = {
    'display': 'inline-block',
    'float': 'right',
    'marginRight': '10px',
    'marginTop': '10px',
    #'fontFamily': '微軟正黑體',
    'fontFamily': 'Arial',
    'fontWeight': 'bold',
    'fontSize': '10pt',
}


layout = html.Div([
    
    #dcc.Location(id='p3-url', refresh=False),
    #dcc.Link('To All performance table', href='/apps/WebOutput'),
    html.Div(id='P3-Performance-container'),
    html.Div(id='P3-Performance-hidden-1', style={'display': 'none'}),
    #html.Div(id='P3-Performance-hidden-2', style={'display': 'none'}),
    html.Div(id='P3-Performance-hidden-3', style={'display': 'none'}),
    
])
        
app.clientside_callback(
    ClientsideFunction(namespace='ui', function_name='replaceWithLinks'),
    Output('P3-Performance-hidden-1', 'children'),
    [Input('P3-Performance-all', 'derived_viewport_data')]
)

#app.clientside_callback(
#    ClientsideFunction(namespace='bar', function_name='createBarChart'),
#    Output('P3-Performance-hidden-2', 'children'),
#    [Input('lan-container', 'children')]
#)

app.clientside_callback(
    ClientsideFunction(namespace='storage', function_name='mergeTableRow'),
    Output('P3-Performance-hidden-3', 'children'),
    [Input('P3-Performance-Storage', 'derived_viewport_data')]
)


@app.callback(Output('P3-Performance-container', 'children'),
              #[Input('p3-url', 'pathname'),Input("P3-drp1", "value")]
              [Input('p0-url1', 'pathname'),Input("P3-drp1", "value")]
              #[Input('p3-url', 'pathname')]
              #[State('item', 'value'), ]
              )
def update_table(pathname,value):
    #print (pathname,value)
    #if pathname is None:
    #    return ""
    if pathname == '/apps/WebOutput/CPU_Performance':
        if value is None:
            #df1_c = df1.ix[:,[-9, 2, -17, -16, -15, -14, -13, -12, -11, -10]]
            df1_c = df1.ix[:, [-9, 2, 4, 5, 6, -18, -17, -16, -15, -14, -13, -12, -11, 0]]
        elif len(value) == 0:
            #df1_c = df1.ix[:,[-9, 2, -17, -16, -15, -14, -13, -12, -11, -10]]
            df1_c = df1.ix[:, [-9, 2, 4, 5, 6, -18, -17, -16, -15, -14, -13, -12, -11, 0]]
        else:
            value_f = value.copy()
            for i in value:
                if i in df1.index.to_list():
                    continue
                else:
                    value_f.remove(i)
            #df1_c = df1.ix[list(value_f),[-9, 2, -17, -16, -15, -14, -13, -12, -11, -10]]
            df1_c = df1.ix[list(value_f), [-9, 2, 4, 5, 6, -18, -17, -16, -15, -14, -13, -12, -11, 0]]
            
        return html.Div([
            dcc.Link('[LAN]', href='/apps/WebOutput/LAN_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Storage]', href='/apps/WebOutput/Storage_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Memory]', href='/apps/WebOutput/Memory_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[CPU]', href='/apps/WebOutput/CPU_Performance', style=back_to_previous_link_style, refresh=True),
            #dcc.Link('回上一頁', href='/apps/WebOutput', style=back_to_previous_link_style),
            html.Div([], style={'clear': 'both'}),
            generate_table(df1_c,'SPEC CPU® 2017'),
            html.Br(),
            html.Br(),
            html.Div(id='cpu-container')
        ])

    elif pathname == '/apps/WebOutput/Memory_Performance':
        if value is None:
            #df2_c = df2.ix[:, [-3, 2, -5, -4]]
            df2_c = df2.ix[:, [-3, 2, 7, 8, 12, -6, -5, 0]]
        elif len(value) == 0:
            #df2_c = df2.ix[:, [-3, 2, -5, -4]]
            df2_c = df2.ix[:, [-3, 2, 7, 8, 12, -6, -5, 0]]
        else:
            value_f = value.copy()
            for i in value:
                if i in df2.index.to_list():
                    continue
                else:
                    value_f.remove(i)
            #df2_c = df2.ix[list(value_f), [-3, 2, -5, -4]]
            df2_c = df2.ix[list(value_f), [-3, 2, 7, 8, 12, -6, -5, 0]]
            
        return html.Div([
            dcc.Link('[LAN]', href='/apps/WebOutput/LAN_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Storage]', href='/apps/WebOutput/Storage_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Memory]', href='/apps/WebOutput/Memory_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[CPU]', href='/apps/WebOutput/CPU_Performance', style=back_to_previous_link_style, refresh=True),
            #dcc.Link('回上一頁', href='/apps/WebOutput', style=back_to_previous_link_style),
            html.Div([], style={'clear': 'both'}),
            generate_table(df2_c,'Intel® Memory Latency Checker'),
            html.Br(),
            html.Br(),
            html.Div(id='mem-container')
        ])

    elif pathname == '/apps/WebOutput/LAN_Performance':
        if value is None:
            #df3_c = df3.ix[:,[1, 2, -7, -6, -5, -4, -3, -2, -1]]
            df3_c = df3.ix[:, [-1, 2, 9, 11, 12, -16, -15, -14, -13, -12, -11, -10, -2, 0]]
        elif len(value) == 0:
            #df3_c = df3.ix[:,[1, 2, -7, -6, -5, -4, -3, -2, -1]]
            df3_c = df3.ix[:, [-1, 2, 9, 11, 12, -16, -15, -14, -13, -12, -11, -10, -2, 0]]
        else:
            value_f = value.copy()
            for i in value:
                if i in df3.index.to_list():
                    continue
                else:
                    value_f.remove(i)
            df3_c = df3.ix[list(value_f), [-1, 2, 9, 11, 12, -16, -15, -14, -13, -12, -11, -10, -2, 0]]
 
        #print(type(df3_c))
        #print(df3)
        return html.Div([
            dcc.Link('[LAN]', href='/apps/WebOutput/LAN_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Storage]', href='/apps/WebOutput/Storage_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Memory]', href='/apps/WebOutput/Memory_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[CPU]', href='/apps/WebOutput/CPU_Performance', style=back_to_previous_link_style, refresh=True),
            #dcc.Link('回上一頁', href='/apps/WebOutput', style=back_to_previous_link_style),
            html.Div([], style={'clear': 'both'}),
            generate_table(df3_c,'LAN Bandwidth'),
            html.Br(),
            html.Br(),
            html.Div(id='lan-container')
        ])

    elif pathname == '/apps/WebOutput/Storage_Performance':
        if value is None:
            df4_c = df4.ix[:, [-1, 2, 9, 18, 11, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, 0]]
        elif len(value) == 0:
            df4_c = df4.ix[:, [-1, 2, 9, 18, 11, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, 0]]
        else:
            value_f = value.copy()
            for i in value:
                if i in df4.index.to_list():
                    continue
                else:
                    value_f.remove(i)
            df4_c = df4.ix[list(value_f), [-1, 2, 9, 18, 11, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, 0]]
        #print(df4_c)

        return html.Div([
            dcc.Link('[LAN]', href='/apps/WebOutput/LAN_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Storage]', href='/apps/WebOutput/Storage_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Memory]', href='/apps/WebOutput/Memory_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[CPU]', href='/apps/WebOutput/CPU_Performance', style=back_to_previous_link_style, refresh=True),
            #dcc.Link('回上一頁', href='/apps/WebOutput', style=back_to_previous_link_style),
            html.Div([], style={'clear': 'both'}),
            generate_table_storage(df4_c),
            html.Br(),
            html.Br(),
            html.Div(id='sto-container')
        ])

    else:
        if value is None:
            return html.Div([
                #html.Div(style={'height': '12px'}),
                dcc.Link('[LAN]', href='/apps/WebOutput/LAN_Performance', style=back_to_previous_link_style, refresh=True),
                dcc.Link('[Storage]', href='/apps/WebOutput/Storage_Performance', style=back_to_previous_link_style, refresh=True),
                dcc.Link('[Memory]', href='/apps/WebOutput/Memory_Performance', style=back_to_previous_link_style, refresh=True),
                dcc.Link('[CPU]', href='/apps/WebOutput/CPU_Performance', style=back_to_previous_link_style, refresh=True),
                #dcc.Link('回上一頁', href='/apps/WebOutput', style=back_to_previous_link_style),
                html.Div([], style={'clear': 'both'}),
                generate_summary(df_perf_all_index, 'Performance Summary')
            ])
        elif len(value) == 0:
            return html.Div([
                #html.Div(style={'height': '12px'}),
                dcc.Link('[LAN]', href='/apps/WebOutput/LAN_Performance', style=back_to_previous_link_style, refresh=True),
                dcc.Link('[Storage]', href='/apps/WebOutput/Storage_Performance', style=back_to_previous_link_style, refresh=True),
                dcc.Link('[Memory]', href='/apps/WebOutput/Memory_Performance', style=back_to_previous_link_style, refresh=True),
                dcc.Link('[CPU]', href='/apps/WebOutput/CPU_Performance', style=back_to_previous_link_style, refresh=True),
                #dcc.Link('回上一頁', href='/apps/WebOutput', style=back_to_previous_link_style),
                html.Div([], style={'clear': 'both'}),
                generate_summary(df_perf_all_index, 'Performance Summary')
            ])
        else:
            value_f = value.copy()
            for i in value:
                if i in df_perf_all_index.index.to_list():
                    #print(df_perf_all_index.index.to_list())
                    continue
                else:
                    value_f.remove(i)
            df_perf_all_index_filter = df_perf_all_index.ix[list(value_f), :]
        return html.Div([
            #html.Div(style={'height': '12px'}),
            dcc.Link('[LAN]', href='/apps/WebOutput/LAN_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Storage]', href='/apps/WebOutput/Storage_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[Memory]', href='/apps/WebOutput/Memory_Performance', style=back_to_previous_link_style, refresh=True),
            dcc.Link('[CPU]', href='/apps/WebOutput/CPU_Performance', style=back_to_previous_link_style, refresh=True),
            #dcc.Link('回上一頁', href='/apps/WebOutput', style=back_to_previous_link_style),
            html.Div([], style={'clear': 'both'}),
            generate_summary(df_perf_all_index_filter, 'Performance Summary')
        ])


#@app.callback(Output('p1-test', 'children'),
#             [Input('p1_pro_sub', 'submit_n_clicks'), Input('p2_provider', 'submit_n_clicks'),
#              Input('p2_provider_mlc', 'submit_n_clicks'), Input('p2_st_pro', 'submit_n_clicks'),
#              Input('p2_provider_LAN', 'submit_n_clicks'), Input('p2_provider_cer', 'submit_n_clicks'),])
#def update_table(component, cpu, memory, storage, lan, certification):
#    if component:
#        print('Oh yes!')
#        return 'It wasn\'t easy but we did it {}'.format(component)


@app.callback(Output('P3-drp1', 'options'),
             [Input('P3-interval', 'n_intervals')])
def update_data(tick):
    #print('Tick !')
    tStart = time.time()
    global df_perf_all_index, df1, df2, df3, df4
    df_pj = pd.read_csv("data/component_project.csv", index_col="ID")
    df_pj.sort_values('Product Name', inplace=True)
    product_name = df_pj['Product Name'].to_list()
    project_id = df_pj.index.to_list()

    # 讀取CPU代碼對應表(ID v.s. Code Name & Processor Name)
    df_comp_cpu = pd.read_csv("data/component_cpu.csv", index_col="ID")
    cpu_code_name = df_comp_cpu['Code Name'].to_list()
    cpu_processor_name = df_comp_cpu['Processor Name'].to_list()
    cpu_id = df_comp_cpu.index.to_list()

    # 讀取Memory代碼對應表(ID v.s. Memory Types)
    df_comp_memory = pd.read_csv("data/component_memory.csv", index_col="ID")
    memory_types = df_comp_memory['Memory Types'].to_list()
    memory_id = df_comp_memory.index.to_list()

    # 讀取Storage代碼對應表(ID v.s. Category)
    df_comp_storage = pd.read_csv("data/component_storage.csv", index_col="ID")
    storage_category = df_comp_storage['Storage Device Category'].to_list()
    storage_id = df_comp_storage.index.to_list()

    # 讀取LAN代碼對應表(ID v.s. Controller)
    df_comp_lan = pd.read_csv("data/component_lan.csv", index_col="ID")
    lan_cnt_name = df_comp_lan['Controller'].to_list()
    lan_id = df_comp_lan.index.to_list()

    # 計算Performance總表數值
    # 計算CPU_Performance代表性數值
    df_cpu = pd.read_csv("data/SPECCPU2017.csv")
    # df_cpu.replace(project_id, product_name, inplace=True)
    idx_cpu = df_cpu.groupby('Product_Name')['Floating_Point_Rate(Base)'].idxmax()
    # df_cpu_summary = df_cpu.iloc[idx_cpu,[2,-2]]
    df_cpu_summary = df_cpu.iloc[idx_cpu, [2, -3]]
    df_cpu_summary.rename(columns={'Floating_Point_Rate(Base)': 'CPU_Performance'}, inplace=True)

    # 計算Memory_Performance代表性數值
    # df_memory_summary = pd.DataFrame({'Product_Name': ['SKY-1234', 'VEGA-5678', 'MIC-8888', 'PAC-6666'],
    #                                  'Memory_Performance': ['123', '234', '456', '889']})
    df_memory = pd.read_csv("data/MLC.csv")
    # df_memory.replace(project_id, product_name, inplace=True)
    idx_memory = df_memory.groupby('Product_Name')['All_Reads(MB/s)'].idxmax()
    # df_memory_summary = df_memory.iloc[idx_memory,[2,-2]]
    df_memory_summary = df_memory.iloc[idx_memory, [2, -3]]
    df_memory_summary.rename(columns={'All_Reads(MB/s)': 'Memory_Performance'}, inplace=True)

    # 計算Storage_Performance代表性數值
    df_storage = pd.read_csv("data/Storage_Performance.csv")
    storage_col = ['128K_Sequential_Read_BandWidth(MB/s)', '128K_Sequential_Read_IOPS(k)',
                   '128K_Sequential_Read_Latency(us)',
                   '128K_Sequential_Write_BandWidth(MB/s)', '128K_Sequential_Write_IOPS(k)',
                   '128K_Sequential_Write_Latency(us)',
                   '128K_Random_Read_BandWidth(MB/s)', '128K_Random_Read_IOPS(k)', '128K_Random_Read_Latency(us)',
                   '128K_Random_Write_BandWidth(MB/s)', '128K_Random_Write_IOPS(k)', '128K_Random_Write_Latency(us)']
    df_storage_128k = pd.DataFrame(columns=storage_col, data=df_storage['128K'].str.split(',').to_list(),
                                   index=df_storage.index).astype('float')
    df_storage_128k['Product_Name'] = df_storage['Product_Name']
    idx_storage_128k = df_storage_128k.groupby('Product_Name')['128K_Sequential_Read_BandWidth(MB/s)'].idxmax()
    df_storage_summary = df_storage_128k.iloc[idx_storage_128k, [-1, 0]]
    df_storage_summary.rename(columns={'128K_Sequential_Read_BandWidth(MB/s)': 'Storage_Performance'}, inplace=True)

    # 計算LAN_Performance代表性數值
    df_lan = pd.read_csv("data/LAN_Performance.csv", encoding='utf-8')
    # df_lan.replace(project_id, product_name, inplace=True)
    df_lan_1518 = df_lan['1518_Bytes'].str.split(',')
    lan_bw = []
    for i in range(len(df_lan_1518)):
        bw = str(round(((100 - float(df_lan_1518[i][9])) / 100) * int(df_lan['Port_#'][i]) * int(
            df_lan['Data_Rate'][i].replace('Gb', '')), 2))
        lan_bw.append(bw)
    lan_bw_float = [float(i) for i in lan_bw]
    df_lan.loc[:, 'LAN_Performance'] = lan_bw_float
    idx_lan = df_lan.groupby('Product_Name')['LAN_Performance'].idxmax()
    df_lan_summary = df_lan.iloc[idx_lan, [2, -1]]

    # 合併Performance總表數據
    df_perf_1 = pd.merge(df_cpu_summary, df_memory_summary, on='Product_Name', how='outer').fillna('---')
    df_perf_2 = pd.merge(df_perf_1, df_storage_summary, on='Product_Name', how='outer').fillna('---')
    df_perf_all = pd.merge(df_perf_2, df_lan_summary, on='Product_Name', how='outer').fillna('---')
    # df_perf_1 = pd.merge(df_cpu_summary, df_memory_summary, on='Product_Name', how='outer')
    # df_perf_2 = pd.merge(df_perf_1, df_storage_summary, on='Product_Name', how='outer')
    # df_perf_all = pd.merge(df_perf_2, df_lan_summary, on='Product_Name', how='outer')
    df_perf_all_index_temp = df_perf_all.sort_values(by=['Product_Name'])
    df_perf_all_index_temp.set_index('Product_Name', inplace=True)
    df_perf_all_index_temp['Product_Name'] = df_perf_all_index_temp.index
    df_perf_all_index_temp.replace(project_id, product_name, inplace=True)
    df_perf_all_index_temp = df_perf_all_index_temp[['Product_Name', 'CPU_Performance', 'Memory_Performance', 'Storage_Performance', 'LAN_Performance']]
    df_perf_all_index = df_perf_all_index_temp.copy()

    # SPECCPU2017 Test Results
    df1_temp = pd.read_csv("data/SPECCPU2017.csv", index_col="Product_Name")
    df1_temp['Product_Name'] = df1_temp.index
    # 將MPxxxxx代碼取代為Product Name
    #df1_temp.replace(project_id, product_name, inplace=True)
    df1_temp['Product_Name'].replace(project_id, product_name, inplace=True)
    df1_temp.insert(4, "Processor_Name", df1_temp['CPU'], True)
    df1_temp.insert(4, "Code_Name", df1_temp['CPU'], True)
    df1_temp['Code_Name'].replace(cpu_id, cpu_code_name, inplace=True)
    df1_temp['Processor_Name'].replace(cpu_id, cpu_processor_name, inplace=True)

    # 計算畫Bar用的Width百分比數值
    # for i in df1.columns[-9:-1].to_list():
    for i in df1_temp.columns[-10:-2].to_list():
        df1_temp[i + '_Bar'] = df1_temp[i] / df1_temp[i].max() * 99
    df1 = df1_temp.copy()
    # df1_c = df1.ix[:,[2, 3, -8, -7, -6, -5, -4, -3, -2, -1]]

    # MLC Test Results
    df2_temp = pd.read_csv("data/MLC.csv", index_col="Product_Name")
    df2_temp['Product_Name'] = df2_temp.index
    df2_temp['Product_Name'].replace(project_id, product_name, inplace=True)
    df2_temp.insert(7, "Memory_Types", df2['Memory'], True)
    df2_temp['Memory_Types'].replace(memory_id, memory_types, inplace=True)

    # 計算畫Bar用的Width百分比數值
    df2_temp['All_Reads(MB/s)_Bar'] = df2_temp['All_Reads(MB/s)'] / df2_temp['All_Reads(MB/s)'].max() * 99
    df2_temp['1:1_Reads_Writes(MB/s)_Bar'] = df2_temp['1:1_Reads_Writes(MB/s)'] / df2_temp['1:1_Reads_Writes(MB/s)'].max() * 99
    # df2_c = df2.iloc[:,[2, 3, -2]]
    df2 = df2_temp.copy()

    # LAN_Performance
    df3_temp = pd.read_csv("data/LAN_Performance.csv", index_col="Product_Name")
    # df3['Product_Name'] = df_lan_perf.index
    # df_lan_perf.replace(project_id, product_name, inplace=True)
    # df_lan_all = df3.iloc[:, [-7, -6, -5, -4, -3, -2, -1]]
    df_lan_all = df3_temp.iloc[:, [-8, -7, -6, -5, -4, -3, -2]]
    for i in df_lan_all.columns.to_list():
        lan_all_bw = []
        df_lan_all_c = df_lan_all[i].str.split(',')
        for j in range(len(df_lan_all_c)):
            # print(j)
            bw = str(round(((100 - float(df_lan_all_c[j][9])) / 100) * int(df3_temp['Port_#'][j]) * int(
                df3_temp['Data_Rate'][j].replace('Gb', '')), 2))
            lan_all_bw.append(bw)
        lan_all_bw_float = [float(k) for k in lan_all_bw]
        # print(lan_bw_float)
        df_lan_all.loc[:, str(i + '_BW')] = lan_all_bw_float
    for i in df_lan_all.columns[-7:].to_list():
        df3_temp[i] = df_lan_all[i]
    for i in df3_temp.columns[-7:].to_list():
        df3_temp[i + '_Bar'] = df3_temp[i] / df3_temp[i].max() * 99
    df3_temp['Detail'] = df3_temp['Test_ID']
    df3_temp['Product_Name'] = df3_temp.index
    df3_temp['Product_Name'].replace(project_id, product_name, inplace=True)
    df3_temp.replace(lan_id, lan_cnt_name, inplace=True)
    df3 = df3_temp.copy()

    # Storage_Performance
    df4_temp = pd.read_csv("data/Storage_Performance.csv", index_col="Product_Name")
    storage_col = ['128K_Sequential_Read_BandWidth(MB/s)', '128K_Sequential_Read_IOPS(k)',
                   '128K_Sequential_Read_Latency(us)',
                   '128K_Sequential_Write_BandWidth(MB/s)', '128K_Sequential_Write_IOPS(k)',
                   '128K_Sequential_Write_Latency(us)',
                   '128K_Random_Read_BandWidth(MB/s)', '128K_Random_Read_IOPS(k)', '128K_Random_Read_Latency(us)',
                   '128K_Random_Write_BandWidth(MB/s)', '128K_Random_Write_IOPS(k)', '128K_Random_Write_Latency(us)']
    df4_128k = pd.DataFrame(columns=storage_col, data=df4_temp['128K'].str.split(',').to_list(), index=df4_temp.index).astype(
        'float')
    df4_temp = pd.merge(df4_temp, df4_128k, on='Product_Name', how='outer')
    # for i in df4.columns[55:].to_list():
    for i in df4_temp.columns[56:].to_list():
        df4_temp[i + '_Bar'] = df4_temp[i] / df4_temp[i].max() * 99
    df4_temp['Product_Name'] = df4_temp.index
    df4_temp['Product_Name'].replace(project_id, product_name, inplace=True)
    df4_temp.insert(9, "Category", df4_temp['Storage_Model_1'], True)
    df4_temp['Category'].replace(storage_id, storage_category, inplace=True)
    df4 = df4_temp.copy()
    tEnd = time.time()
    print(tEnd - tStart)
    print("It cost %f seconds." % (tEnd - tStart))
    return [{'label': i, 'value': j} for i, j in zip(product_name, project_id)]


@app.callback(Output('lan-container', 'children'),
            [Input('P3-Performance-all', 'derived_virtual_data'), Input('P3-Performance-all', 'active_cell')])
def update_graphs(rows, active_cell):
    #print(active_cell)
    dff = pd.DataFrame(rows)
    #y_ticktext = dff["Product_Name"].to_list()
    #y_tickvals = dff.index.to_list()
    #print(dff)
    return [
        dcc.Graph(
            #html.Br(),
            #html.Br(),
            #html.Br(),
            #html.A(id=column),
            id=lan_column,
            figure={
                "data":[
                    {
                        #"y": dff["Product_Name"],
                        "y": dff.index.to_list(),
                        "x": dff[lan_column],
                        "type": "bar",
                        "orientation": 'h',
                        "text": dff[lan_column],
                        "textposition": "inside",
                        "hoverinfo": "x",
                        "opacity": 0.8,
                        "width": 0.6,
                        "textfont": {"family": "monospace", "size": 16},
                    }
                ],
                "layout": {
                    #"barmode": "overlay",
                    "title": {"text": str('<a style="color:#007BFF;" href="#top" target="_self">[TOP]</a><br>' + lan_column),
                              "font": {"family": "monospace", "size": 18, "color": "rgb(31,73,125)"}},
                    "xaxis": {"automargin": True, "tickfont": {"family": "monospace", "size": 16, "color": "rgb(31,73,125)"},
                              "zerolinewidth": 2, "zerolinecolor": "#007BFF", "gridcolor": "rgb(242,242,242)", "gridwidth": 2},
                    "yaxis": {"automargin": True, "tickfont": {"family": "monospace", "size": 16, "color": "rgb(31,73,125)"},
                              "tickmode": "array", "ticktext": dff["Product_Name"], "tickvals": dff.index.to_list(), "autorange": "reversed"},
                    "height": 500,
                    "margin": {"t": 80, "b": 0, "l": 30, "r": 30},
                    #"font": {"family": "monospace", "size": 13},
                    #"paper_bgcolor": "rgb(244,244,248)",
                    "plot_bgcolor": "rgb(220,230,241)",
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for lan_column in ["64_Bytes_BW", "128_Bytes_BW", "256_Bytes_BW", "512_Bytes_BW", "1024_Bytes_BW", "1280_Bytes_BW", "1518_Bytes_BW"] if lan_column in dff
    ]


@app.callback(Output('cpu-container', "children"),
            [Input('P3-Performance-all', "derived_virtual_data")])
def update_graphs(rows):
    dff = pd.DataFrame(rows)
    return [
        dcc.Graph(
            #html.Br(),
            #html.Br(),
            #html.Br(),
            #html.A(id=cpu_column),
            id=cpu_column,
            figure={
                "data":[
                    {
                        #"y": dff["Product_Name"],
                        "y": dff.index.to_list(),
                        "x": dff[cpu_column],
                        "type": "bar",
                        "orientation": 'h',
                        "text" : dff[cpu_column],
                        "textposition": "inside",
                        "hoverinfo": "x",
                        "opacity": 0.8,
                        "width": 0.6,
                        "textfont": {"family": "monospace", "size": 16},
                    }
                ],
                "layout": {
                    "title": {"text": str('<a style="color:#007BFF;" href="#top" target="_self">[TOP]</a><br>' + cpu_column),
                              "font": {"family": "monospace", "size": 18, "color": "rgb(31,73,125)"}},
                    "xaxis": {"automargin": True, "tickfont": {"family": "monospace", "size": 16, "color": "rgb(31,73,125)"},
                              "zerolinewidth": 2, "zerolinecolor": "#007BFF", "gridcolor": "rgb(242,242,242)", "gridwidth": 2},
                    "yaxis": {"automargin": True, "tickfont": {"family": "monospace", "size": 16, "color": "rgb(31,73,125)"},
                              "tickmode": "array", "ticktext": dff["Product_Name"], "tickvals": dff.index.to_list(), "autorange": "reversed"},
                    "height": 500,
                    "margin": {"t": 80, "b": 0, "l": 30, "r": 30},
                    #"font": {"family": "monospace", "size": 13},
                    #"paper_bgcolor": "rgb(244,244,248)",
                    "plot_bgcolor": "rgb(220,230,241)",
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for cpu_column in ["Integer_Speed(Base)", "Integer_Speed(Peak)", "Integer_Rate(Base)", "Integer_Rate(Peak)", "Floating_Point_Speed(Base)", "Floating_Point_Speed(Peak)", "Floating_Point_Rate(Base)", "Floating_Point_Rate(Peak)"] if cpu_column in dff
    ]


@app.callback(Output('mem-container', "children"),
            [Input('P3-Performance-all', "derived_virtual_data")])
def update_graphs(rows):
    dff = pd.DataFrame(rows)
    return [
        dcc.Graph(
            #html.Br(),
            #html.Br(),
            #html.Br(),
            #html.A(id=mem_column),
            id=mem_column,
            figure={
                "data":[
                    {
                        #"y": dff["Product_Name"],
                        "y": dff.index.to_list(),
                        "x": dff[mem_column],
                        "type": "bar",
                        "orientation": 'h',
                        "text": dff[mem_column],
                        "textposition": "inside",
                        "hoverinfo": "x",
                        "opacity": 0.8,
                        "width": 0.6,
                        "textfont": {"family": "monospace", "size": 16},
                    }
                ],
                "layout": {
                    "title": {"text": str('<a style="color:#007BFF;" href="#top" target="_self">[TOP]</a><br>' + mem_column),
                              "font": {"family": "monospace", "size": 18, "color": "rgb(31,73,125)"}},
                    "xaxis": {"automargin": True, "tickfont": {"family": "monospace", "size": 16, "color": "rgb(31,73,125)"},
                              "zerolinewidth": 2, "zerolinecolor": "#007BFF", "gridcolor": "rgb(242,242,242)", "gridwidth": 2},
                    "yaxis": {"automargin": True, "tickfont": {"family": "monospace", "size": 16, "color": "rgb(31,73,125)"},
                              "tickmode": "array", "ticktext": dff["Product_Name"], "tickvals": dff.index.to_list(),
                              "autorange": "reversed"},
                    "height": 500,
                    "margin": {"t": 80, "b": 0, "l": 30, "r": 30},
                    #"font": {"family": "monospace", "size": 13},
                    #"paper_bgcolor": "rgb(244,244,248)",
                    "plot_bgcolor": "rgb(220,230,241)",
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for mem_column in ["All_Reads(MB/s)", "1:1_Reads_Writes(MB/s)"] if mem_column in dff
    ]


@app.callback(Output('sto-container', "children"),
            [Input('P3-Performance-Storage', "derived_virtual_data")])
def update_graphs(rows):
    dff = pd.DataFrame(rows)
    return [
        dcc.Graph(
            #html.Br(),
            #html.Br(),
            #html.Br(),
            #html.A(id=sto_column),
            id=sto_column,
            figure={
                "data":[
                    {
                        #"y": dff["Product_Name"],
                        "y": dff.index.to_list(),
                        "x": dff[sto_column],
                        "type": "bar",
                        "orientation": 'h',
                        "text": dff[sto_column],
                        "textposition": "inside",
                        "hoverinfo": "x",
                        "opacity": 0.8,
                        "width": 0.6,
                        "textfont": {"family": "monospace", "size": 16},
                    }
                ],
                "layout": {
                    "title": {"text": str('<a style="color:#007BFF;" href="#top" target="_self">[TOP]</a><br>' + sto_column),
                              "font": {"family": "monospace", "size": 18, "color": "rgb(31,73,125)"}},
                    "xaxis": {"automargin": True, "tickfont": {"family": "monospace", "size": 16, "color": "rgb(31,73,125)"},
                              "zerolinewidth": 2, "zerolinecolor": "#007BFF", "gridcolor": "rgb(242,242,242)", "gridwidth": 2},
                    "yaxis": {"automargin": True, "tickfont": {"family": "monospace", "size": 16, "color": "rgb(31,73,125)"},
                              "tickmode": "array", "ticktext": dff["Product_Name"], "tickvals": dff.index.to_list(), "autorange": "reversed"},
                    "height": 500,
                    "margin": {"t": 80, "b": 0, "l": 30, "r": 30},
                    #"font": {"family": "monospace", "size": 13},
                    #"paper_bgcolor": "rgb(244,244,248)",
                    "plot_bgcolor": "rgb(220,230,241)",
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for sto_column in ['128K_Sequential_Read_BandWidth(MB/s)', '128K_Sequential_Read_IOPS(k)', '128K_Sequential_Read_Latency(us)', '128K_Sequential_Write_BandWidth(MB/s)',
                        '128K_Sequential_Write_IOPS(k)', '128K_Sequential_Write_Latency(us)', '128K_Random_Read_BandWidth(MB/s)', '128K_Random_Read_IOPS(k)',
                        '128K_Random_Read_Latency(us)', '128K_Random_Write_BandWidth(MB/s)', '128K_Random_Write_IOPS(k)', '128K_Random_Write_Latency(us)'] if sto_column in dff
    ]

