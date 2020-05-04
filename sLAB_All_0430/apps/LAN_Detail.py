#import dash_core_components as dcc
from app import app
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
from dash.exceptions import PreventUpdate

layout = html.Div([
    html.Div(id="P3-Frameloss-Content", style={'marginTop': '12px'}),
    ])


def generate_table(dataframe, title):
    return dash_table.DataTable(
            # table-head
            id='P3-Performance-all',
            columns=[
                {'name': [title, c.replace("_", " ")], 'id': c} for c in dataframe.columns
            ],
            #row_deletable=True,
            #editable=True,
            # table-row
            data=dataframe.to_dict('records'),
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
                    'fontSize': '15px',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '1px solid white',
                    'textAlign': 'center',
                    #'marginTop': '12px',
                }),
            )


@app.callback(Output("P3-Frameloss-Content", "children"),
              [Input('p0-url1', 'pathname')])
def display_frameloss_data(pathname):
    if pathname is None:
        raise PreventUpdate
    elif '/apps/WebOutput/Frame_Loss' in pathname:
        #print("pathname2")
        test_id = int(pathname.split("/")[4])
        df_frameloss = pd.read_csv("data/LAN_Performance.csv", index_col="Test_ID")
        fl_col = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%', 'Throughput']
        df_obj = []
        for i in df_frameloss.columns[-8:-1].to_list():
            zip_obj = zip(fl_col, df_frameloss.loc[test_id, i].split(','))
            dict_obj = dict(zip_obj)
            df_obj.append(dict_obj)
        df_frameloss_all = pd.DataFrame(df_obj)
        fl_size = df_frameloss.columns[-8:-1]
        fl_size1 = [size.replace("_", " ") for size in fl_size]
        df_frameloss_all.insert(0, 'Frame Size', fl_size1)

        return html.Div([
            html.Div(style={'height': '12px'}),
            generate_table(df_frameloss_all, 'LAN Data')
        ])
        #print(AAA)
    else:
        raise PreventUpdate

