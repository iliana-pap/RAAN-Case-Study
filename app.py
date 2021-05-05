# RAAN Internship Program Case Study
# Author: Iliana Papadopoulou

import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


# Initialize Dash Appication
app = dash.Dash(__name__)
server = app.server

excel_file = pd.ExcelFile("raan_case_study interns.xlsx")

# Extract excel sheets into dfs
edges_df = excel_file.parse('edges')
nodes_df = excel_file.parse('nodes')
nodes_df.drop('Unnamed: 3',axis = 1, inplace = True)


#Labels dictionary has node_id as key and the label name as value 
labels = nodes_df.set_index('node_id')['node_label'].to_dict()
colors_dict = nodes_df.set_index('node_id')['node_color'].to_dict()

# Create directed networkx object
G = nx.from_pandas_edgelist(edges_df, source = 'source_id', target = 'target_id',  edge_attr='weights',create_using=nx.DiGraph()) 
nx.set_node_attributes(G, nodes_df.set_index('node_id').to_dict('index'))

# Add weights to edges
weights = {e: G.edges[e]['weights'] for e in G.edges}
# Get edges width based on their weight
widths = nx.get_edge_attributes(G, 'weights')

for n in G.nodes():
    G.nodes[n]['color'] = colors_dict[n]


#Color nodes
colors = [node[1]['color'] for node in G.nodes(data=True)]

# Visualize network
#pos = nx.circular_layout(G)
#pos = nx.layout.shell_layout(G)
pos = nx.spring_layout(G, k=1, iterations=30)

plt.figure(figsize=(10,10)) 
nx.draw(G,pos,labels = labels,node_color=colors,node_size = 2000,width=[x / 2 for x in list(widths.values())], edge_color='navy')

# Add weights as edge labels
#nx.draw_networkx_edge_labels(G, pos, edge_labels=weights) 

plt.savefig("Network_2D_Visualization.png",dpi = 300)
plt.show()


weights_list = list(widths.values())
for node in G.nodes:
    G.nodes[node]['pos'] = list(pos[node])

edge_x = []
edge_y = []

# Define edge with Plotly
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append([x0,x1,None])
    edge_y.append([y0,y1,None])


# Devise multiple traces for adding weights to edges in the network
traces={}
for i in range(0, len(weights_list)):
    traces['edge' + str(i)]=go.Scatter(x = edge_x[i], 
                                           y = edge_y[i],
                                           line=dict(color='lightblue',width=weights_list[i]))



node_x = []
node_y = []
color_list = []
labels_list = []
print('colors',colors)
print('labels',labels)

# Define node with Plotly
for node in G.nodes():

    color_list.append(colors_dict[node])
    labels_list.append(labels[node])
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker={'size' : 15})



node_trace.marker.color  = color_list
node_trace.text = labels_list

data=list(traces.values()) + [node_trace]

# Create a customed figure layout
layout = go.Layout(
      autosize=False,
      width=1000,
      height=1000,
      title="fig_map")

# Build and plot figure
fig=go.Figure(data,layout=layout)

# Define aplication layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port='8050')
