# RAAN Internship Program Case Study
# Author: Iliana Papadopoulou

import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Import functions
from functions import *

    
# Initialize Dash Appication
app = dash.Dash(__name__)
server = app.server


edges_df,nodes_df = Read_Data()

# Get the number of network nodes
N = len(list(set(nodes_df['node_id'])))
Edges = list(edges_df['Edge_pair'])


# Create directed graph object from edgelist
G = nx.from_pandas_edgelist(edges_df, source = 'source_id', target = 'target_id',  edge_attr='weights', create_using=nx.DiGraph()) # create_using=nx.DiGraph()
nx.set_node_attributes(G, nodes_df.set_index('node_id').to_dict('index'))


# Get edges width based on their weight
widths = nx.get_edge_attributes(G, 'weights')


colors_dict = nodes_df.set_index('node_id')['node_color'].to_dict()
for n in G.nodes():
    G.nodes[n]['color'] = colors_dict[n]
    
#Labels dictionary has node_id as key and the label name as value 
labels = nodes_df.set_index('node_id')['node_label'].to_dict()

# Create 2-D visualization 
Visualize_2D_Network(G,widths,labels)

# Create 3-D visualization 
# Fruchterman Reingold layout (compatible with networkX) for plotly data
pos=nx.fruchterman_reingold_layout(G,dim=3) 

colors,labels = Create_Graph_Info(G,nodes_df)
etext,xtext,ytext,ztext,edge_x,edge_y,edge_z = Create_Text_Edges_Layout(G,edges_df,pos)

Nodes_Trace = Devise_Node_Trace(pos,colors,labels)
Edges_trace =  Devise_Edges_Trace(edge_x,edge_y,edge_z)
Weights_trace = Devise_Weights_Trace(xtext,ytext,ztext,etext)
layout = Create_Network_Layout()
    
# Build and plot 3-D Network
fig=go.Figure([Edges_trace,Weights_trace,Nodes_Trace],layout=layout)


# Define aplication layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port='8050')
