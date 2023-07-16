from time import sleep
import os
import pandas as pd
import random
import string
import numpy as np
import flet as ft
from flet import (Page, FilePicker, Text,
                  ElevatedButton, Row, Column, FilePickerResultEvent)

inttype = np.sctypes['int']+[type(1)]
floattype = np.sctypes['float']+[type(1.2)]
maskingcolumns = []
checkbox={}
submitbtenble = False
CheckOnArray=[]
CheckOn=[]
df = pd.DataFrame()
valves = {}
filename= ''

####################

def readfile(path,header=None,sep=','):
    global checkbox,submitbtenble,df,filename,maskingcolumns
    df = pd.read_csv(path,sep = sep,header=header)
    return df

def getcolumns(df):
    list_of_column_names = list(df.columns)
    return list_of_column_names

def generate_random(length, data_type):
    global checkbox,submitbtenble,df,filename,maskingcolumns
    #print(str(type(data_type))+str(data_type)+str(length))
    try:
        float_val = float(data_type)
        decimal_places = len(str(data_type).split('.')[1])
        return str(round(
            random.uniform(0, 100), decimal_places))
    except Exception as e:
        
        if type(data_type) in inttype:
            return ''.join(random.choices(string.digits, k=length))
        elif data_type.isalpha() or type(data_type) in [type('s'),np.dtype('S')]:
            return ''.join(random.choices(string.ascii_letters, k=length))
        else:
            return "Invalid data type!"
    
def maskdata(df,columns=[]):
    global checkbox,submitbtenble,filename,maskingcolumns
    for i in columns:
        if i in df.columns:
            for ind in df.index:
                df.replace(df[i][ind], generate_random(length=len(str(df[i][ind])),data_type=df[i][ind]), inplace=True)
                       
def writefile(path):
     global df
     df.to_csv(path, index=False)

def main(page: ft.Page):
    try:
        global checkbox,submitbtenble,df,filename,maskingcolumns,pb
        page.title = "Data Masking"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        tb2 = ft.TextField(label="Enter Path",color=ft.colors.WHITE,border_color=ft.colors.WHITE54,)
        c4 = ft.Container(
            content=tb2,
            bgcolor=ft.colors.TRANSPARENT,
            padding=10,
            
            border_radius=ft.border_radius.all(5)
        )
        page.window_bgcolor = ft.colors.BLACK
	    # To select the file
        def select_file(e: FilePickerResultEvent):
            global checkbox,submitbtenble,df,filename,maskingcolumns
            if(len(lv.controls)>1):
                lv.controls=[file_path]
                maskingcolumns=[]
            page.add(filepicker)
            filepicker.pick_files("Select file...",)

        def on_click(e,msg):
            page.snack_bar = ft.SnackBar(ft.Text(msg))
            page.snack_bar.open = True
            page.update()
        def savefile(i):
            path = tb2.value

            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
            print(path)
            writefile(path=path+'out_'+filename,)
            open_dlg_modal('out_'+filename)

        def checkbox_changed(i):
            on_click(e=1,msg='Process Started')
            for i, checkbox in valves.items():
                    if checkbox.value == True:
                        if i not in maskingcolumns:
                            maskingcolumns.append(i)
                    if checkbox.value ==False:
                        if i in maskingcolumns:
                            maskingcolumns.remove(i)
            if len(maskingcolumns)!=0:
                c3.content=body2
                c3.update()
                maskdata(df=df,columns=maskingcolumns)
                
                c3.content= body4
                c3.update()
            else:
                c3.content=body3
                c3.update()
            
        subbt =  ElevatedButton(
                text="Submit And Process", on_click=checkbox_changed,)
        
        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("File Saved"),
            
            actions=[
                ft.TextButton("Ok", on_click=close_dlg),
                
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        # Once the file select the test value will update with path
        def return_file(e: FilePickerResultEvent): 
            global checkbox,submitbtenble,df,filename
            if(e.files==None):
                return
            filename = e.files[0].name
            file_path.value = e.files[0].path
            file_path.update()
            df = readfile(path=e.files[0].path,header=0,sep=tb1.value)
            columnsname = getcolumns(df=df)
            for i in columnsname:
                global array
                array = []
                CheckOn = ft.Checkbox(label=i, value=False)
                #print(CheckOn.value)
                CheckOnArray.append(CheckOn.value)
                #print(CheckOnArray)
                k =ft.Checkbox(label=i, value=False)
                valve_name = f"{i}"
                valves[valve_name] = k
                
                #  k = ft.Checkbox(data=i,on_change=checkbox_changed)
                #  checkbox[str(k)]= k
                #  print(checkbox[str(k)])
                #print(checkbox)
                lv.controls.extend([k])
            
            lv.controls.extend([subbt])
            c1.update()
            # for i in columnsname:
            #     lv.controls.append(ft.Text(f"Line {i}"))
            #     lv.update()

        filepicker = FilePicker(on_result=return_file)
        lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        
        file_path = ft.ListView([Text('Columns')])
        lv.controls.append(file_path)
        selectbt = ft.Container(
            content=ElevatedButton(
                text="Select file...", on_click=select_file,),
            bgcolor=ft.colors.TRANSPARENT,
            padding=5,
            border_radius=ft.border_radius.all(7)
        )
        
        c1 = ft.Container(
            content=lv,
            bgcolor=ft.colors.GREY_800,
            padding=5,
            height=page.window_height * 0.8,
            width=page.window_width * 0.48,
            border_radius=ft.border_radius.all(5)
        )
        body3 = ft.Column(controls=[ft.Image(
                    src="/Users/guna/FlutterDev/AppsFiles/Python/icon4.png",
                    width=160,
                    height=150,
                    fit=ft.ImageFit.COVER,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),Text('File Not Selected...')],alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        pb = ft.ProgressBar(width=400,height=7,)

        body4 = ft.Column(controls=[c4,ft.Image(
                    src="/Users/guna/FlutterDev/AppsFiles/Python/icon.png",
                    width=150,
                    height=150,
                    fit=ft.ImageFit.COVER,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),Text('Completed',size=18),ElevatedButton(
                text="Save File", on_click=savefile,)],alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        body2 = ft.Column(controls=[ft.Image(
                    src="/Users/guna/FlutterDev/AppsFiles/Python/icon2.png",
                    width=150,
                    height=150,
                    fit=ft.ImageFit.COVER,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),Text('Loading',size=18),pb],alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        c3 = ft.Container(
            content=body3,
            bgcolor=ft.colors.GREY_800,
            padding=5,
            height=page.window_height * 0.8,
            width=page.window_width * 0.48,
            border_radius=ft.border_radius.all(10)
        )
        
        bodyrow = Row([c1,c3],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        # row_filepicker = Column(horizontal_alignment="center")
        
        # row_filepicker.controls.append(
        #     file_path)
        tb1 = ft.TextField(label="Enter Delimiter",color=ft.colors.WHITE,border_color=ft.colors.WHITE54,value=',')
        
        c2 = ft.Container(
            content=tb1,
            bgcolor=ft.colors.TRANSPARENT,
            padding=10,
            
            border_radius=ft.border_radius.all(5)
        )

        

        col = ft.Column(spacing=0, controls=[Row(controls=[c2,selectbt],alignment=ft.MainAxisAlignment.START),bodyrow])

        page.add(col)

        # body = Row(vertical_alignment='start')
        # row_filepicker.controls.append(c1)
        
    
        # page.add(body)
        #page.add(row_filepicker)
    except Exception as e:
        print(e)
        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Something went wrong, try again..."),
            
            actions=[
                ft.TextButton("Ok", on_click=close_dlg),
                
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        open_dlg_modal(1)


ft.app(target=main)
                    
# df = readfile(path='data.csv',header=0)
# list_of_column_names = getcolumns(df=df)
# maskdata(df=df,columns=['name','id'])
# dff= df


