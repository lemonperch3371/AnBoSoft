from dash import Dash, html, dcc
from df_Acceptor import Plot_Temperature, Plot_Temperature_Hours, Plot_Current, Plot_Current_Hours, Plot_Voltage, Plot_Voltage_Hours
import os
import plotly.express as px
import pickle


app = Dash(__name__)
app.title = "Anodic Bonding Reader Software"

with open('data.pkl', 'rb') as f:
    df, units = pickle.load(f)


# Layout of the app
app.layout = html.Div([
    html.H1("Anodic Bonding Reader Software", style={"textAlign": "center"}),
    dcc.Graph(id='temperature-plot', figure=Plot_Temperature(df, units)),
    html.Br(),
    dcc.Graph(id='temperature-hours-plot', figure=Plot_Temperature_Hours(df, units)),
    html.Br(),
    dcc.Graph(id='current-plot', figure=Plot_Current(df, units)),
    html.Br(),
    dcc.Graph(id='current-hours-plot', figure=Plot_Current_Hours(df, units)),
    html.Br(),
    dcc.Graph(id='voltage-plot', figure=Plot_Voltage(df, units)),
    html.Br(),
    dcc.Graph(id='voltage-hours-plot', figure=Plot_Voltage_Hours(df, units))
])

#Running...
if __name__ == "__main__":
    app.run(debug=True)
