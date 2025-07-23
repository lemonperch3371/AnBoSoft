# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 17:48:19 2024

@author: VERMA Anshuman
Ph.D. Student
Scanning Probe Microscopy (Renner Group)
Department of Quantum Matter Physics
Université de Genève
24 Quai Ernest-Ansermet, Genève-1205, Suisse

University of Geneva, Department of Physics (Department of Quantum Matter Physics)

Module Name: AnBo_Reader_2_New_Format_HV.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from scipy.optimize import curve_fit as cf
import matplotlib.ticker as ticker
import os
import sqlalchemy
from sqlalchemy import create_engine
import datetime
from datetime import datetime as dt
from sqlalchemy import text
import tkinter as tk
from tkinter import filedialog
import pickle

def get_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title = "Select a .txt Data File for Anodic Bonding Data!")
    
    return(str(file_path).replace("/","\\"))






# file_path = r"Z:\AnshumanVerma\Anodic_Bonding_Data-AnshumanVerma\AnshumanVerma\TiSe2_Pre1\20250630_AB_TiSe2_Pre1_HK9L050_04\AB_TiSe2_Pre1_HK9L050_04_20250701_171549.txt"
is_Temperature = False 



def file_opener(file_path):
    
    # file_path = "F:\MoS2_Pre2\AB_MoS2_Pre2_BS_8\AB_MoS2_Pre2_BS_820241029_161943.txt"
    
    file = open(file_path,"r")
    file_lines = file.readlines()
    return(file_lines)


# Splits the file and each line is stored as an array element
def End_Of_Header_Index_Finder(file_path):
    file_lines = file_opener(file_path)
    EOH_index_array = []
    for index, line in enumerate(file_lines):
        if "end_of_header" in line.lower():
            # print(line)
            EOH_index_array.append(index)
            
    return(EOH_index_array)

def Header(file_path):
    file_lines = file_opener(file_path)
    eoh_index = End_Of_Header_Index_Finder(file_path)[-1]
    header = file_lines[:eoh_index+1]
    return(header)


def Parameter_Extractor(file_lines,EOH_Index_Array):
    parameters = (file_lines[EOH_Index_Array[-1] + 1].replace('\n','')).split('\t')
    return(parameters)

def Parameter_Units(file_path):
    header = Header(file_path)
    units = []
    for line in header:
        if "Y_Unit_Label" in line:
            units = line.replace('\n','').split('\t')[:-2]
    return(units)


def Data_Extractor(file_lines,EOH_Index_Array):
    last_EOH = EOH_Index_Array[-1]
    SOD_index = last_EOH + 2 #Start of Data Index
    data = file_lines[SOD_index:]
    return(data)

def df_Data_Column_Splitter(parameters,data):
    df = pd.DataFrame(columns = parameters[:-2])
    for p_index,parameter in enumerate(parameters[:-2]):
        values = []
        for line in data:
            values.append((line.replace('\t\n','')).split('\t')[p_index])
        df[parameter] = values
    
    if ',' in df[parameters[0]][0]:
        for c in df.columns:
            df[c] = [float(x.replace(',','.')) for x in df[c]]
    else:
        for c in df.columns:
            df[c] = [float(x) for x in df[c] if ',' not in x]
    # print(df.columns)
    return(df)


def Plot_Temperature(df, units,ppp):
    path = os.path.join(ppp,"Plot_Temperature")
    os.makedirs(path,exist_ok=True)
    Time = df['Time']
    Temperature = df['Temperature']
    plt.figure(figsize = (8,8))
    plt.xlabel(f"Time ({units[1]})")
    plt.ylabel(f"Temperature ({units[5]})")
    plt.title(f"Temperature ({units[5]}) vs Time ({units[1]})")
    plt.plot(Time, Temperature)
    plt.savefig(os.path.join(path,"Plot_Temperature.png"))
    plt.show()
    return 

def Plot_Temperature_Hours(df, units,ppp):
    path = os.path.join(ppp,"Plot_Temperature_Hour")
    os.makedirs(path,exist_ok=True)
    Time = df['Time']/3600
    Temperature = df['Temperature']
    plt.figure(figsize = (8,8))
    plt.xlabel(f"Time (hours)")
    plt.ylabel(f"Temperature ({units[5]})")
    plt.title(f"Temperature ({units[5]}) vs Time (hours)")
    plt.plot(Time, Temperature)
    plt.savefig(os.path.join(path,"Plot_Temperature.png"))
    plt.show()
    return 

def Plot_Current(df,units,ppp):
    Time = df['Time'][:]
    Current = df['Current'][:]
    path = os.path.join(ppp,"Plot_Current")
    os.makedirs(path,exist_ok=True)
    plt.figure(figsize = (8,8))
    plt.xlabel(f"Time ({units[1]})")
    plt.ylabel(f"Current ({units[4]})")
    plt.plot(Time, Current)
    plt.title(f"Current ({units[4]}) vs Time ({units[1]})\n Max Current: {np.min(Current)}{units[4]}")
    plt.ylim(-100,100)
    plt.savefig(os.path.join(path,"Plot_Current.png"))
    plt.show()
    return 

def Plot_Current_Hours(df,units,ppp):
    Time = df['Time'][:]/3600
    Current = df['Current'][:]
    path = os.path.join(ppp,"Plot_Current_Hours")
    os.makedirs(path,exist_ok=True)
    plt.figure(figsize = (8,8))
    plt.xlabel(f"Time (Hours)")
    plt.ylabel(f"Current ({units[4]})")
    plt.plot(Time, Current)
    plt.title(f"Current ({units[4]}) vs Time (Hours)\n Max Current: {np.min(Current)}{units[4]}")
    plt.ylim(-20,10)
    plt.savefig(os.path.join(path,"Plot_Current_Hours.png"))
    plt.show()
    return 

def Plot_Voltage(df, units,ppp):
    path = os.path.join(ppp,"Plot_Voltage")
    os.makedirs(path,exist_ok=True)
    Time = df['Time']
    Voltage = -df['Measured V']
    plt.figure(figsize = (8,8))
    plt.xlabel(f"Time ({units[1]})")
    plt.ylabel(f"Voltage ({units[2]})")
    plt.title(f"(-)Voltage ({units[2]}) vs Time ({units[1]})")
    plt.plot(Time, Voltage)
    plt.savefig(os.path.join(path,"Plot_Voltage.png"))
    plt.show()
    return 

def Plot_Voltage_Hours(df, units,ppp):
    path = os.path.join(ppp,"Plot_Voltage_Hours")
    os.makedirs(path,exist_ok=True)
    Time = df['Time']/3600
    Voltage = -df['Measured V']
    plt.figure(figsize = (8,8))
    plt.xlabel(f"Time (hours)")
    plt.ylabel(f"Voltage ({units[2]})")
    plt.title(f"(-)Voltage ({units[2]}) vs Time (hours)")
    plt.plot(Time, Voltage)
    plt.savefig(os.path.join(path,"Plot_Voltage_Hours.png"))
    plt.show()
    return 

def Plot_Current_Voltage_Time_Hours(df, units,ppp):
    path = os.path.join(ppp, "Plot_Current_Voltage_Time_Hours")
    os.makedirs(path, exist_ok=True)
    Time = df['Time'] / 3600
    Voltage = -df['Measured V']
    Current = df['Current']
    fig, ax1 = plt.subplots(figsize=(8, 8))
    color = 'tab:blue'
    ax1.set_xlabel('Time (hours)')
    ax1.set_ylabel(f'Current ({units[4]})', color=color)
    ax1.plot(Time, Current, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(-30, 400)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel(f'Voltage ({units[2]})', color=color)
    ax2.plot(Time, Voltage, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax1.set_title(f"Current and (-)Voltage vs Time (hours)")
    fig.tight_layout()
    plt.savefig(os.path.join(path, "Plot_Current_Voltage_Time_Hours.png"))
    plt.show()
    return 

def Max_Bonding_Voltage(df):
    return(np.max(np.abs(df['Programmed V'])))


def Max_Temperature(df,is_Temperature):
    if is_Temperature==True:
        return(np.max(df['Temperature']))
    else:
        return("Temperature not recorded")

# def Plot_Current_Hours(df, units, ppp):
#     # Extract Time and Current columns from the dataframe, starting at index 4000
#     Time = df['Time'][4000:] / 3600  # Convert Time from seconds to hours
#     Current = df['Current'][4000:]
    
#     # Create the directory for saving the plot if it doesn't exist
#     plot_dir = os.path.join(ppp, "Plot_Current_Hours")
#     os.makedirs(plot_dir, exist_ok=True)
    
#     # Plot the data
#     plt.figure(figsize=(12, 12))
#     plt.xlabel(f"Time (Hours)")
#     plt.ylabel(f"Current ({units[4]})")
#     plt.plot(Time, Current)
#     plt.title(f"Current ({units[4]}) vs Time (Hours)")

#     plt.savefig(os.path.join(plot_dir, "Plot_Current_Hours.png"))
    
#     plt.show()
    
#     return()

def Create_SQL_Database(df,file_path):

    df.columns = df.columns.str.replace(' ', '_')
    
    df['File_Name'] = os.path.basename(file_path[0:-4])
    
    file = os.path.basename(file_path[0:-4])

    engine = create_engine("mysql+pymysql://root:69420@localhost/")
    
    my_db = f"anodic_bonding_database"
    
    connection = engine.connect()
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {my_db};"))
    connection.close()
    
    new_engine = create_engine(f"mysql+pymysql://root:69420@localhost/{my_db}")
    
    # Upload DataFrame to MySQL with the table name 'anbo_1' (replace if it exists)
    table_name = f"{file}"
    
    df.to_sql(table_name, con=new_engine, if_exists='replace', index=False)
    
    print("\n!!Successfully created the Database!!")
    return()

def df_Thrower(df):
    return(df)

def get_dataframe(file_path):
    file_lines = file_opener(file_path)
    EOH_Index_Array = End_Of_Header_Index_Finder(file_path)
    units = Parameter_Units(file_path)
    data = Data_Extractor(file_lines, EOH_Index_Array)
    parameters = Parameter_Extractor(file_lines, EOH_Index_Array)
    df = df_Data_Column_Splitter(parameters, data)
    return df

def Probe_Current_Extractor():
    return()


def plot_all(df, units, ppp, is_Temperature):
    Plot_Current(df, units, ppp)
    Plot_Current_Hours(df, units, ppp)
    Plot_Voltage(df, units, ppp)
    Plot_Voltage_Hours(df, units, ppp)
    Plot_Current_Voltage_Time_Hours(df, units, ppp)
    if is_Temperature:
        Plot_Temperature_Hours(df, units, ppp)
        Plot_Temperature(df, units, ppp)
        
def throwdata(file_path):
    df = get_dataframe(file_path)
    units = Parameter_Units(file_path)
    return df, units
    
    #####
    #########
    #######
    
    #####
    #########
    #######
    
    #####
    #########
    #######
    
    #####
    #########
    #######
    
    #####
    #########
    #######
    
    #####
    #########
    #######
    
if __name__=="__main__":
   file_path = get_file_path()
   print(file_path)
   
   present_datetime= [dt.now().year,dt.now().month,dt.now().day,dt.now().hour,dt.now().minute,dt.now().second]
   pdt = ''.join([str(a) for a in present_datetime])
   
    
    
    
   file_lines = file_opener(file_path)
   EOH_Index_Array = End_Of_Header_Index_Finder(file_path)
   header = Header(file_path)
   
   # For convenience
   eoh = EOH_Index_Array[-1]
   # For convenience
   units = Parameter_Units(file_path)
   
   #PostProcessing
   post_processing_path = r"\AnBoSoft"
   os.makedirs(os.path.join(post_processing_path,"Anodic_Bonding_Plots"),exist_ok = True)
   post_processing_path = os.path.join(post_processing_path,"Anodic_Bonding_Plots_WrapUp")
   ppp = os.path.join(post_processing_path,"Anodic_Bonding_{}".format(file_path.split("\\")[-1][:-4]))
   os.makedirs(ppp,exist_ok = True)                                                                    
   #PostProcessing
   data = Data_Extractor(file_lines,EOH_Index_Array)
   parameters = Parameter_Extractor(file_lines,EOH_Index_Array)
   df = df_Data_Column_Splitter(parameters,data)
   if 'Temperature' in df.columns:
        is_Temperature = True
        
   plot_all(df, units, ppp, is_Temperature)
   throwdata(file_path)
   
  
   with open('data.pkl', 'wb') as f:
    pickle.dump((df, units), f)


        
  ### # df.columns = [f"{col} [{unit}]" for col, unit in zip(df.columns, units)] -BUGGY? BUGGY?
   
   
   
   
#    df_Thrower(df) #Throwing the df
#    Plot_Current(df,units,ppp)
#    Plot_Current_Hours(df,units,ppp)
#    Plot_Voltage(df,units,ppp)
#    Plot_Voltage_Hours(df,units,ppp)

#    Plot_Current_Voltage_Time_Hours(df, units, ppp)
   
   
#    if is_Temperature==True:
#         Plot_Temperature_Hours(df, units,ppp)
#         Plot_Temperature(df,units,ppp)


   print(Max_Temperature(df,is_Temperature),'\t' ,-1*Max_Bonding_Voltage(df))
   average_current = np.mean([x for x in df['Current'] if x<0])
   
   print(f"Average Current = {average_current}")
   

       
   
   #SQL Database Creator
   # Create_SQL_Database(df,file_path)
   
   
   
    