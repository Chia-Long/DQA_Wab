import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import random



#colors = ['E9C46A','F4A261','E76F51','00AEE0','04294F','672A4E','EF476F','FFD166','06D6A0','118AB2','073B4C','264653','2A9D8F','69306D','F2D7EE','D3BCC0']



# 讀取Memory代碼對應表(ID v.s. Memory Types)
df_comp_memory = pd.read_csv("data/component_memory.csv", index_col="ID")
memory_part = df_comp_memory['Part Number'].to_list()
memory_id = df_comp_memory.index.to_list()
#print(df_comp_memory)


df = pd.read_csv('data/RMT.csv')
orders = list(df.columns) 
df_result = df.iloc[:,0:21]
result_orders = ['Test_ID', 'PCB_Name', 'Memory_Name', 'Memory_Frequency','Intel_code_name', 'Sample', 'RxDqs-', 'RxDqs+', 'RxV-', 'RxV+', 'TxDq-', 'TxDq+', 'TxV-', 'TxV+', 'Cmd-', 'Cmd+', 'CmdV-', 'CmdV+', 'Ctl-', 'Ctl+','User']
df_result = df_result[result_orders]

data_column_names = []
Graph_data_list = []


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.A([html.Img(id='logo',src='/assets/Advantech-logo-200P-color.jpg', width='150',style={'display': 'inline-block'})], href='/'),
        html.A([html.Label('NCG DQA RMT Database', style={'display': 'inline-block','fontFamily': 'Arial','fontSize': '24pt','textAlign': 'center','verticalAlign': 'top','margin': '0px'}),], href='http://172.17.9.218:8050/apps/login'),
    ]),
    dcc.Location(id='url', refresh=True),
    dcc.Interval(id='RMT-interval', interval=10000, n_intervals=0),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df_result.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        #row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        style_table={
            'height': '500px',
            'overflowY': 'scroll',
            'border': 'thin lightgrey solid'
        },
        style_cell_conditional=[{'textAlign': 'center'}]
    ),
    html.Div(id='datatable-interactivity-container'),
    html.Div(id='rmt-container'),
    html.Div(id='margin-container'),
])


@app.callback(Output('rmt-container', "children"),
            [Input('datatable-interactivity', "derived_virtual_data")])
def update_graphs(rows):
    Graph_data_list = []
    dff = pd.DataFrame(rows, columns=orders)
    #dff = dff.iloc[:,0:20]
    dff_result = dff.iloc[:,6:20]
    dff_result2 = dff.iloc[:,21:35]
    data_column_names = list(dff_result.columns)
    #print(data_column_names)

    for i in range(len(dff_result)):
        a = {'x': data_column_names, 'y': dff_result.loc[i].values.tolist(), 'type': 'bar', 'name': dff.iloc[i].iat[1]+ '_' + dff.iloc[i].iat[2],'text': dff_result.loc[i].values.tolist(),'textposition': 'outside'}
        b = {'x': data_column_names, 'y': dff_result2.loc[i].values.tolist(), 'type': 'markers', 'name': dff.iloc[i].iat[1]+'_Guideline', 'markers' : '202'}
        Graph_data_list.append(a)
        Graph_data_list.append(b)
    return [
        dcc.Graph(
            id='rmt_column',
            figure={
                "data": Graph_data_list,
                "layout": {
                    "title": {"text": 'Worst Case Margin Result vs Guideline'}
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        #for mem_column in ["All_Reads(MB/s)", "1:1_Reads_Writes(MB/s)"] if mem_column in dff
    ]

@app.callback(Output('margin-container', "children"),
            [Input('datatable-interactivity', "derived_virtual_data")])
def update_graphs(rows):
    Margin_data_list = []
    #margin = []
    dff = pd.DataFrame(rows, columns=orders)
    #dff = dff.iloc[:,0:20]
    dff_result = dff.iloc[:,6:20]
    dff_result2 = dff.iloc[:,21:35]
    

    data_column_names = list(dff_result.columns)
    #print(len(dff_result.loc[0].values.tolist()))
    #print(data_column_names)

    for i in range(len(dff_result)):
        margin = []
        for j in range(len(dff_result.loc[i].values.tolist())):
            d = dff_result.loc[i].values.tolist()[j] - dff_result2.loc[i].values.tolist()[j]
            margin.append(d)
        margin_data = {'x': data_column_names, 'y': margin, 'type': 'bar', 'name': dff.iloc[i].iat[1]+ '_' + dff.iloc[i].iat[2],'text': margin,'textposition': 'outside'}
        margin_data2 = {'x': None, 'y': None, 'type': 'linear', 'name': dff.iloc[i].iat[1]+'_Guideline'}
        Margin_data_list.append(margin_data)
        Margin_data_list.append(margin_data2)
    return [
        dcc.Graph(
            id='rmt_column',
            figure={
                "data": Margin_data_list,
                "layout": {
                    "title": {"text": 'Margin'}
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        #for mem_column in ["All_Reads(MB/s)", "1:1_Reads_Writes(MB/s)"] if mem_column in dff
    ]



@app.callback(Output('datatable-interactivity', 'data'),
            [Input('url', 'pathname')])
def update_data(intervals):
    global df
    df = pd.read_csv('data/RMT.csv')
    df_result = df.iloc[:,0:21]
    df_result = df_result[result_orders]
    data=df.to_dict('records')
    return data


if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0',port=8000)