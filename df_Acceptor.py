from AnBo_df_Throw import get_dataframe, Parameter_Units, get_file_path
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import os
import plotly.express as px
import AnBo_df_Throw

# def throwdata():
#     df = get_dataframe()
#     units = Parameter_Units()
#     return(df,units)
import pickle

with open('data.pkl', 'rb') as f:
    df, units = pickle.load(f)




def Plot_Temperature(df, units):

    Time = df['Time']
    Temperature = df['Temperature']

    fig = go.Figure(data=go.Scatter(
        x=Time,
        y=Temperature,
        mode='lines',
        name='Temperature',
        line=dict(color='firebrick')
    ))

    fig.update_layout(
        title=f"Temperature ({units[5]}) vs Time ({units[1]})",
        xaxis_title=f"Time ({units[1]})",
        yaxis_title=f"Temperature ({units[5]})"
    )
    return fig

def Plot_Temperature_Hours(df, units):
    
    Time = df['Time']/3600
    Temperature = df['Temperature']
    fig = go.Figure(data = go.Scatter(x = Time, y= Temperature, mode = 'lines', name = 'Temperature', line = dict(color = 'black')))
    
    fig.update_layout(title = f"Temperature ({units[5]}) vs Time (hours)",
                      xaxis_title = f"Time (hours)", 
                      yaxis_title = f"Temperature ({units[5]})"
                     )
    return fig


#Current (nA) vs Time (s)
def Plot_Current(df,units):
    Time = df['Time']
    Current = df['Current']

    
    fig = px.line(x = Time,y = Current, labels = {'x': f'Time ({units[1]})', 'y': f'Current ({units[4]})'}, title = f"Current ({units[4]}) vs Time ({units[1]})")
    return(fig)

#Current (nA) vs Time (hours)
def Plot_Current_Hours(df,units):
    Time = df['Time']/3600
    Current = df['Current']
    
    fig = px.line(x = Time,y = Current, labels = {'x': f'Time (hours)', 'y': f'Current ({units[4]})'}, title = f"Current ({units[4]}) vs Time (hours)")
    return(fig)

#Plot Voltage (V) vs Time (s)
def Plot_Voltage(df, units):
    Time = df['Time']
    Voltage = df['Measured V']
    
    fig = px.line(x = Time, y = Voltage, labels = {'x': f'Time ({units[1]})', 'y': f'Voltage ({units[3]})'}, title = f"Voltage ({units[3]}) vs Time ({units[1]})")
    return fig


#Plot Voltage (V) vs Time (hours)
def Plot_Voltage_Hours(df, units):
    Time = df['Time']/3600
    Voltage = df['Measured V']
    
    fig = px.line(x = Time, y = Voltage, labels = {'x': f'Time (hours)', 'y': f'Voltage ({units[3]})'}, title = f"Voltage ({units[3]}) vs Time (hours)")
    return fig




if __name__ == "__main__":
    # df, units = throwdata()
    # Plot_Temperature(df, units, ppp)    
##### df and units imported
    print()



