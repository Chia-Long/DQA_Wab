import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import ClientsideFunction, Input, Output, State
import pandas as pd
from app import app
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import time
#import os

#url = os.environ
#print("url"+url)

#duttest1 = str(url).split("/")
#print (duttest1[2])
# data
#duttest = "2020000111"
#pd_cpu = pd.read_csv('csv/SPECCPU2017.csv', index_col=1)


layout = html.Div([
    html.Div(id="systeminfo", style={'marginTop': '12px'}),
    html.P(id="counter",style={'display': 'block'}),dcc.Input(id="card1_msg",value="",style={'display': 'none'}),dcc.Input(id="lcard1_msg",value="",style={'display': 'none'}),dcc.Input(id="mcard1_msg",value="",style={'display': 'none'}),dcc.Input(id="scard1_msg",value="",style={'display': 'none'}),
    dcc.Input(id="card2_msg",value="",style={'display': 'none'}),dcc.Input(id="lcard2_msg",value="",style={'display': 'none'}),dcc.Input(id="mcard2_msg",value="",style={'display': 'none'}),dcc.Input(id="scard2_msg",value="",style={'display': 'none'}),dcc.Input(id="storage_msg",value="",style={'display': 'none'}),
    #,style={'display': 'none'})
])



@app.callback(
    Output("systeminfo", "children"), [Input('p0-url1', 'pathname')],
)
def display_page(pathname):
    if pathname is None:
        raise PreventUpdate
    elif '/apps/System_Information' in pathname:
        #print("pathname2")
        test_id = pathname.split("/")
        #print(AAA)
    else:
        raise PreventUpdate
        #print(pathname)
        # print (data)
        #print("pathname3")

    duttest = int(test_id[3])
    print(duttest)
    df1 = pd.read_csv('data/SPECCPU2017.csv', index_col="Test_ID")
    df2 = pd.read_csv('data/Storage_Performance.csv', index_col="Test_ID")
    df3 = pd.read_csv('data/MLC.csv', index_col="Test_ID")
    df4 = pd.read_csv('data/LAN_Performance.csv', index_col="Test_ID")
    check1 = df1.query("Test_ID==@duttest")
    check2 = df2.query("Test_ID==@duttest")
    check3 = df3.query("Test_ID==@duttest")
    check4 = df4.query("Test_ID==@duttest")

    if not check1.empty:
        select_data = df1.loc[[duttest]]
        testcase = "SPECCPU2017"
    elif not check2.empty:
        select_data = df2.loc[[duttest]]
        testcase = "RAID"
    elif not check3.empty:
        select_data = df3.loc[[duttest]]
        testcase = "MLC"
    elif not check4.empty:
        select_data = df4.loc[[duttest]]
        testcase = "LAN"
    else:
        return 404

    c1_cpu = select_data.at[duttest, 'CPU']
    c1_mem = select_data.at[duttest, 'Memory']
    c1_cpunum = select_data.at[duttest, 'CPU_#']
    c1_project = select_data.at[duttest, 'Product_Name']
    c2_memlo = select_data.at[duttest, 'Memory_Location']
    #print("c2_memlo"+str(c2_memlo))
    c1_memnum = len(c2_memlo.split(","))
    #print("c1_memnum"+str(c1_memnum))
    c1_testdata = select_data.at[duttest, 'Test_Date']
    s_project = pd.read_csv('data/component_project.csv', index_col="ID")
    select_project = s_project.loc[[c1_project]]
    product_name = select_project.at[c1_project, 'Product Name']

    ### c3 cpu ###
    s_cpu = pd.read_csv('data/component_cpu.csv', index_col="ID")
    select_cpu = s_cpu.loc[[c1_cpu]]
    code_Name = select_cpu.at[c1_cpu,'Code Name']
    processor_name = select_cpu.at[c1_cpu,'Processor Name']
    cores = select_cpu.at[c1_cpu,'# of cores']
    threads = select_cpu.at[c1_cpu,'# of threads']
    processor_base_frequency = select_cpu.at[c1_cpu,'Processor Base Frequency(GHz)']
    max_turbo_frequency = select_cpu.at[c1_cpu,'Max Turbo Frequency(GHz)']
    cache = select_cpu.at[c1_cpu,'Cache(MB)']
    tDP = select_cpu.at[c1_cpu,'TDP(W)']

    ## C3 mem ##
    memheader = ""
    s_mem = pd.read_csv('data/component_memory.csv', index_col="ID")
    select_mem = s_mem.loc[[c1_mem]]
    dimm_vendor = select_mem.at[c1_mem, 'DIMM Vendor']
    part_number = select_mem.at[c1_mem, 'Part Number']
    memory_types = select_mem.at[c1_mem, 'Memory Types']
    of_pin = select_mem.at[c1_mem, '# of Pin']
    ecc_support = select_mem.at[c1_mem, 'ECC Support']
    maximum_memory_speed = select_mem.at[c1_mem, 'Maximum Memory Speed']
    memory_size = select_mem.at[c1_mem, 'Memory Size(GB)']
    of_rank = select_mem.at[c1_mem, '# of Rank']
    ram_chip = select_mem.at[c1_mem,'RAM Chip']

    ## SPECCPU ##
    if testcase == "SPECCPU2017":
        # C2_cpu_list
        cpu0 = dbc.ListGroupItem("CPU0", id="b_c2_cpu0", n_clicks_timestamp="0", style={'display': 'none'})
        cpu1 = dbc.ListGroupItem("CPU1", id="b_c2_cpu1", n_clicks_timestamp="0", style={'display': 'none'})
        cpu2 = dbc.ListGroupItem("CPU2", id="b_c2_cpu2", n_clicks_timestamp="0", style={'display': 'none'})
        cpu3 = dbc.ListGroupItem("CPU3", id="b_c2_cpu3", n_clicks_timestamp="0", style={'display': 'none'})
        for i in range(int(c1_cpunum)):
            if i == 0:
                cpu0 = dbc.ListGroupItem("CPU0", id="b_c2_cpu0", n_clicks_timestamp="0", action=True, color="info")
            if i == 1:
                cpu1 = dbc.ListGroupItem("CPU1", id="b_c2_cpu1", n_clicks_timestamp="0", action=True, color="info")
            if i == 2:
                cpu2 = dbc.ListGroupItem("CPU2", id="b_c2_cpu2", n_clicks_timestamp="0", action=True, color="info")
            if i == 3:
                cpu3 = dbc.ListGroupItem("CPU3", id="b_c2_cpu3", n_clicks_timestamp="0", action=True, color="info")

        # C2 mem list
        if "A1" in c2_memlo:
            memA1 = dbc.ListGroupItem("DIMM A1", id="b_c2_A1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memA1 = dbc.ListGroupItem("DIMM A1", id="b_c2_A1", n_clicks_timestamp="0", style={'display': 'none'})
        if "A2" in c2_memlo:
            memA2 = dbc.ListGroupItem("DIMM A2", id="b_c2_A2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memA2 = dbc.ListGroupItem("DIMM A2", id="b_c2_A2", n_clicks_timestamp="0", style={'display': 'none'})
        if "B1" in c2_memlo:
            memB1 = dbc.ListGroupItem("DIMM B1", id="b_c2_B1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memB1 = dbc.ListGroupItem("DIMM B1", id="b_c2_B1", n_clicks_timestamp="0", style={'display': 'none'})
        if "B2" in c2_memlo:
            memB2 = dbc.ListGroupItem("DIMM B2", id="b_c2_B2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memB2 = dbc.ListGroupItem("DIMM B2", id="b_c2_B2", n_clicks_timestamp="0", style={'display': 'none'})
        if "C1" in c2_memlo:
            memC1 = dbc.ListGroupItem("DIMM C1", id="b_c2_C1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memC1 = dbc.ListGroupItem("DIMM C1", id="b_c2_C1", n_clicks_timestamp="0", style={'display': 'none'})
        if "C2" in c2_memlo:
            memC2 = dbc.ListGroupItem("DIMM C2", id="b_c2_C2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memC2 = dbc.ListGroupItem("DIMM C2", id="b_c2_C2", n_clicks_timestamp="0", style={'display': 'none'})
        if "D1" in c2_memlo:
            memD1 = dbc.ListGroupItem("DIMM D1", id="b_c2_D1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memD1 = dbc.ListGroupItem("DIMM D1", id="b_c2_D1", n_clicks_timestamp="0", style={'display': 'none'})
        if "D2" in c2_memlo:
            memD2 = dbc.ListGroupItem("DIMM D2", id="b_c2_D2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memD2 = dbc.ListGroupItem("DIMM D2", id="b_c2_D2", n_clicks_timestamp="0", style={'display': 'none'})
        if "E1" in c2_memlo:
            memE1 = dbc.ListGroupItem("DIMM E1", id="b_c2_E1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memE1 = dbc.ListGroupItem("DIMM E1", id="b_c2_E1", n_clicks_timestamp="0", style={'display': 'none'})
        if "E2" in c2_memlo:
            memE2 = dbc.ListGroupItem("DIMM E2", id="b_c2_E2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memE2 = dbc.ListGroupItem("DIMM E2", id="b_c2_E2", n_clicks_timestamp="0", style={'display': 'none'})
        if "F1" in c2_memlo:
            memF1 = dbc.ListGroupItem("DIMM F1", id="b_c2_F1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memF1 = dbc.ListGroupItem("DIMM F1", id="b_c2_F1", n_clicks_timestamp="0", style={'display': 'none'})
        if "F2" in c2_memlo:
            memF2 = dbc.ListGroupItem("DIMM F2", id="b_c2_F2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memF2 = dbc.ListGroupItem("DIMM F2", id="b_c2_F2", n_clicks_timestamp="0", style={'display': 'none'})
        if "G1" in c2_memlo:
            memG1 = dbc.ListGroupItem("DIMM G1", id="b_c2_G1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memG1 = dbc.ListGroupItem("DIMM G1", id="b_c2_G1", n_clicks_timestamp="0", style={'display': 'none'})
        if "G2" in c2_memlo:
            memG2 = dbc.ListGroupItem("DIMM G2", id="b_c2_G2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memG2 = dbc.ListGroupItem("DIMM G2", id="b_c2_G2", n_clicks_timestamp="0", style={'display': 'none'})
        if "H1" in c2_memlo:
            memH1 = dbc.ListGroupItem("DIMM H1", id="b_c2_H1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memH1 = dbc.ListGroupItem("DIMM H1", id="b_c2_H1", n_clicks_timestamp="0", style={'display': 'none'})
        if "H2" in c2_memlo:
            memH2 = dbc.ListGroupItem("DIMM H2", id="b_c2_H2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memH2 = dbc.ListGroupItem("DIMM H2", id="b_c2_H2", n_clicks_timestamp="0", style={'display': 'none'})
        if "J1" in c2_memlo:
            memJ1 = dbc.ListGroupItem("DIMM J1", id="b_c2_J1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memJ1 = dbc.ListGroupItem("DIMM J1", id="b_c2_J1", n_clicks_timestamp="0", style={'display': 'none'})
        if "J2" in c2_memlo:
            memJ2 = dbc.ListGroupItem("DIMM J2", id="b_c2_J2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memJ2 = dbc.ListGroupItem("DIMM J2", id="b_c2_J2", n_clicks_timestamp="0", style={'display': 'none'})
        if "K1" in c2_memlo:
            memK1 = dbc.ListGroupItem("DIMM K1", id="b_c2_K1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memK1 = dbc.ListGroupItem("DIMM K1", id="b_c2_K1", n_clicks_timestamp="0", style={'display': 'none'})
        if "K2" in c2_memlo:
            memK2 = dbc.ListGroupItem("DIMM K2", id="b_c2_K2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memK2 = dbc.ListGroupItem("DIMM K2", id="b_c2_K2", n_clicks_timestamp="0", style={'display': 'none'})
        if "L1" in c2_memlo:
            memL1 = dbc.ListGroupItem("DIMM L1", id="b_c2_L1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memL1 = dbc.ListGroupItem("DIMM L1", id="b_c2_L1", n_clicks_timestamp="0", style={'display': 'none'})
        if "L2" in c2_memlo:
            memL2 = dbc.ListGroupItem("DIMM L2", id="b_c2_L2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memL2 = dbc.ListGroupItem("DIMM L2", id="b_c2_L2", n_clicks_timestamp="0", style={'display': 'none'})
        if "M1" in c2_memlo:
            memM1 = dbc.ListGroupItem("DIMM M1", id="b_c2_M1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memM1 = dbc.ListGroupItem("DIMM M1", id="b_c2_M1", n_clicks_timestamp="0", style={'display': 'none'})
        if "M2" in c2_memlo:
            memM2 = dbc.ListGroupItem("DIMM M2", id="b_c2_M2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memM2 = dbc.ListGroupItem("DIMM M2", id="b_c2_M2", n_clicks_timestamp="0", style={'display': 'none'})
        #c1_cpu = select_data.at[duttest,'CPU']
        #c1_mem = select_data.at[duttest,'Memory']
        c1_storage = select_data.at[duttest,'Storage_Model']
        #c1_cpunum = select_data.at[duttest, 'CPU #']
        #c1_project = select_data.at[duttest,'Product Name']
        #c2_memlo = select_data.at[duttest, 'Memory Location'].split(",")
        #c1_memnum = len(c2_memlo)
        c1_storagenum = select_data.at[duttest, 'Storage_Number']
        #c1_testdata = select_data.at[duttest, 'Test Date']
        #s_project = pd.read_csv('csv/component_project.csv', index_col="ID")
        #select_project = s_project.loc[[c1_project]]
        #product_name = select_project.at[c1_project,'Product Name']
        c1_topology = select_data.at[duttest, 'Topology']
        if c1_topology == "Ring":
            topology = dbc.ListGroupItem(c1_topology, id="c1_topology", n_clicks_timestamp="0")
        elif c1_topology == "Star":
            topology = dbc.ListGroupItem(c1_topology, id="c1_topology", n_clicks_timestamp="0")
        else:
            topology = dbc.ListGroupItem(c1_topology, id="c1_topology", n_clicks_timestamp="0", style={'display': 'none'})
        #C2_storage_list
        c1_storagetype = select_data.at[duttest, 'Form_Factor']

        if c1_storagetype == "nan":
            c1l_storage = dbc.ListGroupItem(str(c1_storagetype) + " : " + str(int(c1_storagenum)), id="b_c2_nvmessdm2",
                                            n_clicks_timestamp="0", style={'display': 'none'})
        else:
            c1l_storage = dbc.ListGroupItem(str(c1_storagetype) + " : " + str(int(c1_storagenum)), id="b_c2_nvmessdm2",
                                            n_clicks_timestamp="0", action=True, color="info")

        #nvmessdm2 = dbc.ListGroupItem("M.2 NVMe SSD", id="b_c2_nvmessdm2",  n_clicks_timestamp="0", style={'display': 'none'})
        #satassdm2 = dbc.ListGroupItem("M.2 SATA SSD", id="b_c2_satassdm2", n_clicks_timestamp="0",style={'display': 'none'})
        #nvmessd25 = dbc.ListGroupItem("2.5\" NVMe SSD", id="b_c2_nvmessd25",n_clicks_timestamp="0", style={'display': 'none'})
        #satassd25 = dbc.ListGroupItem("2.5\" SATA SSD", id="b_c2_satassd25", n_clicks_timestamp="0",style={'display': 'none'})
        #satahdd25 = dbc.ListGroupItem("2.5\" SATA HDD", id="b_c2_satahdd25", n_clicks_timestamp="0",style={'display': 'none'})
        #satahdd35 = dbc.ListGroupItem("3.5\" SATA HDD", id="b_c2_satahdd35", n_clicks_timestamp="0",style={'display': 'none'})
        #pciecardssd = dbc.ListGroupItem("PCIe card SSD", id="b_c2_pciecardssd", n_clicks_timestamp="0",style={'display': 'none'})
        #if c2_storagetype == "M.2 NVMe SSD":
        #    nvmessdm2 = dbc.ListGroupItem("M.2 NVMe SSD: "+str(c1_storagenum), id="b_c2_nvmessdm2", n_clicks_timestamp="0", action=True, color="info")
        #if c2_storagetype == "M.2 SATA SSD":
        #    satassdm2 = dbc.ListGroupItem("M.2 SATA SSD: "+str(c1_storagenum), id="b_c2_satassdm2", n_clicks_timestamp="0", action=True, color="info")
        #if c2_storagetype == "2.5\" NVMe SSD":
        #    nvmessd25 = dbc.ListGroupItem("2.5\" NVMe SSD: "+str(c1_storagenum), id="b_c2_nvmessd25", n_clicks_timestamp="0", action=True, color="info")
        #if c2_storagetype == "2.5\" SATA SSD":
        #    satassd25 = dbc.ListGroupItem("2.5\" SATA SSD: "+str(c1_storagenum), id="b_c2_satassd25", n_clicks_timestamp="0", action=True, color="info")
        #if c2_storagetype == "2.5\" SATA HDD":
        #    satahdd25 = dbc.ListGroupItem("2.5\" SATA HDD: "+str(c1_storagenum), id="b_c2_satahdd25", n_clicks_timestamp="0", action=True, color="info")
        #if c2_storagetype == "3.5\" SATA HDD":
        #    satahdd35 = dbc.ListGroupItem("3.5\" SATA HDD: "+str(c1_storagenum), id="b_c2_satahdd35", n_clicks_timestamp="0", action=True, color="info")
        #if c2_storagetype == "PCIe card SSD":
        #    pciecardssd = dbc.ListGroupItem("PCIe card SSD: "+str(c1_storagenum), id="b_c2_pciecardssd", n_clicks_timestamp="0", action=True, color="info")
        ## C3 storage ##
        s_storage = pd.read_csv('data/component_storage.csv', index_col="ID")
        select_storage = s_storage.loc[[c1_storage]]
        storage_vendor = select_storage.at[c1_storage,'Storage Vendor']
        storage_model_name = select_storage.at[c1_storage,'Storage Model Name']
        form_factor = select_storage.at[c1_storage,'Form Factor']
        storage_interface = select_storage.at[c1_storage,'Storage Interface']
        storage_capacity = select_storage.at[c1_storage,'Storage Capacity']
        media_components = select_storage.at[c1_storage,'Media / Components']
        power_consumption = select_storage.at[c1_storage,'Power Consumption(W)']
        c3_configspeed = select_data.at[duttest, 'I/O_Type_Bus_Speed']
        first_col = html.Div([

            dbc.Card(
            dbc.ListGroup(
                [
                    dbc.ListGroupItemHeading("System Information"),
                    dbc.ListGroupItem(product_name),
                    dbc.ListGroupItem("CPU", id="b_c1_cpu", n_clicks_timestamp="0", action=True, color="info"),
                    dbc.ListGroupItem("CPU number: "+str(int(c1_cpunum))),
                    topology,
                    dbc.ListGroupItem("DIMM", id="b_c1_mem", n_clicks_timestamp="0", action=True, color="info"),
                    dbc.ListGroupItem("DIMM number: "+str(int(c1_memnum))),
                    dbc.ListGroupItem("Storage Device Category ", id="b_c1_stg", n_clicks_timestamp="0", action=True, color="info"),
                    dbc.ListGroupItem(c1_testdata),
                ],
                flush=True,
            )
        ),
        ])

        second_col = html.Div([

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("CPU"),
                            cpu0,cpu1,cpu2,cpu3
                        ],
                        flush=True,
                    ),
                ),
                id="cpufade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("Memory DIMM"),
                            memA1, memA2, memB1, memB2, memC1, memC2, memD1, memD2, memE1, memE2, memF1, memF2,
                            memG1, memG2, memH1, memH2, memJ1, memJ2, memK1, memK2, memL1, memL2, memM1, memM2,
                        ],
                        flush=True,
                    ),
                ),
                id="memfade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("Storage Device Category"),
                            c1l_storage,
                            #nvmessdm2,
                            #satassdm2,
                            #nvmessd25,
                            #satassd25,
                            #satahdd25,
                            #satahdd35,
                            #pciecardssd,
                        ],
                        flush=True,
                    ),
                ),
                id="storagefade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),


        ])

        third_col = html.Div([

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            #dbc.ListGroupItemHeading("aaaa"),
                            dbc.ListGroupItemHeading(id="cardheader_C"),
                            dbc.ListGroupItem("Code Name: "+str(code_Name)),
                            dbc.ListGroupItem("Processor Name: "+str(processor_name)),
                            dbc.ListGroupItem("Cores: "+str(int(cores))),
                            dbc.ListGroupItem("# of threads: "+str(int(threads))),
                            dbc.ListGroupItem("Processor Base Frequency: "+str(processor_base_frequency)+" GHz"),
                            dbc.ListGroupItem("Max Turbo Frequency: "+str(max_turbo_frequency)+" GHz"),
                            dbc.ListGroupItem("Cache: "+str(cache)+" MB"),
                            dbc.ListGroupItem("TDP: "+str(tDP)+" W"),
                        ],
                        flush=True,
                    ),
                ),
                id="c3_cpufade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(id="cardheader_M"),
                            dbc.ListGroupItem("DIMM Vendor: "+str(dimm_vendor)),
                            dbc.ListGroupItem("Part Number: "+str(part_number)),
                            dbc.ListGroupItem("Memory Types: "+str(memory_types)),
                            dbc.ListGroupItem("# of Pin: "+str(int(of_pin))),
                            dbc.ListGroupItem("ECC Support: "+str(ecc_support)),
                            dbc.ListGroupItem("Maximum Memory Speed: "+str(int(maximum_memory_speed))+" MHz"),
                            dbc.ListGroupItem("Memory Size: "+str(int(memory_size))+" GB"),
                            dbc.ListGroupItem("# of Rank: " + str(of_rank)),
                            dbc.ListGroupItem("RAM_Chip: " + str(ram_chip)),
                        ],
                        flush=True,
                    ),
                ),
                id="c3_memfade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(id="cardheader_S"),
                            dbc.ListGroupItem("Storage Vendor: "+str(storage_vendor)),
                            dbc.ListGroupItem("Storage Model Name: "+str(storage_model_name)),
                            dbc.ListGroupItem("Form Factor: "+str(form_factor)),
                            dbc.ListGroupItem("Storage Interface: "+str(storage_interface)),
                            dbc.ListGroupItem("Storage Capacity: "+str(storage_capacity)),
                            dbc.ListGroupItem("Media / Components: "+str(media_components)),
                            dbc.ListGroupItem("Power Consumption: "+str(power_consumption)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c3_configspeed)),
                        ],
                        flush=True,
                    ),
                ),
                id="c3_storagefade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),

        ])
    elif testcase == "RAID":
        print("RAID")
        # C2_cpu_list
        cpu0 = dbc.ListGroupItem("CPU0", id="sb_c2_cpu0", n_clicks_timestamp="0", style={'display': 'none'})
        cpu1 = dbc.ListGroupItem("CPU1", id="sb_c2_cpu1", n_clicks_timestamp="0", style={'display': 'none'})
        cpu2 = dbc.ListGroupItem("CPU2", id="sb_c2_cpu2", n_clicks_timestamp="0", style={'display': 'none'})
        cpu3 = dbc.ListGroupItem("CPU3", id="sb_c2_cpu3", n_clicks_timestamp="0", style={'display': 'none'})
        for i in range(int(c1_cpunum)):
            if i == 0:
                cpu0 = dbc.ListGroupItem("CPU0", id="sb_c2_cpu0", n_clicks_timestamp="0", action=True, color="info")
            if i == 1:
                cpu1 = dbc.ListGroupItem("CPU1", id="sb_c2_cpu1", n_clicks_timestamp="0", action=True, color="info")
            if i == 2:
                cpu2 = dbc.ListGroupItem("CPU2", id="sb_c2_cpu2", n_clicks_timestamp="0", action=True, color="info")
            if i == 3:
                cpu3 = dbc.ListGroupItem("CPU3", id="sb_c2_cpu3", n_clicks_timestamp="0", action=True, color="info")

        # C2 mem list
        if "A1" in c2_memlo:
            memA1 = dbc.ListGroupItem("DIMM A1", id="sb_c2_A1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memA1 = dbc.ListGroupItem("DIMM A1", id="sb_c2_A1", n_clicks_timestamp="0", style={'display': 'none'})
        if "A2" in c2_memlo:
            memA2 = dbc.ListGroupItem("DIMM A2", id="sb_c2_A2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memA2 = dbc.ListGroupItem("DIMM A2", id="sb_c2_A2", n_clicks_timestamp="0", style={'display': 'none'})
        if "B1" in c2_memlo:
            memB1 = dbc.ListGroupItem("DIMM B1", id="sb_c2_B1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memB1 = dbc.ListGroupItem("DIMM B1", id="sb_c2_B1", n_clicks_timestamp="0", style={'display': 'none'})
        if "B2" in c2_memlo:
            memB2 = dbc.ListGroupItem("DIMM B2", id="sb_c2_B2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memB2 = dbc.ListGroupItem("DIMM B2", id="sb_c2_B2", n_clicks_timestamp="0", style={'display': 'none'})
        if "C1" in c2_memlo:
            memC1 = dbc.ListGroupItem("DIMM C1", id="sb_c2_C1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memC1 = dbc.ListGroupItem("DIMM C1", id="sb_c2_C1", n_clicks_timestamp="0", style={'display': 'none'})
        if "C2" in c2_memlo:
            memC2 = dbc.ListGroupItem("DIMM C2", id="sb_c2_C2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memC2 = dbc.ListGroupItem("DIMM C2", id="sb_c2_C2", n_clicks_timestamp="0", style={'display': 'none'})
        if "D1" in c2_memlo:
            memD1 = dbc.ListGroupItem("DIMM D1", id="sb_c2_D1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memD1 = dbc.ListGroupItem("DIMM D1", id="sb_c2_D1", n_clicks_timestamp="0", style={'display': 'none'})
        if "D2" in c2_memlo:
            memD2 = dbc.ListGroupItem("DIMM D2", id="sb_c2_D2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memD2 = dbc.ListGroupItem("DIMM D2", id="sb_c2_D2", n_clicks_timestamp="0", style={'display': 'none'})
        if "E1" in c2_memlo:
            memE1 = dbc.ListGroupItem("DIMM E1", id="sb_c2_E1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memE1 = dbc.ListGroupItem("DIMM E1", id="sb_c2_E1", n_clicks_timestamp="0", style={'display': 'none'})
        if "E2" in c2_memlo:
            memE2 = dbc.ListGroupItem("DIMM E2", id="sb_c2_E2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memE2 = dbc.ListGroupItem("DIMM E2", id="sb_c2_E2", n_clicks_timestamp="0", style={'display': 'none'})
        if "F1" in c2_memlo:
            memF1 = dbc.ListGroupItem("DIMM F1", id="sb_c2_F1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memF1 = dbc.ListGroupItem("DIMM F1", id="sb_c2_F1", n_clicks_timestamp="0", style={'display': 'none'})
        if "F2" in c2_memlo:
            memF2 = dbc.ListGroupItem("DIMM F2", id="sb_c2_F2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memF2 = dbc.ListGroupItem("DIMM F2", id="sb_c2_F2", n_clicks_timestamp="0", style={'display': 'none'})
        if "G1" in c2_memlo:
            memG1 = dbc.ListGroupItem("DIMM G1", id="sb_c2_G1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memG1 = dbc.ListGroupItem("DIMM G1", id="sb_c2_G1", n_clicks_timestamp="0", style={'display': 'none'})
        if "G2" in c2_memlo:
            memG2 = dbc.ListGroupItem("DIMM G2", id="sb_c2_G2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memG2 = dbc.ListGroupItem("DIMM G2", id="sb_c2_G2", n_clicks_timestamp="0", style={'display': 'none'})
        if "H1" in c2_memlo:
            memH1 = dbc.ListGroupItem("DIMM H1", id="sb_c2_H1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memH1 = dbc.ListGroupItem("DIMM H1", id="sb_c2_H1", n_clicks_timestamp="0", style={'display': 'none'})
        if "H2" in c2_memlo:
            memH2 = dbc.ListGroupItem("DIMM H2", id="sb_c2_H2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memH2 = dbc.ListGroupItem("DIMM H2", id="sb_c2_H2", n_clicks_timestamp="0", style={'display': 'none'})
        if "J1" in c2_memlo:
            memJ1 = dbc.ListGroupItem("DIMM J1", id="sb_c2_J1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memJ1 = dbc.ListGroupItem("DIMM J1", id="sb_c2_J1", n_clicks_timestamp="0", style={'display': 'none'})
        if "J2" in c2_memlo:
            memJ2 = dbc.ListGroupItem("DIMM J2", id="sb_c2_J2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memJ2 = dbc.ListGroupItem("DIMM J2", id="sb_c2_J2", n_clicks_timestamp="0", style={'display': 'none'})
        if "K1" in c2_memlo:
            memK1 = dbc.ListGroupItem("DIMM K1", id="sb_c2_K1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memK1 = dbc.ListGroupItem("DIMM K1", id="sb_c2_K1", n_clicks_timestamp="0", style={'display': 'none'})
        if "K2" in c2_memlo:
            memK2 = dbc.ListGroupItem("DIMM K2", id="sb_c2_K2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memK2 = dbc.ListGroupItem("DIMM K2", id="sb_c2_K2", n_clicks_timestamp="0", style={'display': 'none'})
        if "L1" in c2_memlo:
            memL1 = dbc.ListGroupItem("DIMM L1", id="sb_c2_L1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memL1 = dbc.ListGroupItem("DIMM L1", id="sb_c2_L1", n_clicks_timestamp="0", style={'display': 'none'})
        if "L2" in c2_memlo:
            memL2 = dbc.ListGroupItem("DIMM L2", id="sb_c2_L2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memL2 = dbc.ListGroupItem("DIMM L2", id="sb_c2_L2", n_clicks_timestamp="0", style={'display': 'none'})
        if "M1" in c2_memlo:
            memM1 = dbc.ListGroupItem("DIMM M1", id="sb_c2_M1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memM1 = dbc.ListGroupItem("DIMM M1", id="sb_c2_M1", n_clicks_timestamp="0", style={'display': 'none'})
        if "M2" in c2_memlo:
            memM2 = dbc.ListGroupItem("DIMM M2", id="sb_c2_M2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memM2 = dbc.ListGroupItem("DIMM M2", id="sb_c2_M2", n_clicks_timestamp="0", style={'display': 'none'})

        # = select_data.at[duttest, 'Topology']
        #if c1_topology == "Ring":
        #    topology = dbc.ListGroupItem("Ring")
        #elif c1_topology == "Star":
        #    topology = dbc.ListGroupItem("Star")
        #else:
         #   topology = dbc.ListGroupItem("", style={'display': 'none'})

        s_storage = pd.read_csv('data/component_storage.csv', index_col="ID")

        ##### _storage_list 1 #####
        FF1 = pd.isnull(select_data['Form_Factor_1'].iloc[0])
        #c2_storage1 = dbc.ListGroupItem("N/A", id="sb_c2_storage1",n_clicks_timestamp="0", style={'display': 'none'})
        if FF1 is True:
            c2_storage1 = dbc.ListGroupItem("N/A", id="sb_c2_storage1",n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype1 = " "
            c2_storagemodel1 = " "
            c2_storagenum1 = " "
            c2_storagespeed1 = " "
            select_storage1 = " "
            storage_vendor1 = " "
            storage_model_name1 = " "
            form_factor1 = " "
            storage_interface1 = " "
            storage_capacity1 = " "
            media_components1 = " "
            power_consumption1 = " "
        else:
            c2_storagetype1 = select_data.at[duttest, 'Form_Factor_1']
            c2_storagemodel1 = select_data.at[duttest, 'Storage_Model_1']
            c2_storagenum1 = select_data.at[duttest, 'Storage_Number_1']
            c2_storagespeed1 = select_data.at[duttest, 'I/O_Type_Bus_Speed_1']
            select_storage1 = s_storage.loc[[c2_storagemodel1]]
            storage_vendor1 = select_storage1.at[c2_storagemodel1, 'Storage Vendor']
            storage_model_name1 = select_storage1.at[c2_storagemodel1, 'Storage Model Name']
            form_factor1 = select_storage1.at[c2_storagemodel1, 'Form Factor']
            storage_interface1 = select_storage1.at[c2_storagemodel1, 'Storage Interface']
            storage_capacity1 = select_storage1.at[c2_storagemodel1, 'Storage Capacity']
            media_components1 = select_storage1.at[c2_storagemodel1, 'Media / Components']
            power_consumption1 = select_storage1.at[c2_storagemodel1, 'Power Consumption(W)']
            c2_storage1 = dbc.ListGroupItem(str(c2_storagetype1) + " : " + str(int(c2_storagenum1)),id="sb_c2_storage1",n_clicks_timestamp="0", action=True, color="info")

        ##### _storage_list 1 #####

        ##### _storage_list 2 #####
        FF2 = pd.isnull(select_data['Form_Factor_2'].iloc[0])
        if FF2 is True:
            c2_storage2 = dbc.ListGroupItem("N/A", id="sb_c2_storage2",
                                            n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype2 = " "
            c2_storagemodel2 = " "
            c2_storagenum2 = " "
            c2_storagespeed2 = " "
            select_storage2 = " "
            storage_vendor2 = " "
            storage_model_name2 = " "
            form_factor2 = " "
            storage_interface2 = " "
            storage_capacity2 = " "
            media_components2 = " "
            power_consumption2 = " "
        else:
            c2_storagetype2 = select_data.at[duttest, 'Form_Factor_2']
            c2_storagemodel2 = select_data.at[duttest, 'Storage_Model_2']
            c2_storagenum2 = select_data.at[duttest, 'Storage_Number_2']
            c2_storagespeed2 = select_data.at[duttest, 'I/O_Type_Bus_Speed_2']
            select_storage2 = s_storage.loc[[c2_storagemodel2]]
            storage_vendor2 = select_storage2.at[c2_storagemodel2, 'Storage Vendor']
            storage_model_name2 = select_storage2.at[c2_storagemodel2, 'Storage Model Name']
            form_factor2 = select_storage2.at[c2_storagemodel2, 'Form Factor']
            storage_interface2 = select_storage2.at[c2_storagemodel2, 'Storage Interface']
            storage_capacity2 = select_storage2.at[c2_storagemodel2, 'Storage Capacity']
            media_components2 = select_storage2.at[c2_storagemodel2, 'Media / Components']
            power_consumption2 = select_storage2.at[c2_storagemodel2, 'Power Consumption(W)']
            c2_storage2 = dbc.ListGroupItem(str(c2_storagetype2) + " : " + str(int(c2_storagenum2)),
                                            id="sb_c2_storage2",
                                            n_clicks_timestamp="0", action=True, color="info")

        ##### _storage_list 2 #####

        ##### _storage_list 3 #####
        FF3 = pd.isnull(select_data['Form_Factor_3'].iloc[0])
        if FF3 is True:
            c2_storage3 = dbc.ListGroupItem("N/A", id="sb_c2_storage3",
                                            n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype3 = " "
            c2_storagemodel3 = " "
            c2_storagenum3 = " "
            c2_storagespeed3 = " "
            select_storage3 = " "
            storage_vendor3 = " "
            storage_model_name3 = " "
            form_factor3 = " "
            storage_interface3 = " "
            storage_capacity3 = " "
            media_components3 = " "
            power_consumption3 = " "
        else:
            c2_storagetype3 = select_data.at[duttest, 'Form_Factor_3']
            c2_storagemodel3 = select_data.at[duttest, 'Storage_Model_3']
            c2_storagenum3 = select_data.at[duttest, 'Storage_Number_3']
            c2_storagespeed3 = select_data.at[duttest, 'I/O_Type_Bus_Speed_3']
            select_storage3 = s_storage.loc[[c2_storagemodel3]]
            storage_vendor3 = select_storage3.at[c2_storagemodel3, 'Storage Vendor']
            storage_model_name3 = select_storage3.at[c2_storagemodel3, 'Storage Model Name']
            form_factor3 = select_storage3.at[c2_storagemodel3, 'Form Factor']
            storage_interface3 = select_storage3.at[c2_storagemodel3, 'Storage Interface']
            storage_capacity3 = select_storage3.at[c2_storagemodel3, 'Storage Capacity']
            media_components3 = select_storage3.at[c2_storagemodel3, 'Media / Components']
            power_consumption3 = select_storage3.at[c2_storagemodel3, 'Power Consumption(W)']
            c2_storage3 = dbc.ListGroupItem(str(c2_storagetype3) + " : " + str(int(c2_storagenum3)), id="sb_c2_storage3",
                                            n_clicks_timestamp="0", action=True, color="info")
        ##### _storage_list 3 #####

        ##### _storage_list 4 #####
        FF4 = pd.isnull(select_data['Form_Factor_4'].iloc[0])
        if FF4 is True:
            c2_storage4 = dbc.ListGroupItem("N/A", id="sb_c2_storage4",
                                            n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype4 = " "
            c2_storagemodel4 = " "
            c2_storagenum4 = " "
            c2_storagespeed4 = " "
            select_storage4 = " "
            storage_vendor4 = " "
            storage_model_name4 = " "
            form_factor4 = " "
            storage_interface4 = " "
            storage_capacity4 = " "
            media_components4 = " "
            power_consumption4 = " "
        else:
            c2_storagetype4 = select_data.at[duttest, 'Form_Factor_4']
            c2_storagemodel4 = select_data.at[duttest, 'Storage_Model_4']
            c2_storagenum4 = select_data.at[duttest, 'Storage_Number_4']
            c2_storagespeed4 = select_data.at[duttest, 'I/O_Type_Bus_Speed_4']
            select_storage4 = s_storage.loc[[c2_storagemodel4]]
            storage_vendor4 = select_storage4.at[c2_storagemodel4, 'Storage Vendor']
            storage_model_name4 = select_storage4.at[c2_storagemodel4, 'Storage Model Name']
            form_factor4 = select_storage4.at[c2_storagemodel4, 'Form Factor']
            storage_interface4 = select_storage4.at[c2_storagemodel4, 'Storage Interface']
            storage_capacity4 = select_storage4.at[c2_storagemodel4, 'Storage Capacity']
            media_components4 = select_storage4.at[c2_storagemodel4, 'Media / Components']
            power_consumption4 = select_storage4.at[c2_storagemodel4, 'Power Consumption(W)']
            c2_storage4 = dbc.ListGroupItem(str(c2_storagetype4) + " : " + str(int(c2_storagenum4)),
                                            id="sb_c2_storage4",
                                            n_clicks_timestamp="0", action=True, color="info")
        ##### _storage_list 4 #####
        ##### _storage_list 5 #####
        FF5 = pd.isnull(select_data['Form_Factor_5'].iloc[0])
        if FF5 is True:
            c2_storage5 = dbc.ListGroupItem("N/A", id="sb_c2_storage5",
                                            n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype5 = " "
            c2_storagemodel5 = " "
            c2_storagenum5 = " "
            c2_storagespeed5 = " "
            select_storage5 = " "
            storage_vendor5 = " "
            storage_model_name5 = " "
            form_factor5 = " "
            storage_interface5 = " "
            storage_capacity5 = " "
            media_components5 = " "
            power_consumption5 = " "
        else:
            c2_storagetype5 = select_data.at[duttest, 'Form_Factor_5']
            c2_storagemodel5 = select_data.at[duttest, 'Storage_Model_5']
            c2_storagenum5 = select_data.at[duttest, 'Storage_Number_5']
            c2_storagespeed5 = select_data.at[duttest, 'I/O_Type_Bus_Speed_5']
            select_storage5 = s_storage.loc[[c2_storagemodel5]]
            storage_vendor5 = select_storage5.at[c2_storagemodel5, 'Storage Vendor']
            storage_model_name5 = select_storage5.at[c2_storagemodel5, 'Storage Model Name']
            form_factor5 = select_storage5.at[c2_storagemodel5, 'Form Factor']
            storage_interface5 = select_storage5.at[c2_storagemodel5, 'Storage Interface']
            storage_capacity5 = select_storage5.at[c2_storagemodel5, 'Storage Capacity']
            media_components5 = select_storage5.at[c2_storagemodel5, 'Media / Components']
            power_consumption5 = select_storage5.at[c2_storagemodel5, 'Power Consumption(W)']
            c2_storage5 = dbc.ListGroupItem(str(c2_storagetype5) + " : " + str(int(c2_storagenum5)), id="sb_c2_storage5",
                                            n_clicks_timestamp="0", action=True, color="info")
        ##### _storage_list 5 #####
        ##### _storage_list 6 #####
        FF6 = pd.isnull(select_data['Form_Factor_6'].iloc[0])
        if FF6 is True:
            c2_storage6 = dbc.ListGroupItem("N/A", id="sb_c2_storage6",
                                            n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype6 = " "
            c2_storagemodel6 = " "
            c2_storagenum6 = " "
            c2_storagespeed6 = " "
            select_storage6 = " "
            storage_vendor6 = " "
            storage_model_name6 = " "
            form_factor6 = " "
            storage_interface6 = " "
            storage_capacity6 = " "
            media_components6 = " "
            power_consumption6 = " "
        else:
            c2_storagetype6 = select_data.at[duttest, 'Form_Factor_6']
            c2_storagemodel6 = select_data.at[duttest, 'Storage_Model_6']
            c2_storagenum6 = select_data.at[duttest, 'Storage_Number_6']
            c2_storagespeed6 = select_data.at[duttest, 'I/O_Type_Bus_Speed_6']
            select_storage6 = s_storage.loc[[c2_storagemodel6]]
            storage_vendor6 = select_storage6.at[c2_storagemodel6, 'Storage Vendor']
            storage_model_name6 = select_storage6.at[c2_storagemodel6, 'Storage Model Name']
            form_factor6 = select_storage6.at[c2_storagemodel6, 'Form Factor']
            storage_interface6 = select_storage6.at[c2_storagemodel6, 'Storage Interface']
            storage_capacity6 = select_storage6.at[c2_storagemodel6, 'Storage Capacity']
            media_components6 = select_storage6.at[c2_storagemodel6, 'Media / Components']
            power_consumption6 = select_storage6.at[c2_storagemodel6, 'Power Consumption(W)']
            c2_storage6 = dbc.ListGroupItem(str(c2_storagetype6) + " : " + str(int(c2_storagenum6)),
                                            id="sb_c2_storage6",
                                            n_clicks_timestamp="0", action=True, color="info")
        ##### _storage_list 6 #####
        ##### _storage_list 7 #####
        FF7 = pd.isnull(select_data['Form_Factor_7'].iloc[0])
        if FF7 is True:
            c2_storage7 = dbc.ListGroupItem("N/A", id="sb_c2_storage7",
                                            n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype7 = " "
            c2_storagemodel7 = " "
            c2_storagenum7 = " "
            c2_storagespeed7 = " "
            select_storage7 = " "
            storage_vendor7 = " "
            storage_model_name7 = " "
            form_factor7 = " "
            storage_interface7 = " "
            storage_capacity7 = " "
            media_components7 = " "
            power_consumption7 = " "
        else:
            c2_storagetype7 = select_data.at[duttest, 'Form_Factor_7']
            c2_storagemodel7 = select_data.at[duttest, 'Storage_Model_7']
            c2_storagenum7 = select_data.at[duttest, 'Storage_Number_7']
            c2_storagespeed7 = select_data.at[duttest, 'I/O_Type_Bus_Speed_7']
            select_storage7 = s_storage.loc[[c2_storagemodel7]]
            storage_vendor7 = select_storage7.at[c2_storagemodel7, 'Storage Vendor']
            storage_model_name7 = select_storage7.at[c2_storagemodel7, 'Storage Model Name']
            form_factor7 = select_storage7.at[c2_storagemodel7, 'Form Factor']
            storage_interface7 = select_storage7.at[c2_storagemodel7, 'Storage Interface']
            storage_capacity7 = select_storage7.at[c2_storagemodel7, 'Storage Capacity']
            media_components7 = select_storage7.at[c2_storagemodel7, 'Media / Components']
            power_consumption7 = select_storage7.at[c2_storagemodel7, 'Power Consumption(W)']
            c2_storage7 = dbc.ListGroupItem(str(c2_storagetype7) + " : " + str(int(c2_storagenum7)), id="sb_c2_storage7",
                                            n_clicks_timestamp="0", action=True, color="info")
            ##### _storage_list 7 #####
            ##### _storage_list 8 #####
        FF8 = pd.isnull(select_data['Form_Factor_8'].iloc[0])
        if FF8 is True:
            c2_storage8 = dbc.ListGroupItem("N/A", id="sb_c2_storage8",
                                            n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype8 = " "
            c2_storagemodel8 = " "
            c2_storagenum8 = " "
            c2_storagespeed8 = " "
            select_storage8 = " "
            storage_vendor8 = " "
            storage_model_name8 = " "
            form_factor8 = " "
            storage_interface8 = " "
            storage_capacity8 = " "
            media_components8 = " "
            power_consumption8 = " "
        else:
            c2_storagetype8 = select_data.at[duttest, 'Form_Factor_8']
            c2_storagemodel8 = select_data.at[duttest, 'Storage_Model_8']
            c2_storagenum8 = select_data.at[duttest, 'Storage_Number_8']
            c2_storagespeed8 = select_data.at[duttest, 'I/O_Type_Bus_Speed_8']
            select_storage8 = s_storage.loc[[c2_storagemodel8]]
            storage_vendor8 = select_storage8.at[c2_storagemodel8, 'Storage Vendor']
            storage_model_name8 = select_storage8.at[c2_storagemodel8, 'Storage Model Name']
            form_factor8 = select_storage8.at[c2_storagemodel8, 'Form Factor']
            storage_interface8 = select_storage8.at[c2_storagemodel8, 'Storage Interface']
            storage_capacity8 = select_storage8.at[c2_storagemodel8, 'Storage Capacity']
            media_components8 = select_storage8.at[c2_storagemodel8, 'Media / Components']
            power_consumption8 = select_storage8.at[c2_storagemodel8, 'Power Consumption(W)']
            c2_storage8 = dbc.ListGroupItem(str(c2_storagetype8) + " : " + str(int(c2_storagenum8)), id="sb_c2_storage8",
                                            n_clicks_timestamp="0", action=True, color="info")

        ##### _storage_list 8 #####
        ##### _storage_list 9 #####
        FF9 = pd.isnull(select_data['Form_Factor_9'].iloc[0])
        if FF9 is True:
            c2_storage9 = dbc.ListGroupItem("N/A", id="sb_c2_storage9",
                                            n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype9 = " "
            c2_storagemodel9 = " "
            c2_storagenum9 = " "
            c2_storagespeed9 = " "
            select_storage9 = " "
            storage_vendor9 = " "
            storage_model_name9 = " "
            form_factor9 = " "
            storage_interface9 = " "
            storage_capacity9 = " "
            media_components9 = " "
            power_consumption9 = " "
        else:
            c2_storagetype9 = select_data.at[duttest, 'Form_Factor_9']
            c2_storagemodel9 = select_data.at[duttest, 'Storage_Model_9']
            c2_storagenum9 = select_data.at[duttest, 'Storage_Number_9']
            c2_storagespeed9 = select_data.at[duttest, 'I/O_Type_Bus_Speed_9']
            select_storage9 = s_storage.loc[[c2_storagemodel9]]
            storage_vendor9 = select_storage9.at[c2_storagemodel9, 'Storage Vendor']
            storage_model_name9 = select_storage9.at[c2_storagemodel9, 'Storage Model Name']
            form_factor9 = select_storage9.at[c2_storagemodel9, 'Form Factor']
            storage_interface9 = select_storage9.at[c2_storagemodel9, 'Storage Interface']
            storage_capacity9 = select_storage9.at[c2_storagemodel9, 'Storage Capacity']
            media_components9 = select_storage9.at[c2_storagemodel9, 'Media / Components']
            power_consumption9 = select_storage9.at[c2_storagemodel9, 'Power Consumption(W)']
            c2_storage9 = dbc.ListGroupItem(str(c2_storagetype9) + " : " + str(int(c2_storagenum9)),
                                            id="sb_c2_storage9",
                                            n_clicks_timestamp="0", action=True, color="info")

        ##### _storage_list 9 #####

        ##### _storage_list 10 #####
        FF10 = pd.isnull(select_data['Form_Factor_10'].iloc[0])
        if FF10 is True:
            c2_storage10 = dbc.ListGroupItem("N/A", id="sb_c2_storage10",
                                             n_clicks_timestamp="0", style={'display': 'none'})
            c2_storagetype10 = " "
            c2_storagemodel10 = " "
            c2_storagenum10 = " "
            c2_storagespeed10 = " "
            select_storage10 = " "
            storage_vendor10 = " "
            storage_model_name10 = " "
            form_factor10 = " "
            storage_interface10 = " "
            storage_capacity10 = " "
            media_components10 = " "
            power_consumption10 = " "
        else:
            c2_storagetype10 = select_data.at[duttest, 'Form_Factor_10']
            c2_storagemodel10 = select_data.at[duttest, 'Storage_Model_10']
            c2_storagenum10 = select_data.at[duttest, 'Storage_Number_10']
            c2_storagespeed10 = select_data.at[duttest, 'I/O_Type_Bus_Speed_10']
            select_storage10 = s_storage.loc[[c2_storagemodel10]]
            storage_vendor10 = select_storage10.at[c2_storagemodel10, 'Storage Vendor']
            storage_model_name10 = select_storage10.at[c2_storagemodel10, 'Storage Model Name']
            form_factor10 = select_storage10.at[c2_storagemodel10, 'Form Factor']
            storage_interface10 = select_storage10.at[c2_storagemodel10, 'Storage Interface']
            storage_capacity10 = select_storage10.at[c2_storagemodel10, 'Storage Capacity']
            media_components10 = select_storage10.at[c2_storagemodel10, 'Media / Components']
            power_consumption10 = select_storage10.at[c2_storagemodel10, 'Power Consumption(W)']
            c2_storage10 = dbc.ListGroupItem(str(c2_storagetype10) + " : " + str(int(c2_storagenum10)),
                                             id="sb_c2_storage10",
                                             n_clicks_timestamp="0", action=True, color="info")
            ##### _storage_list 10 #####


        first_col = html.Div([

            dbc.Card(
            dbc.ListGroup(
                [
                    dbc.ListGroupItemHeading("System Information"),
                    dbc.ListGroupItem(product_name),
                    dbc.ListGroupItem("CPU", id="sb_c1_cpu", n_clicks_timestamp="0", action=True, color="info"),
                    dbc.ListGroupItem("CPU number: "+str(int(c1_cpunum))),
                    #topology,
                    dbc.ListGroupItem("DIMM", id="sb_c1_mem", n_clicks_timestamp="0", action=True, color="info"),
                    dbc.ListGroupItem("DIMM number: "+str(int(c1_memnum))),
                    dbc.ListGroupItem("Storage Device Category" , id="sb_c1_stg", n_clicks_timestamp="0", action=True, color="info"),
                    dbc.ListGroupItem(c1_testdata),
                ],
                flush=True,
            )
        ),
        ])

        second_col = html.Div([

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("CPU"),
                            cpu0,cpu1,cpu2,cpu3
                        ],
                        flush=True,
                    ),
                ),
                id="scpufade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("Memory DIMM"),
                            memA1, memA2, memB1, memB2, memC1, memC2, memD1, memD2, memE1, memE2, memF1, memF2,
                            memG1, memG2, memH1, memH2, memJ1, memJ2, memK1, memK2, memL1, memL2, memM1, memM2,
                        ],
                        flush=True,
                    ),
                ),
                id="smemfade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("Storage Device Category"),
                            c2_storage1,c2_storage2,c2_storage3,c2_storage4,c2_storage5,c2_storage6,c2_storage7,c2_storage8,c2_storage9,c2_storage10,
                        ],
                        flush=True,
                    ),
                ),
                id="sstoragefade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),


        ])

        third_col = html.Div([

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            #dbc.ListGroupItemHeading("aaaa"),
                            dbc.ListGroupItemHeading(id="scardheader_C"),
                            dbc.ListGroupItem("Code Name: "+str(code_Name)),
                            dbc.ListGroupItem("Processor Name: "+str(processor_name)),
                            dbc.ListGroupItem("Cores: "+str(int(cores))),
                            dbc.ListGroupItem("# of threads: "+str(int(threads))),
                            dbc.ListGroupItem("Processor Base Frequency: "+str(processor_base_frequency)+" GHz"),
                            dbc.ListGroupItem("Max Turbo Frequency: "+str(max_turbo_frequency)+" GHz"),
                            dbc.ListGroupItem("Cache: "+str(cache)+" MB"),
                            dbc.ListGroupItem("TDP: "+str(tDP)+" W"),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_cpufade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(id="scardheader_M"),
                            dbc.ListGroupItem("DIMM Vendor: "+str(dimm_vendor)),
                            dbc.ListGroupItem("Part Number: "+str(part_number)),
                            dbc.ListGroupItem("Memory Types: "+str(memory_types)),
                            dbc.ListGroupItem("# of Pin: "+str(int(of_pin))),
                            dbc.ListGroupItem("ECC Support: "+str(ecc_support)),
                            dbc.ListGroupItem("Maximum Memory Speed: "+str(int(maximum_memory_speed))+" MHz"),
                            dbc.ListGroupItem("Memory Size: "+str(memory_size)+" GB"),
                            dbc.ListGroupItem("# of Rank: " + str(of_rank)),
                            dbc.ListGroupItem("RAM Chip: " + str(ram_chip)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_memfade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype1),
                            dbc.ListGroupItem("Storage Vendor: "+str(storage_vendor1)),
                            dbc.ListGroupItem("Storage Model Name: "+str(storage_model_name1)),
                            dbc.ListGroupItem("Form Factor: "+str(form_factor1)),
                            dbc.ListGroupItem("Storage Interface: "+str(storage_interface1)),
                            dbc.ListGroupItem("Storage Capacity: "+str(storage_capacity1)),
                            dbc.ListGroupItem("Media / Components: "+str(media_components1)),
                            dbc.ListGroupItem("Power Consumption: "+str(power_consumption1)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed1)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade1",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype2),
                            dbc.ListGroupItem("Storage Vendor: " + str(storage_vendor2)),
                            dbc.ListGroupItem("Storage Model Name: " + str(storage_model_name2)),
                            dbc.ListGroupItem("Form Factor: " + str(form_factor2)),
                            dbc.ListGroupItem("Storage Interface: " + str(storage_interface2)),
                            dbc.ListGroupItem("Storage Capacity: " + str(storage_capacity2)),
                            dbc.ListGroupItem("Media / Components: " + str(media_components2)),
                            dbc.ListGroupItem("Power Consumption: " + str(power_consumption2)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed2)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade2",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype3),
                            dbc.ListGroupItem("Storage Vendor: " + str(storage_vendor3)),
                            dbc.ListGroupItem("Storage Model Name: " + str(storage_model_name3)),
                            dbc.ListGroupItem("Form Factor: " + str(form_factor3)),
                            dbc.ListGroupItem("Storage Interface: " + str(storage_interface3)),
                            dbc.ListGroupItem("Storage Capacity: " + str(storage_capacity3)),
                            dbc.ListGroupItem("Media / Components: " + str(media_components3)),
                            dbc.ListGroupItem("Power Consumption: " + str(power_consumption3)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed3)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade3",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype4),
                            dbc.ListGroupItem("Storage Vendor: " + str(storage_vendor4)),
                            dbc.ListGroupItem("Storage Model Name: " + str(storage_model_name4)),
                            dbc.ListGroupItem("Form Factor: " + str(form_factor4)),
                            dbc.ListGroupItem("Storage Interface: " + str(storage_interface4)),
                            dbc.ListGroupItem("Storage Capacity: " + str(storage_capacity4)),
                            dbc.ListGroupItem("Media / Components: " + str(media_components4)),
                            dbc.ListGroupItem("Power Consumption: " + str(power_consumption4)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed4)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade4",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype5),
                            dbc.ListGroupItem("Storage Vendor: " + str(storage_vendor5)),
                            dbc.ListGroupItem("Storage Model Name: " + str(storage_model_name5)),
                            dbc.ListGroupItem("Form Factor: " + str(form_factor5)),
                            dbc.ListGroupItem("Storage Interface: " + str(storage_interface5)),
                            dbc.ListGroupItem("Storage Capacity: " + str(storage_capacity5)),
                            dbc.ListGroupItem("Media / Components: " + str(media_components5)),
                            dbc.ListGroupItem("Power Consumption: " + str(power_consumption5)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed5)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade5",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype6),
                            dbc.ListGroupItem("Storage Vendor: " + str(storage_vendor6)),
                            dbc.ListGroupItem("Storage Model Name: " + str(storage_model_name6)),
                            dbc.ListGroupItem("Form Factor: " + str(form_factor6)),
                            dbc.ListGroupItem("Storage Interface: " + str(storage_interface6)),
                            dbc.ListGroupItem("Storage Capacity: " + str(storage_capacity6)),
                            dbc.ListGroupItem("Media / Components: " + str(media_components6)),
                            dbc.ListGroupItem("Power Consumption: " + str(power_consumption6)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed6)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade6",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype7),
                            dbc.ListGroupItem("Storage Vendor: " + str(storage_vendor7)),
                            dbc.ListGroupItem("Storage Model Name: " + str(storage_model_name7)),
                            dbc.ListGroupItem("Form Factor: " + str(form_factor7)),
                            dbc.ListGroupItem("Storage Interface: " + str(storage_interface7)),
                            dbc.ListGroupItem("Storage Capacity: " + str(storage_capacity7)),
                            dbc.ListGroupItem("Media / Components: " + str(media_components7)),
                            dbc.ListGroupItem("Power Consumption: " + str(power_consumption7)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed7)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade7",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype8),
                            dbc.ListGroupItem("Storage Vendor: " + str(storage_vendor8)),
                            dbc.ListGroupItem("Storage Model Name: " + str(storage_model_name8)),
                            dbc.ListGroupItem("Form Factor: " + str(form_factor8)),
                            dbc.ListGroupItem("Storage Interface: " + str(storage_interface8)),
                            dbc.ListGroupItem("Storage Capacity: " + str(storage_capacity8)),
                            dbc.ListGroupItem("Media / Components: " + str(media_components8)),
                            dbc.ListGroupItem("Power Consumption: " + str(power_consumption8)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed8)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade8",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype9),
                            dbc.ListGroupItem("Storage Vendor: " + str(storage_vendor9)),
                            dbc.ListGroupItem("Storage Model Name: " + str(storage_model_name9)),
                            dbc.ListGroupItem("Form Factor: " + str(form_factor9)),
                            dbc.ListGroupItem("Storage Interface: " + str(storage_interface9)),
                            dbc.ListGroupItem("Storage Capacity: " + str(storage_capacity9)),
                            dbc.ListGroupItem("Media / Components: " + str(media_components9)),
                            dbc.ListGroupItem("Power Consumption: " + str(power_consumption9)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed9)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade9",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(c2_storagetype10),
                            dbc.ListGroupItem("Storage Vendor: " + str(storage_vendor10)),
                            dbc.ListGroupItem("Storage Model Name: " + str(storage_model_name10)),
                            dbc.ListGroupItem("Form Factor: " + str(form_factor10)),
                            dbc.ListGroupItem("Storage Interface: " + str(storage_interface10)),
                            dbc.ListGroupItem("Storage Capacity: " + str(storage_capacity10)),
                            dbc.ListGroupItem("Media / Components: " + str(media_components10)),
                            dbc.ListGroupItem("Power Consumption: " + str(power_consumption10)),
                            dbc.ListGroupItem("Configuration Speed: " + str(c2_storagespeed10)),
                        ],
                        flush=True,
                    ),
                ),
                id="sc3_storagefade10",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
        ])
    elif testcase == "MLC":
        print("MLC")
        # C2_cpu_list
        cpu0 = dbc.ListGroupItem("CPU0", id="mb_c2_cpu0", n_clicks_timestamp="0", style={'display': 'none'})
        cpu1 = dbc.ListGroupItem("CPU1", id="mb_c2_cpu1", n_clicks_timestamp="0", style={'display': 'none'})
        cpu2 = dbc.ListGroupItem("CPU2", id="mb_c2_cpu2", n_clicks_timestamp="0", style={'display': 'none'})
        cpu3 = dbc.ListGroupItem("CPU3", id="mb_c2_cpu3", n_clicks_timestamp="0", style={'display': 'none'})
        for i in range(int(c1_cpunum)):
            if i == 0:
                cpu0 = dbc.ListGroupItem("CPU0", id="mb_c2_cpu0", n_clicks_timestamp="0", action=True, color="info")
            if i == 1:
                cpu1 = dbc.ListGroupItem("CPU1", id="mb_c2_cpu1", n_clicks_timestamp="0", action=True, color="info")
            if i == 2:
                cpu2 = dbc.ListGroupItem("CPU2", id="mb_c2_cpu2", n_clicks_timestamp="0", action=True, color="info")
            if i == 3:
                cpu3 = dbc.ListGroupItem("CPU3", id="mb_c2_cpu3", n_clicks_timestamp="0", action=True, color="info")

        # C2 mem list
        if "A1" in c2_memlo:
            memA1 = dbc.ListGroupItem("DIMM A1", id="mb_c2_A1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memA1 = dbc.ListGroupItem("DIMM A1", id="mb_c2_A1", n_clicks_timestamp="0", style={'display': 'none'})
        if "A2" in c2_memlo:
            memA2 = dbc.ListGroupItem("DIMM A2", id="mb_c2_A2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memA2 = dbc.ListGroupItem("DIMM A2", id="mb_c2_A2", n_clicks_timestamp="0", style={'display': 'none'})
        if "B1" in c2_memlo:
            memB1 = dbc.ListGroupItem("DIMM B1", id="mb_c2_B1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memB1 = dbc.ListGroupItem("DIMM B1", id="mb_c2_B1", n_clicks_timestamp="0", style={'display': 'none'})
        if "B2" in c2_memlo:
            memB2 = dbc.ListGroupItem("DIMM B2", id="mb_c2_B2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memB2 = dbc.ListGroupItem("DIMM B2", id="mb_c2_B2", n_clicks_timestamp="0", style={'display': 'none'})
        if "C1" in c2_memlo:
            memC1 = dbc.ListGroupItem("DIMM C1", id="mb_c2_C1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memC1 = dbc.ListGroupItem("DIMM C1", id="mb_c2_C1", n_clicks_timestamp="0", style={'display': 'none'})
        if "C2" in c2_memlo:
            memC2 = dbc.ListGroupItem("DIMM C2", id="mb_c2_C2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memC2 = dbc.ListGroupItem("DIMM C2", id="mb_c2_C2", n_clicks_timestamp="0", style={'display': 'none'})
        if "D1" in c2_memlo:
            memD1 = dbc.ListGroupItem("DIMM D1", id="mb_c2_D1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memD1 = dbc.ListGroupItem("DIMM D1", id="mb_c2_D1", n_clicks_timestamp="0", style={'display': 'none'})
        if "D2" in c2_memlo:
            memD2 = dbc.ListGroupItem("DIMM D2", id="mb_c2_D2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memD2 = dbc.ListGroupItem("DIMM D2", id="mb_c2_D2", n_clicks_timestamp="0", style={'display': 'none'})
        if "E1" in c2_memlo:
            memE1 = dbc.ListGroupItem("DIMM E1", id="mb_c2_E1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memE1 = dbc.ListGroupItem("DIMM E1", id="mb_c2_E1", n_clicks_timestamp="0", style={'display': 'none'})
        if "E2" in c2_memlo:
            memE2 = dbc.ListGroupItem("DIMM E2", id="mb_c2_E2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memE2 = dbc.ListGroupItem("DIMM E2", id="mb_c2_E2", n_clicks_timestamp="0", style={'display': 'none'})
        if "F1" in c2_memlo:
            memF1 = dbc.ListGroupItem("DIMM F1", id="mb_c2_F1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memF1 = dbc.ListGroupItem("DIMM F1", id="mb_c2_F1", n_clicks_timestamp="0", style={'display': 'none'})
        if "F2" in c2_memlo:
            memF2 = dbc.ListGroupItem("DIMM F2", id="mb_c2_F2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memF2 = dbc.ListGroupItem("DIMM F2", id="mb_c2_F2", n_clicks_timestamp="0", style={'display': 'none'})
        if "G1" in c2_memlo:
            memG1 = dbc.ListGroupItem("DIMM G1", id="mb_c2_G1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memG1 = dbc.ListGroupItem("DIMM G1", id="mb_c2_G1", n_clicks_timestamp="0", style={'display': 'none'})
        if "G2" in c2_memlo:
            memG2 = dbc.ListGroupItem("DIMM G2", id="mb_c2_G2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memG2 = dbc.ListGroupItem("DIMM G2", id="mb_c2_G2", n_clicks_timestamp="0", style={'display': 'none'})
        if "H1" in c2_memlo:
            memH1 = dbc.ListGroupItem("DIMM H1", id="mb_c2_H1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memH1 = dbc.ListGroupItem("DIMM H1", id="mb_c2_H1", n_clicks_timestamp="0", style={'display': 'none'})
        if "H2" in c2_memlo:
            memH2 = dbc.ListGroupItem("DIMM H2", id="mb_c2_H2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memH2 = dbc.ListGroupItem("DIMM H2", id="mb_c2_H2", n_clicks_timestamp="0", style={'display': 'none'})
        if "J1" in c2_memlo:
            memJ1 = dbc.ListGroupItem("DIMM J1", id="mb_c2_J1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memJ1 = dbc.ListGroupItem("DIMM J1", id="mb_c2_J1", n_clicks_timestamp="0", style={'display': 'none'})
        if "J2" in c2_memlo:
            memJ2 = dbc.ListGroupItem("DIMM J2", id="mb_c2_J2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memJ2 = dbc.ListGroupItem("DIMM J2", id="mb_c2_J2", n_clicks_timestamp="0", style={'display': 'none'})
        if "K1" in c2_memlo:
            memK1 = dbc.ListGroupItem("DIMM K1", id="mb_c2_K1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memK1 = dbc.ListGroupItem("DIMM K1", id="mb_c2_K1", n_clicks_timestamp="0", style={'display': 'none'})
        if "K2" in c2_memlo:
            memK2 = dbc.ListGroupItem("DIMM K2", id="mb_c2_K2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memK2 = dbc.ListGroupItem("DIMM K2", id="mb_c2_K2", n_clicks_timestamp="0", style={'display': 'none'})
        if "L1" in c2_memlo:
            memL1 = dbc.ListGroupItem("DIMM L1", id="mb_c2_L1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memL1 = dbc.ListGroupItem("DIMM L1", id="mb_c2_L1", n_clicks_timestamp="0", style={'display': 'none'})
        if "L2" in c2_memlo:
            memL2 = dbc.ListGroupItem("DIMM L2", id="mb_c2_L2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memL2 = dbc.ListGroupItem("DIMM L2", id="mb_c2_L2", n_clicks_timestamp="0", style={'display': 'none'})
        if "M1" in c2_memlo:
            memM1 = dbc.ListGroupItem("DIMM M1", id="mb_c2_M1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memM1 = dbc.ListGroupItem("DIMM M1", id="mb_c2_M1", n_clicks_timestamp="0", style={'display': 'none'})
        if "M2" in c2_memlo:
            memM2 = dbc.ListGroupItem("DIMM M2", id="mb_c2_M2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memM2 = dbc.ListGroupItem("DIMM M2", id="mb_c2_M2", n_clicks_timestamp="0", style={'display': 'none'})
        c1_topology = select_data.at[duttest, 'Topology']
        if c1_topology == "Ring":
            topology = dbc.ListGroupItem(c1_topology, id="mc1_topology", n_clicks_timestamp="0")
        elif c1_topology == "Star":
            topology = dbc.ListGroupItem(c1_topology, id="mc1_topology", n_clicks_timestamp="0")
        else:
            topology = dbc.ListGroupItem(c1_topology, id="mc1_topology", n_clicks_timestamp="0",style={'display': 'none'})
        first_col = html.Div([

            dbc.Card(
                dbc.ListGroup(
                    [
                        dbc.ListGroupItemHeading("System Information"),
                        dbc.ListGroupItem(product_name),
                        dbc.ListGroupItem("CPU", id="mb_c1_cpu", n_clicks_timestamp="0",action=True, color="info"),
                        dbc.ListGroupItem("CPU number: " + str(int(c1_cpunum))),
                        topology,
                        dbc.ListGroupItem("DIMM", id="mb_c1_mem", n_clicks_timestamp="0", action=True, color="info"),
                        dbc.ListGroupItem("DIMM number: "+str(int(c1_memnum))),
                        dbc.ListGroupItem(c1_testdata),
                    ],
                    flush=True,
                )
            ),
        ])
        second_col = html.Div([

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("CPU"),
                            cpu0, cpu1, cpu2, cpu3
                        ],
                        flush=True,
                    ),
                ),
                id="mcpufade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("Memory DIMM"),
                            memA1, memA2, memB1, memB2, memC1, memC2, memD1, memD2, memE1, memE2, memF1, memF2,
                            memG1, memG2, memH1, memH2, memJ1, memJ2, memK1, memK2, memL1, memL2, memM1, memM2,
                        ],
                        flush=True,
                    ),
                ),
                id="mmemfade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),
        ])

        third_col = html.Div([

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            # dbc.ListGroupItemHeading("aaaa"),
                            dbc.ListGroupItemHeading(id="mcardheader_C"),
                            dbc.ListGroupItem("Code Name: " + str(code_Name)),
                            dbc.ListGroupItem("Processor Name: " + str(processor_name)),
                            dbc.ListGroupItem("Cores: " +str(int(cores))),
                            dbc.ListGroupItem("# of threads: " + str(int(threads))),
                            dbc.ListGroupItem("Processor Base Frequency: " + str(processor_base_frequency)+" GHz"),
                            dbc.ListGroupItem("Max Turbo Frequency: " + str(max_turbo_frequency)+" GHz"),
                            dbc.ListGroupItem("Cache: " + str(cache)+" MB"),
                            dbc.ListGroupItem("TDP: " + str(tDP)+" W"),
                        ],
                        flush=True,
                    ),
                ),
                id="mc3_cpufade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(id="mcardheader_M"),
                            dbc.ListGroupItem("DIMM Vendor: " + str(dimm_vendor)),
                            dbc.ListGroupItem("Part Number: " + str(part_number)),
                            dbc.ListGroupItem("Memory Types: " + str(memory_types)),
                            dbc.ListGroupItem("# of Pin: " + str(int(of_pin))),
                            dbc.ListGroupItem("ECC Support: " + str(ecc_support)),
                            dbc.ListGroupItem("Maximum Memory Speed: " + str(int(maximum_memory_speed))+" MHz"),
                            dbc.ListGroupItem("Memory Size: " + str(int(memory_size))+" GB"),
                            dbc.ListGroupItem("# of Rank: " + str(of_rank)),
                            dbc.ListGroupItem("RAM Chip: " + str(ram_chip)),
                        ],
                        flush=True,
                    ),
                ),
                id="mc3_memfade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),
        ])

    elif testcase == "LAN":
        print("LAN")
        # C2_cpu_list
        cpu0 = dbc.ListGroupItem("CPU0", id="lb_c2_cpu0", n_clicks_timestamp="0", style={'display': 'none'})
        cpu1 = dbc.ListGroupItem("CPU1", id="lb_c2_cpu1", n_clicks_timestamp="0", style={'display': 'none'})
        cpu2 = dbc.ListGroupItem("CPU2", id="lb_c2_cpu2", n_clicks_timestamp="0", style={'display': 'none'})
        cpu3 = dbc.ListGroupItem("CPU3", id="lb_c2_cpu3", n_clicks_timestamp="0", style={'display': 'none'})
        for i in range(int(c1_cpunum)):
            if i == 0:
                cpu0 = dbc.ListGroupItem("CPU0", id="lb_c2_cpu0", n_clicks_timestamp="0", action=True, color="info")
            if i == 1:
                cpu1 = dbc.ListGroupItem("CPU1", id="lb_c2_cpu1", n_clicks_timestamp="0", action=True, color="info")
            if i == 2:
                cpu2 = dbc.ListGroupItem("CPU2", id="lb_c2_cpu2", n_clicks_timestamp="0", action=True, color="info")
            if i == 3:
                cpu3 = dbc.ListGroupItem("CPU3", id="lb_c2_cpu3", n_clicks_timestamp="0", action=True, color="info")

        # C2 mem list
        if "A1" in c2_memlo:
            memA1 = dbc.ListGroupItem("DIMM A1", id="lb_c2_A1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memA1 = dbc.ListGroupItem("DIMM A1", id="lb_c2_A1", n_clicks_timestamp="0", style={'display': 'none'})
        if "A2" in c2_memlo:
            memA2 = dbc.ListGroupItem("DIMM A2", id="lb_c2_A2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memA2 = dbc.ListGroupItem("DIMM A2", id="lb_c2_A2", n_clicks_timestamp="0", style={'display': 'none'})
        if "B1" in c2_memlo:
            memB1 = dbc.ListGroupItem("DIMM B1", id="lb_c2_B1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memB1 = dbc.ListGroupItem("DIMM B1", id="lb_c2_B1", n_clicks_timestamp="0", style={'display': 'none'})
        if "B2" in c2_memlo:
            memB2 = dbc.ListGroupItem("DIMM B2", id="lb_c2_B2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memB2 = dbc.ListGroupItem("DIMM B2", id="lb_c2_B2", n_clicks_timestamp="0", style={'display': 'none'})
        if "C1" in c2_memlo:
            memC1 = dbc.ListGroupItem("DIMM C1", id="lb_c2_C1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memC1 = dbc.ListGroupItem("DIMM C1", id="lb_c2_C1", n_clicks_timestamp="0", style={'display': 'none'})
        if "C2" in c2_memlo:
            memC2 = dbc.ListGroupItem("DIMM C2", id="lb_c2_C2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memC2 = dbc.ListGroupItem("DIMM C2", id="lb_c2_C2", n_clicks_timestamp="0", style={'display': 'none'})
        if "D1" in c2_memlo:
            memD1 = dbc.ListGroupItem("DIMM D1", id="lb_c2_D1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memD1 = dbc.ListGroupItem("DIMM D1", id="lb_c2_D1", n_clicks_timestamp="0", style={'display': 'none'})
        if "D2" in c2_memlo:
            memD2 = dbc.ListGroupItem("DIMM D2", id="lb_c2_D2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memD2 = dbc.ListGroupItem("DIMM D2", id="lb_c2_D2", n_clicks_timestamp="0", style={'display': 'none'})
        if "E1" in c2_memlo:
            memE1 = dbc.ListGroupItem("DIMM E1", id="lb_c2_E1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memE1 = dbc.ListGroupItem("DIMM E1", id="lb_c2_E1", n_clicks_timestamp="0", style={'display': 'none'})
        if "E2" in c2_memlo:
            memE2 = dbc.ListGroupItem("DIMM E2", id="lb_c2_E2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memE2 = dbc.ListGroupItem("DIMM E2", id="lb_c2_E2", n_clicks_timestamp="0", style={'display': 'none'})
        if "F1" in c2_memlo:
            memF1 = dbc.ListGroupItem("DIMM F1", id="lb_c2_F1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memF1 = dbc.ListGroupItem("DIMM F1", id="lb_c2_F1", n_clicks_timestamp="0", style={'display': 'none'})
        if "F2" in c2_memlo:
            memF2 = dbc.ListGroupItem("DIMM F2", id="lb_c2_F2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memF2 = dbc.ListGroupItem("DIMM F2", id="lb_c2_F2", n_clicks_timestamp="0", style={'display': 'none'})
        if "G1" in c2_memlo:
            memG1 = dbc.ListGroupItem("DIMM G1", id="lb_c2_G1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memG1 = dbc.ListGroupItem("DIMM G1", id="lb_c2_G1", n_clicks_timestamp="0", style={'display': 'none'})
        if "G2" in c2_memlo:
            memG2 = dbc.ListGroupItem("DIMM G2", id="lb_c2_G2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memG2 = dbc.ListGroupItem("DIMM G2", id="lb_c2_G2", n_clicks_timestamp="0", style={'display': 'none'})
        if "H1" in c2_memlo:
            memH1 = dbc.ListGroupItem("DIMM H1", id="lb_c2_H1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memH1 = dbc.ListGroupItem("DIMM H1", id="lb_c2_H1", n_clicks_timestamp="0", style={'display': 'none'})
        if "H2" in c2_memlo:
            memH2 = dbc.ListGroupItem("DIMM H2", id="lb_c2_H2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memH2 = dbc.ListGroupItem("DIMM H2", id="lb_c2_H2", n_clicks_timestamp="0", style={'display': 'none'})
        if "J1" in c2_memlo:
            memJ1 = dbc.ListGroupItem("DIMM J1", id="lb_c2_J1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memJ1 = dbc.ListGroupItem("DIMM J1", id="lb_c2_J1", n_clicks_timestamp="0", style={'display': 'none'})
        if "J2" in c2_memlo:
            memJ2 = dbc.ListGroupItem("DIMM J2", id="lb_c2_J2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memJ2 = dbc.ListGroupItem("DIMM J2", id="lb_c2_J2", n_clicks_timestamp="0", style={'display': 'none'})
        if "K1" in c2_memlo:
            memK1 = dbc.ListGroupItem("DIMM K1", id="lb_c2_K1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memK1 = dbc.ListGroupItem("DIMM K1", id="lb_c2_K1", n_clicks_timestamp="0", style={'display': 'none'})
        if "K2" in c2_memlo:
            memK2 = dbc.ListGroupItem("DIMM K2", id="lb_c2_K2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memK2 = dbc.ListGroupItem("DIMM K2", id="lb_c2_K2", n_clicks_timestamp="0", style={'display': 'none'})
        if "L1" in c2_memlo:
            memL1 = dbc.ListGroupItem("DIMM L1", id="lb_c2_L1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memL1 = dbc.ListGroupItem("DIMM L1", id="lb_c2_L1", n_clicks_timestamp="0", style={'display': 'none'})
        if "L2" in c2_memlo:
            memL2 = dbc.ListGroupItem("DIMM L2", id="lb_c2_L2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memL2 = dbc.ListGroupItem("DIMM L2", id="lb_c2_L2", n_clicks_timestamp="0", style={'display': 'none'})
        if "M1" in c2_memlo:
            memM1 = dbc.ListGroupItem("DIMM M1", id="lb_c2_M1", n_clicks_timestamp="0", action=True, color="info")
        else:
            memM1 = dbc.ListGroupItem("DIMM M1", id="lb_c2_M1", n_clicks_timestamp="0", style={'display': 'none'})
        if "M2" in c2_memlo:
            memM2 = dbc.ListGroupItem("DIMM M2", id="lb_c2_M2", n_clicks_timestamp="0", action=True, color="info")
        else:
            memM2 = dbc.ListGroupItem("DIMM M2", id="lb_c2_M2", n_clicks_timestamp="0", style={'display': 'none'})
        #c1_topology = select_data.at[duttest, 'Topology']
        #if c1_topology == "Ring":
        #    topology = dbc.ListGroupItem(c1_topology, id="c1_topology", n_clicks_timestamp="0")
        #elif c1_topology == "Star":
        #    topology = dbc.ListGroupItem(c1_topology, id="c1_topology", n_clicks_timestamp="0")
        #else:
        #    topology = dbc.ListGroupItem(c1_topology, id="c1_topology", n_clicks_timestamp="0", style={'display': 'none'})
        #c1_lan = select_data.at[duttest,'Controller']
        c1_card = select_data.at[duttest,'Card_Name']
        s_lan = pd.read_csv('data/component_lan.csv', index_col="ID")
        print(c1_card)
        select_lan = s_lan.loc[[c1_card]]
        lan_vendor = select_lan.at[c1_card,'Vendor']
        lan_model_name = select_lan.at[c1_card,'Card Name']
        lan_controller = select_lan.at[c1_card,'Controller']
        lan_datarate = select_lan.at[c1_card,'Data Rate Per Port']
        lan_interface_type = select_lan.at[c1_card,'System Interface Type']

        first_col = html.Div([

            dbc.Card(
            dbc.ListGroup(
                [
                    dbc.ListGroupItemHeading("System Information"),
                    dbc.ListGroupItem(product_name),
                    dbc.ListGroupItem("CPU", id="lb_c1_cpu", n_clicks_timestamp="0", action=True, color="info"),
                    dbc.ListGroupItem("CPU number: "+str(int(c1_cpunum))),
                    #topology,
                    dbc.ListGroupItem("DIMM", id="lb_c1_mem", n_clicks_timestamp="0", action=True, color="info"),
                    #print("LAN:"+c2_memlo),
                    #print("LAN:"+str(len(c2_memlo))),
                    dbc.ListGroupItem("DIMM number: "+str(int(c1_memnum))),
                    dbc.ListGroupItem("LAN Category", id="lb_c1_lan", n_clicks_timestamp="0", action=True, color="info"),
                    dbc.ListGroupItem(c1_testdata),
                ],
                flush=True,
            )
        ),
        ])

        second_col = html.Div([

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("CPU"),
                            cpu0,cpu1,cpu2,cpu3
                        ],
                        flush=True,
                    ),
                ),
                id="lcpufade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("Memory DIMM"),
                            memA1, memA2, memB1, memB2, memC1, memC2, memD1, memD2, memE1, memE2, memF1, memF2,
                            memG1, memG2, memH1, memH2, memJ1, memJ2, memK1, memK2, memL1, memL2, memM1, memM2,
                        ],
                        flush=True,
                    ),
                ),
                id="lmemfade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading("LAN Category"),
                            dbc.ListGroupItem(lan_model_name, id="b_c2_lan", n_clicks_timestamp="0", action=True, color="info"),
                        ],
                        flush=True,
                    ),
                ),
                id="lanfade",
                is_in=False,
                appear=False,
                style={'display': 'none'}
            ),

        ])

        third_col = html.Div([

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            #dbc.ListGroupItemHeading("aaaa"),
                            dbc.ListGroupItemHeading(id="lcardheader_C"),
                            dbc.ListGroupItem("Code Name: "+str(code_Name)),
                            dbc.ListGroupItem("Processor Name: "+str(processor_name)),
                            dbc.ListGroupItem("Cores: "+str(int(cores))),
                            dbc.ListGroupItem("# of threads: "+str(int(threads))),
                            dbc.ListGroupItem("Processor Base Frequency: "+str(processor_base_frequency)+" GHz"),
                            dbc.ListGroupItem("Max Turbo Frequency: "+str(max_turbo_frequency)+" GHz"),
                            dbc.ListGroupItem("Cache: "+str(cache)+" MB"),
                            dbc.ListGroupItem("TDP: "+str(tDP)+" W"),
                        ],
                        flush=True,
                    ),
                ),
                id="lc3_cpufade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(id="lcardheader_M"),
                            dbc.ListGroupItem("DIMM Vendor: "+str(dimm_vendor)),
                            dbc.ListGroupItem("Part Number: "+str(part_number)),
                            dbc.ListGroupItem("Memory Types: "+str(memory_types)),
                            dbc.ListGroupItem("# of Pin: "+str(int(of_pin))),
                            dbc.ListGroupItem("ECC Support: "+str(ecc_support)),
                            dbc.ListGroupItem("Maximum Memory Speed: "+str(int(maximum_memory_speed))+" MHz"),
                            dbc.ListGroupItem("Memory Size: "+str(int(memory_size))+" GB"),
                            dbc.ListGroupItem("# of Rank: " + str(of_rank)),
                            dbc.ListGroupItem("RAM Chip: " + str(ram_chip)),
                        ],
                        flush=True,
                    ),
                ),
                id="lc3_memfade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),

            dbc.Fade(
                dbc.Card(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItemHeading(id="cardheader_L"),
                            dbc.ListGroupItem("Vendor: "+str(lan_vendor)),
                            dbc.ListGroupItem("Model Name: "+str(lan_model_name)),
                            dbc.ListGroupItem("Controller: "+str(lan_controller)),
                            dbc.ListGroupItem("Date Rate Per Port: "+str(lan_datarate)),
                            dbc.ListGroupItem("System Interface Type: "+str(lan_interface_type)),
                        ],
                        flush=True,
                    ),
                ),
                id="c3_lanfade",
                is_in=False,
                appear=False,
                style={'display': 'none'},
            ),

        ])
    else:
        print("Not compare test case")

    return dbc.Row([dbc.Col(first_col, width=4), dbc.Col(second_col, width=4), dbc.Col(third_col, width=4)]),








#################    CPU    #################
@app.callback(
    [Output("card1_msg", "value"),Output("cpufade", "is_in"), Output("cpufade", "style"),Output("memfade", "is_in"), Output("memfade", "style"),Output("storagefade", "is_in"), Output("storagefade", "style")],
    [Input("b_c1_cpu", "n_clicks_timestamp"),Input("b_c1_mem", "n_clicks_timestamp"),Input("b_c1_stg", "n_clicks_timestamp")],
    [State("card1_msg", "value"),State("cpufade", "is_in"),State("memfade", "is_in"),State("storagefade", "is_in")]
)
def toggle_fade(c1c_nc, c1m_nc,c1s_nc,lastclick_C1,cis_in,mis_in,sis_in):
    if c1c_nc == "0" and c1m_nc == "0" and c1s_nc =="0" :
        # Button has never been clicked
        return f"No click",False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'}
    if int(c1c_nc) > int(c1m_nc) and int(c1c_nc) > int(c1s_nc) :
        lastclick="b_c1_cpu"
        if lastclick_C1 == lastclick:
            return f"b_c1_cpu", not cis_in, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'}
        else:
            return f"b_c1_cpu",True, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'}
    elif int(c1m_nc) > int(c1c_nc) and int(c1m_nc) > int(c1s_nc) :
        lastclick = "b_c1_mem"
        if lastclick_C1 == lastclick:
            return f"b_c1_mem", False, {'display': 'none'}, not mis_in, {'display': 'block'}, False, {'display': 'none'}
        else:
            return f"b_c1_mem", False, {'display': 'none'}, True, {'display': 'block'}, False, {'display': 'none'}
    elif int(c1s_nc) > int(c1c_nc) and int(c1s_nc) > int(c1m_nc) :
        lastclick = "b_c1_stg"
        if lastclick_C1 == lastclick:
            return f"b_c1_stg", False, {'display': 'none'}, False, {'display': 'none'}, not sis_in, {'display': 'block'}
        else:
            return f"b_c1_stg", False, {'display': 'none'}, False, {'display': 'none'}, True, {'display': 'block'}



@app.callback(
    [Output("card2_msg", "value"),Output("c3_cpufade", "is_in"), Output("c3_cpufade", "style"),Output("c3_memfade", "is_in"), Output("c3_memfade", "style"),Output("c3_storagefade", "is_in"), Output("c3_storagefade", "style"), Output("cardheader_C", "children"),Output("cardheader_M", "children"),Output("cardheader_S", "children")],
    [Input("b_c1_cpu", "n_clicks_timestamp"),Input("b_c1_mem", "n_clicks_timestamp"),Input("b_c1_stg", "n_clicks_timestamp"),
     Input("b_c2_cpu0", "n_clicks_timestamp"), Input("b_c2_cpu1", "n_clicks_timestamp"),Input("b_c2_cpu2", "n_clicks_timestamp"),Input("b_c2_cpu3", "n_clicks_timestamp"),
     Input("b_c2_A1", "n_clicks_timestamp"),Input("b_c2_A2", "n_clicks_timestamp"),Input("b_c2_B1", "n_clicks_timestamp"),Input("b_c2_B2", "n_clicks_timestamp"),
     Input("b_c2_C1", "n_clicks_timestamp"),Input("b_c2_C2", "n_clicks_timestamp"),Input("b_c2_D1", "n_clicks_timestamp"),Input("b_c2_D2", "n_clicks_timestamp"),
     Input("b_c2_E1", "n_clicks_timestamp"),Input("b_c2_E2", "n_clicks_timestamp"),Input("b_c2_F1", "n_clicks_timestamp"),Input("b_c2_F2", "n_clicks_timestamp"),
     Input("b_c2_G1", "n_clicks_timestamp"),Input("b_c2_G2", "n_clicks_timestamp"),Input("b_c2_H1", "n_clicks_timestamp"),Input("b_c2_H2", "n_clicks_timestamp"),
     Input("b_c2_J1", "n_clicks_timestamp"),Input("b_c2_J2", "n_clicks_timestamp"),Input("b_c2_K1", "n_clicks_timestamp"),Input("b_c2_K2", "n_clicks_timestamp"),
     Input("b_c2_L1", "n_clicks_timestamp"),Input("b_c2_L2", "n_clicks_timestamp"),Input("b_c2_M1", "n_clicks_timestamp"),Input("b_c2_M2", "n_clicks_timestamp"),
     Input("b_c2_nvmessdm2", "n_clicks_timestamp"),
     ],
    [State("card2_msg", "value"),State("c3_cpufade", "is_in"),State("c3_memfade", "is_in"),State("c3_storagefade", "is_in"),State("b_c2_nvmessdm2","children")]
)
def toggle_fade2(c1c_nc, c1m_nc,c1s_nc,
                 c0,c1,c2,c3,
                 ma1,ma2,mb1,mb2,mc1,mc2,md1,md2,me1,me2,mf1,mf2,
                 mg1,mg2,mh1,mh2,mj1,mj2,mk1,mk2,ml1,ml2,mm1,mm2,
                 nvmessdm2,
                 lastclick_C2,c2cis_in,c2mis_in,c2sis_in,storage_name):
        if c1c_nc == "0" and c1m_nc == "0" and c1s_nc == "0":
            # Button has never been clicked
            return f"No click", False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},f"",f"",f""
        var = {int(c1c_nc):"c1c_nc", int(c1m_nc):"c1m_nc",int(c1s_nc):"c1s_nc",
                 int(c0):"CPU 0",int(c1):"CPU 1",int(c2):"CPU 2",int(c3):"CPU 3",
                 int(ma1):"DIMM A1",int(ma2):"DIMM A2",int(mb1):"DIMM B1",int(mb2):"DIMM B2",int(mc1):"DIMM C1",int(mc2):"DIMM C2",int(md1):"DIMM D1",int(md2):"DIMM D2",int(me1):"DIMM E1",int(me2):"DIMM E2",int(mf1):"DIMM F1",int(mf2):"DIMM F2",
                 int(mg1):"DIMM G1",int(mg2):"DIMM G2",int(mh1):"DIMM H1",int(mh2):"DIMM H2",int(mj1):"DIMM J1",int(mj2):"DIMM J2",int(mk1):"DIMM K1",int(mk2):"DIMM K2",int(ml1):"DIMM L1",int(ml2):"DIMM L2",int(mm1):"DIMM M1",int(mm2):"DIMM M2",
                 int(nvmessdm2):"M.2 NVMe SSD"}

        lastc = str(var.get(max(var)))
        print(lastc)
        #cpu fade
        if lastc == "CPU 0" or lastc == "CPU 1" or lastc == "CPU 2" or lastc == "CPU 3":
            print(111)
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, not c2cis_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},lastc,lastc,lastc
            else:
                return lastc, True, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'},lastc,lastc,lastc
        elif lastc == "DIMM A1" or lastc == "DIMM A2" or lastc == "DIMM B1" or lastc == "DIMM B2" or lastc == "DIMM C1" or lastc == "DIMM C2" or lastc == "DIMM D1" or lastc == "DIMM D2" or lastc == "DIMM E1" or lastc == "DIMM E2" or lastc == "DIMM F1" or lastc == "DIMM F2" or lastc == "DIMM G1" or lastc == "DIMM G2" or lastc == "DIMM H1" or lastc == "DIMM H2" or lastc == "DIMM J1" or lastc == "DIMM J2" or lastc == "DIMM K1" or lastc == "DIMM K2" or lastc == "DIMM L1" or lastc == "DIMM L2" or lastc == "DIMM M1" or lastc == "DIMM M2":
            print(222)
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'},not c2mis_in, {'display': 'block'},False, {'display': 'none'},lastc,lastc,lastc
            else:
                return lastc, False, {'display': 'none'}, True, {'display': 'block'}, False, {'display': 'none'}, lastc,lastc,lastc
        elif lastc == "M.2 NVMe SSD":
            print(333)
            print(storage_name)
            storage_title= storage_name.split(':')
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},not c2sis_in, {'display': 'block'}, lastc, lastc, storage_title[0]
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, True, {'display': 'block'}, lastc, lastc, storage_title[0]
        else:
            lastclick1 = "N/A"
            return lastc, False, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'}, lastc, lastc, lastc
#################    CPU    #################



#################    MEM    #################
@app.callback(
    [Output("mcard1_msg", "value"),Output("mcpufade", "is_in"), Output("mcpufade", "style"),Output("mmemfade", "is_in"), Output("mmemfade", "style")],
    [Input("mb_c1_cpu", "n_clicks_timestamp"),Input("mb_c1_mem", "n_clicks_timestamp")],
    [State("mcard1_msg", "value"),State("mcpufade", "is_in"),State("mmemfade", "is_in")]
)
def toggle_fade(c1c_nc, c1m_nc,lastclick_C1,cis_in,mis_in):
    if c1c_nc == "0" and c1m_nc == "0":
        # Button has never been clicked
        return f"No click",False, {'display': 'none'}, False, {'display': 'none'}
    if int(c1c_nc) > int(c1m_nc):
        lastclick="b_c1_cpu"
        if lastclick_C1 == lastclick:
            return f"b_c1_cpu", not cis_in, {'display': 'block'}, False, {'display': 'none'}
        else:
            return f"b_c1_cpu",True, {'display': 'block'}, False, {'display': 'none'}
    elif int(c1m_nc) > int(c1c_nc):
        lastclick = "b_c1_mem"
        if lastclick_C1 == lastclick:
            return f"b_c1_mem", False, {'display': 'none'}, not mis_in, {'display': 'block'}
        else:
            return f"b_c1_mem", False, {'display': 'none'}, True, {'display': 'block'}


@app.callback(
    [Output("mcard2_msg", "value"),Output("mc3_cpufade", "is_in"), Output("mc3_cpufade", "style"),Output("mc3_memfade", "is_in"), Output("mc3_memfade", "style"), Output("mcardheader_C", "children"),Output("mcardheader_M", "children")],
    [Input("mb_c1_cpu", "n_clicks_timestamp"),Input("mb_c1_mem", "n_clicks_timestamp"),
     Input("mb_c2_cpu0", "n_clicks_timestamp"), Input("mb_c2_cpu1", "n_clicks_timestamp"),Input("mb_c2_cpu2", "n_clicks_timestamp"),Input("mb_c2_cpu3", "n_clicks_timestamp"),
     Input("mb_c2_A1", "n_clicks_timestamp"),Input("mb_c2_A2", "n_clicks_timestamp"),Input("mb_c2_B1", "n_clicks_timestamp"),Input("mb_c2_B2", "n_clicks_timestamp"),
     Input("mb_c2_C1", "n_clicks_timestamp"),Input("mb_c2_C2", "n_clicks_timestamp"),Input("mb_c2_D1", "n_clicks_timestamp"),Input("mb_c2_D2", "n_clicks_timestamp"),
     Input("mb_c2_E1", "n_clicks_timestamp"),Input("mb_c2_E2", "n_clicks_timestamp"),Input("mb_c2_F1", "n_clicks_timestamp"),Input("mb_c2_F2", "n_clicks_timestamp"),
     Input("mb_c2_G1", "n_clicks_timestamp"),Input("mb_c2_G2", "n_clicks_timestamp"),Input("mb_c2_H1", "n_clicks_timestamp"),Input("mb_c2_H2", "n_clicks_timestamp"),
     Input("mb_c2_J1", "n_clicks_timestamp"),Input("mb_c2_J2", "n_clicks_timestamp"),Input("mb_c2_K1", "n_clicks_timestamp"),Input("mb_c2_K2", "n_clicks_timestamp"),
     Input("mb_c2_L1", "n_clicks_timestamp"),Input("mb_c2_L2", "n_clicks_timestamp"),Input("mb_c2_M1", "n_clicks_timestamp"),Input("mb_c2_M2", "n_clicks_timestamp"),
     ],
    [State("mcard2_msg", "value"),State("mc3_cpufade", "is_in"),State("mc3_memfade", "is_in")]
)
def toggle_fade2(c1c_nc, c1m_nc,
                 c0,c1,c2,c3,
                 ma1,ma2,mb1,mb2,mc1,mc2,md1,md2,me1,me2,mf1,mf2,
                 mg1,mg2,mh1,mh2,mj1,mj2,mk1,mk2,ml1,ml2,mm1,mm2,
                 lastclick_C2,c2cis_in,c2mis_in):
        if c1c_nc == "0" and c1m_nc == "0":
            # Button has never been clicked
            return f"No click", False, {'display': 'none'}, False, {'display': 'none'},f"",f""
        var = {int(c1c_nc):"c1c_nc", int(c1m_nc):"c1m_nc",
                 int(c0):"CPU 0",int(c1):"CPU 1",int(c2):"CPU 2",int(c3):"CPU 3",
                 int(ma1):"DIMM A1",int(ma2):"DIMM A2",int(mb1):"DIMM B1",int(mb2):"DIMM B2",int(mc1):"DIMM C1",int(mc2):"DIMM C2",int(md1):"DIMM D1",int(md2):"DIMM D2",int(me1):"DIMM E1",int(me2):"DIMM E2",int(mf1):"DIMM F1",int(mf2):"DIMM F2",
                 int(mg1):"DIMM G1",int(mg2):"DIMM G2",int(mh1):"DIMM H1",int(mh2):"DIMM H2",int(mj1):"DIMM J1",int(mj2):"DIMM J2",int(mk1):"DIMM K1",int(mk2):"DIMM K2",int(ml1):"DIMM L1",int(ml2):"DIMM L2",int(mm1):"DIMM M1",int(mm2):"DIMM M2",
            }

        lastc = str(var.get(max(var)))
        print(lastc)
        #cpu fade
        if lastc == "CPU 0" or lastc == "CPU 1" or lastc == "CPU 2" or lastc == "CPU 3":
            print(111)
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, not c2cis_in, {'display': 'block'},False, {'display': 'none'},lastc,lastc
            else:
                return lastc, True, {'display': 'block'}, False, {'display': 'none'},lastc,lastc
        elif lastc == "DIMM A1" or lastc == "DIMM A2" or lastc == "DIMM B1" or lastc == "DIMM B2" or lastc == "DIMM C1" or lastc == "DIMM C2" or lastc == "DIMM D1" or lastc == "DIMM D2" or lastc == "DIMM E1" or lastc == "DIMM E2" or lastc == "DIMM F1" or lastc == "DIMM F2" or lastc == "DIMM G1" or lastc == "DIMM G2" or lastc == "DIMM H1" or lastc == "DIMM H2" or lastc == "DIMM J1" or lastc == "DIMM J2" or lastc == "DIMM K1" or lastc == "DIMM K2" or lastc == "DIMM L1" or lastc == "DIMM L2" or lastc == "DIMM M1" or lastc == "DIMM M2":
            print(222)
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'},not c2mis_in, {'display': 'block'},lastc,lastc
            else:
                return lastc, False, {'display': 'none'}, True, {'display': 'block'},lastc,lastc
        else:
            lastclick1 = "N/A"
            return lastc, False, {'display': 'block'}, False, {'display': 'none'}, lastc, lastc
#################    MEM    #################




#################    LAN    #################
@app.callback(
    [Output("lcard1_msg", "value"),Output("lcpufade", "is_in"), Output("lcpufade", "style"),Output("lmemfade", "is_in"), Output("lmemfade", "style"),Output("lanfade", "is_in"), Output("lanfade", "style")],
    [Input("lb_c1_cpu", "n_clicks_timestamp"),Input("lb_c1_mem", "n_clicks_timestamp"),Input("lb_c1_lan", "n_clicks_timestamp")],
    [State("lcard1_msg", "value"),State("lcpufade", "is_in"),State("lmemfade", "is_in"),State("lanfade", "is_in")]
)
def toggle_fade(c1c_nc, c1m_nc,c1l_nc,lastclick_C1,cis_in,mis_in,lis_in):
    if c1c_nc == "0" and c1m_nc == "0" and c1l_nc == "0" :
        # Button has never been clicked
        return f"No click",False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'}
    if int(c1c_nc) > int(c1m_nc) and int(c1c_nc) > int(c1l_nc):
        lastclick="b_c1_cpu"
        if lastclick_C1 == lastclick:
            return f"b_c1_cpu", not cis_in, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'}
        else:
            return f"b_c1_cpu",True, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'}
    elif int(c1m_nc) > int(c1c_nc) and int(c1m_nc) > int(c1l_nc):
        lastclick = "b_c1_mem"
        if lastclick_C1 == lastclick:
            return f"b_c1_mem", False, {'display': 'none'}, not mis_in, {'display': 'block'}, False, {'display': 'none'}
        else:
            return f"b_c1_mem", False, {'display': 'none'}, True, {'display': 'block'}, False, {'display': 'none'}
    elif int(c1l_nc) > int(c1c_nc) and int(c1l_nc) > int(c1m_nc):
        lastclick = "b_c1_lan"
        if lastclick_C1 == lastclick:
            return f"b_c1_lan", False, {'display': 'none'}, False, {'display': 'none'}, not lis_in, {'display': 'block'}
        else:
            return f"b_c1_lan", False, {'display': 'none'}, False, {'display': 'none'}, True, {'display': 'block'}


@app.callback(
    [Output("lcard2_msg", "value"),Output("lc3_cpufade", "is_in"), Output("lc3_cpufade", "style"),Output("lc3_memfade", "is_in"), Output("lc3_memfade", "style"),Output("c3_lanfade", "is_in"), Output("c3_lanfade", "style"),Output("lcardheader_C", "children"),Output("lcardheader_M", "children"),Output("cardheader_L", "children")],
    [Input("lb_c1_cpu", "n_clicks_timestamp"),Input("lb_c1_mem", "n_clicks_timestamp"),Input("lb_c1_lan", "n_clicks_timestamp"),
     Input("lb_c2_cpu0", "n_clicks_timestamp"), Input("lb_c2_cpu1", "n_clicks_timestamp"),Input("lb_c2_cpu2", "n_clicks_timestamp"),Input("lb_c2_cpu3", "n_clicks_timestamp"),
     Input("lb_c2_A1", "n_clicks_timestamp"),Input("lb_c2_A2", "n_clicks_timestamp"),Input("lb_c2_B1", "n_clicks_timestamp"),Input("lb_c2_B2", "n_clicks_timestamp"),
     Input("lb_c2_C1", "n_clicks_timestamp"),Input("lb_c2_C2", "n_clicks_timestamp"),Input("lb_c2_D1", "n_clicks_timestamp"),Input("lb_c2_D2", "n_clicks_timestamp"),
     Input("lb_c2_E1", "n_clicks_timestamp"),Input("lb_c2_E2", "n_clicks_timestamp"),Input("lb_c2_F1", "n_clicks_timestamp"),Input("lb_c2_F2", "n_clicks_timestamp"),
     Input("lb_c2_G1", "n_clicks_timestamp"),Input("lb_c2_G2", "n_clicks_timestamp"),Input("lb_c2_H1", "n_clicks_timestamp"),Input("lb_c2_H2", "n_clicks_timestamp"),
     Input("lb_c2_J1", "n_clicks_timestamp"),Input("lb_c2_J2", "n_clicks_timestamp"),Input("lb_c2_K1", "n_clicks_timestamp"),Input("lb_c2_K2", "n_clicks_timestamp"),
     Input("lb_c2_L1", "n_clicks_timestamp"),Input("lb_c2_L2", "n_clicks_timestamp"),Input("lb_c2_M1", "n_clicks_timestamp"),Input("lb_c2_M2", "n_clicks_timestamp"),
     Input("b_c2_lan", "n_clicks_timestamp")],
    [State("lcard2_msg", "value"),State("lc3_cpufade", "is_in"),State("lc3_memfade", "is_in"),State("c3_lanfade", "is_in")]
)
def toggle_fade2(c1c_nc, c1m_nc,c1l_nc,
                 c0,c1,c2,c3,
                 ma1,ma2,mb1,mb2,mc1,mc2,md1,md2,me1,me2,mf1,mf2,
                 mg1,mg2,mh1,mh2,mj1,mj2,mk1,mk2,ml1,ml2,mm1,mm2,
                 lan,
                 lastclick_C2,c2cis_in,c2mis_in,c2lis_in):
        if c1c_nc == "0" and c1m_nc == "0" and c1l_nc == "0":
            # Button has never been clicked
            return f"No click", False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},f"",f"",f""
        var = {int(c1c_nc):"c1c_nc", int(c1m_nc):"c1m_nc",int(c1l_nc):"c1l_nc",
                 int(c0):"CPU 0",int(c1):"CPU 1",int(c2):"CPU 2",int(c3):"CPU 3",
                 int(ma1):"DIMM A1",int(ma2):"DIMM A2",int(mb1):"DIMM B1",int(mb2):"DIMM B2",int(mc1):"DIMM C1",int(mc2):"DIMM C2",int(md1):"DIMM D1",int(md2):"DIMM D2",int(me1):"DIMM E1",int(me2):"DIMM E2",int(mf1):"DIMM F1",int(mf2):"DIMM F2",
                 int(mg1):"DIMM G1",int(mg2):"DIMM G2",int(mh1):"DIMM H1",int(mh2):"DIMM H2",int(mj1):"DIMM J1",int(mj2):"DIMM J2",int(mk1):"DIMM K1",int(mk2):"DIMM K2",int(ml1):"DIMM L1",int(ml2):"DIMM L2",int(mm1):"DIMM M1",int(mm2):"DIMM M2",
                 int(lan):"lan"}

        lastc = str(var.get(max(var)))
        print(lastc)
        #cpu fade
        if lastc == "CPU 0" or lastc == "CPU 1" or lastc == "CPU 2" or lastc == "CPU 3":
            print(111)
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, not c2cis_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},lastc,lastc,lastc
            else:
                return lastc, True, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'},lastc,lastc,lastc
        elif lastc == "DIMM A1" or lastc == "DIMM A2" or lastc == "DIMM B1" or lastc == "DIMM B2" or lastc == "DIMM C1" or lastc == "DIMM C2" or lastc == "DIMM D1" or lastc == "DIMM D2" or lastc == "DIMM E1" or lastc == "DIMM E2" or lastc == "DIMM F1" or lastc == "DIMM F2" or lastc == "DIMM G1" or lastc == "DIMM G2" or lastc == "DIMM H1" or lastc == "DIMM H2" or lastc == "DIMM J1" or lastc == "DIMM J2" or lastc == "DIMM K1" or lastc == "DIMM K2" or lastc == "DIMM L1" or lastc == "DIMM L2" or lastc == "DIMM M1" or lastc == "DIMM M2":
            print(222)
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'},not c2mis_in, {'display': 'block'},False, {'display': 'none'},lastc,lastc,lastc
            else:
                return lastc, False, {'display': 'none'}, True, {'display': 'block'}, False, {'display': 'none'},lastc,lastc,lastc
        elif lastc == "lan":
            print(333)
            lastclick1 = lastc
            lastc_lan = "LAN Information"
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},not c2lis_in, {'display': 'block'}, lastc, lastc, lastc_lan
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, True, {'display': 'block'}, lastc, lastc, lastc_lan
        else:
            lastclick1 = "N/A"
            return lastc, False, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'}, lastc, lastc, lastc
#################    LAN    #################

#################    RAID    #################
@app.callback(
    [Output("scard1_msg", "value"),Output("scpufade", "is_in"), Output("scpufade", "style"),Output("smemfade", "is_in"), Output("smemfade", "style"),Output("sstoragefade", "is_in"), Output("sstoragefade", "style")],
    [Input("sb_c1_cpu", "n_clicks_timestamp"),Input("sb_c1_mem", "n_clicks_timestamp"),Input("sb_c1_stg", "n_clicks_timestamp")],
    [State("scard1_msg", "value"),State("scpufade", "is_in"),State("smemfade", "is_in"),State("sstoragefade", "is_in")]
)
def toggle_fade(c1c_nc, c1m_nc,c1s_nc,lastclick_C1,cis_in,mis_in,sis_in):
    if c1c_nc == "0" and c1m_nc == "0" and c1s_nc =="0":
        # Button has never been clicked
        return f"No click",False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'}
    if int(c1c_nc) > int(c1m_nc) and int(c1c_nc) > int(c1s_nc) :
        lastclick="b_c1_cpu"
        if lastclick_C1 == lastclick:
            return f"b_c1_cpu", not cis_in, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'}
        else:
            return f"b_c1_cpu",True, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'}
    elif int(c1m_nc) > int(c1c_nc) and int(c1m_nc) > int(c1s_nc) :
        lastclick = "b_c1_mem"
        if lastclick_C1 == lastclick:
            return f"b_c1_mem", False, {'display': 'none'}, not mis_in, {'display': 'block'}, False, {'display': 'none'}
        else:
            return f"b_c1_mem", False, {'display': 'none'}, True, {'display': 'block'}, False, {'display': 'none'}
    elif int(c1s_nc) > int(c1c_nc) and int(c1s_nc) > int(c1m_nc) :
        lastclick = "b_c1_stg"
        if lastclick_C1 == lastclick:
            return f"b_c1_stg", False, {'display': 'none'}, False, {'display': 'none'}, not sis_in, {'display': 'block'}
        else:
            return f"b_c1_stg", False, {'display': 'none'}, False, {'display': 'none'}, True, {'display': 'block'}



@app.callback(
    [Output("scard2_msg", "value"),Output("sc3_cpufade", "is_in"), Output("sc3_cpufade", "style"),Output("sc3_memfade", "is_in"), Output("sc3_memfade", "style"),
     Output("sc3_storagefade1", "is_in"), Output("sc3_storagefade1", "style"),Output("sc3_storagefade2", "is_in"), Output("sc3_storagefade2", "style"),
Output("sc3_storagefade3", "is_in"), Output("sc3_storagefade3", "style"),Output("sc3_storagefade4", "is_in"), Output("sc3_storagefade4", "style"),
Output("sc3_storagefade5", "is_in"), Output("sc3_storagefade5", "style"),Output("sc3_storagefade6", "is_in"), Output("sc3_storagefade6", "style"),
Output("sc3_storagefade7", "is_in"), Output("sc3_storagefade7", "style"),Output("sc3_storagefade8", "is_in"), Output("sc3_storagefade8", "style"),
Output("sc3_storagefade9", "is_in"), Output("sc3_storagefade9", "style"),Output("sc3_storagefade10", "is_in"), Output("sc3_storagefade10", "style"),
     Output("scardheader_C", "children"),Output("scardheader_M", "children")],
    [Input("sb_c1_cpu", "n_clicks_timestamp"),Input("sb_c1_mem", "n_clicks_timestamp"),Input("sb_c1_stg", "n_clicks_timestamp"),
     Input("sb_c2_cpu0", "n_clicks_timestamp"), Input("sb_c2_cpu1", "n_clicks_timestamp"),Input("sb_c2_cpu2", "n_clicks_timestamp"),Input("sb_c2_cpu3", "n_clicks_timestamp"),
     Input("sb_c2_A1", "n_clicks_timestamp"),Input("sb_c2_A2", "n_clicks_timestamp"),Input("sb_c2_B1", "n_clicks_timestamp"),Input("sb_c2_B2", "n_clicks_timestamp"),
     Input("sb_c2_C1", "n_clicks_timestamp"),Input("sb_c2_C2", "n_clicks_timestamp"),Input("sb_c2_D1", "n_clicks_timestamp"),Input("sb_c2_D2", "n_clicks_timestamp"),
     Input("sb_c2_E1", "n_clicks_timestamp"),Input("sb_c2_E2", "n_clicks_timestamp"),Input("sb_c2_F1", "n_clicks_timestamp"),Input("sb_c2_F2", "n_clicks_timestamp"),
     Input("sb_c2_G1", "n_clicks_timestamp"),Input("sb_c2_G2", "n_clicks_timestamp"),Input("sb_c2_H1", "n_clicks_timestamp"),Input("sb_c2_H2", "n_clicks_timestamp"),
     Input("sb_c2_J1", "n_clicks_timestamp"),Input("sb_c2_J2", "n_clicks_timestamp"),Input("sb_c2_K1", "n_clicks_timestamp"),Input("sb_c2_K2", "n_clicks_timestamp"),
     Input("sb_c2_L1", "n_clicks_timestamp"),Input("sb_c2_L2", "n_clicks_timestamp"),Input("sb_c2_M1", "n_clicks_timestamp"),Input("sb_c2_M2", "n_clicks_timestamp"),
     Input("sb_c2_storage1", "n_clicks_timestamp"),Input("sb_c2_storage2", "n_clicks_timestamp"),Input("sb_c2_storage3", "n_clicks_timestamp"),Input("sb_c2_storage4", "n_clicks_timestamp"),Input("sb_c2_storage5", "n_clicks_timestamp"),
     Input("sb_c2_storage6", "n_clicks_timestamp"),Input("sb_c2_storage7", "n_clicks_timestamp"),Input("sb_c2_storage8", "n_clicks_timestamp"),Input("sb_c2_storage9", "n_clicks_timestamp"),Input("sb_c2_storage10", "n_clicks_timestamp"),
     ],
    [State("scard2_msg", "value"),State("sc3_cpufade", "is_in"),State("sc3_memfade", "is_in"),
     State("sc3_storagefade1", "is_in"),State("sc3_storagefade2", "is_in"),State("sc3_storagefade3", "is_in"),State("sc3_storagefade4", "is_in"),State("sc3_storagefade5", "is_in"),
    State("sc3_storagefade6", "is_in"),State("sc3_storagefade7", "is_in"),State("sc3_storagefade8", "is_in"),State("sc3_storagefade9", "is_in"),State("sc3_storagefade10", "is_in")
     ]
)
def toggle_fade2(c1c_nc, c1m_nc,c1s_nc,
                 c0,c1,c2,c3,
                 ma1,ma2,mb1,mb2,mc1,mc2,md1,md2,me1,me2,mf1,mf2,
                 mg1,mg2,mh1,mh2,mj1,mj2,mk1,mk2,ml1,ml2,mm1,mm2,
                 c2_storage1,c2_storage2,c2_storage3,c2_storage4,c2_storage5,c2_storage6,c2_storage7,c2_storage8,c2_storage9,c2_storage10,
                 lastclick_C2,c2cis_in,c2mis_in,c2s1is_in,c2s2is_in,c2s3is_in,c2s4is_in,c2s5is_in,c2s6is_in,c2s7is_in,c2s8is_in,c2s9is_in,c2s10is_in):
        if c1c_nc == "0" and c1m_nc == "0" and c1s_nc == "0" :
            # Button has never been clicked
            return f"No click", False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, f"",f""
        var = {int(c1c_nc):"c1c_nc", int(c1m_nc):"c1m_nc",int(c1s_nc):"c1s_nc",
                 int(c0):"CPU 0",int(c1):"CPU 1",int(c2):"CPU 2",int(c3):"CPU 3",
                 int(ma1):"DIMM A1",int(ma2):"DIMM A2",int(mb1):"DIMM B1",int(mb2):"DIMM B2",int(mc1):"DIMM C1",int(mc2):"DIMM C2",int(md1):"DIMM D1",int(md2):"DIMM D2",int(me1):"DIMM E1",int(me2):"DIMM E2",int(mf1):"DIMM F1",int(mf2):"DIMM F2",
                 int(mg1):"DIMM G1",int(mg2):"DIMM G2",int(mh1):"DIMM H1",int(mh2):"DIMM H2",int(mj1):"DIMM J1",int(mj2):"DIMM J2",int(mk1):"DIMM K1",int(mk2):"DIMM K2",int(ml1):"DIMM L1",int(ml2):"DIMM L2",int(mm1):"DIMM M1",int(mm2):"DIMM M2",
                 int(c2_storage1):"c2_storage1",int(c2_storage2):"c2_storage2",int(c2_storage3):"c2_storage3",int(c2_storage4):"c2_storage4",int(c2_storage5):"c2_storage5",
               int(c2_storage6):"c2_storage6",int(c2_storage7):"c2_storage7", int(c2_storage8):"c2_storage8",int(c2_storage9):"c2_storage9", int(c2_storage10):"c2_storage10"}

        lastc = str(var.get(max(var)))
        print(lastc)
        #cpu fade
        if lastc == "CPU 0" or lastc == "CPU 1" or lastc == "CPU 2" or lastc == "CPU 3":
            print(111)
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, not c2cis_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},lastc,lastc
            else:
                return lastc, True, {'display': 'block'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},lastc,lastc
        elif lastc == "DIMM A1" or lastc == "DIMM A2" or lastc == "DIMM B1" or lastc == "DIMM B2" or lastc == "DIMM C1" or lastc == "DIMM C2" or lastc == "DIMM D1" or lastc == "DIMM D2" or lastc == "DIMM E1" or lastc == "DIMM E2" or lastc == "DIMM F1" or lastc == "DIMM F2" or lastc == "DIMM G1" or lastc == "DIMM G2" or lastc == "DIMM H1" or lastc == "DIMM H2" or lastc == "DIMM J1" or lastc == "DIMM J2" or lastc == "DIMM K1" or lastc == "DIMM K2" or lastc == "DIMM L1" or lastc == "DIMM L2" or lastc == "DIMM M1" or lastc == "DIMM M2":
            print(222)
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'},not c2mis_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},lastc,lastc
            else:
                return lastc, False, {'display': 'none'}, True, {'display': 'block'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},lastc,lastc
        elif lastc == "c2_storage1" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},not c2s1is_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, True, {'display': 'block'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
        elif lastc == "c2_storage2" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},not c2s2is_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'}, True, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
        elif lastc == "c2_storage3" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},not c2s3is_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},True, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
        elif lastc == "c2_storage4" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},not c2s4is_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},True, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
        elif lastc == "c2_storage5" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},not c2s5is_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},True, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
        elif lastc == "c2_storage6" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},not c2s6is_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},True, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
        elif lastc == "c2_storage7" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},not c2s7is_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},True, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
        elif lastc == "c2_storage8" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},not c2s8is_in, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},True, {'display': 'block'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
        elif lastc == "c2_storage9" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},not c2s9is_in, {'display': 'block'},False, {'display': 'none'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},True, {'display': 'block'},False, {'display': 'none'}, lastc, lastc
        elif lastc == "c2_storage10" :
            lastclick1 = lastc
            if lastclick_C2 == lastclick1:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},not c2s10is_in, {'display': 'block'}, lastc, lastc
            else:
                return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},True, {'display': 'block'}, lastc, lastc
        else:
            lastclick1 = "N/A"
            return lastc, False, {'display': 'none'}, False, {'display': 'none'}, False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'},False, {'display': 'none'}, lastc, lastc
#################    RAID    #################


