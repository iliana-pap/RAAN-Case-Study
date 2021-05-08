# RAAN Internship Program Case Study
# Author: Iliana Papadopoulou

import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def Create_color_mapping_df(df):
    """
    Create a mapping dectionary between colors and integer values
    
    Args:
        df : dataframe with node_id, node_color and node_label
        
    Returns: 
        color_mapping : dictionary with color as key and incremental integer as value
        Create_Text_Edges_Layout
    """
    unique_colors = list(df['node_color'])
    color_mapping = dict.fromkeys(unique_colors)
    
    int_val = range(0,len(unique_colors))
    count = 0
    for key,value in color_mapping.items():
        color_mapping[key] = int_val[count]
        count = count +1
        
    return(color_mapping)

def Read_Data():
    
    """
    Read input data from excel file
        
    Returns: 
        edges_df : dataframe with node_id, node_color and node_label
        nodes_df : dataframe with source_id, target_id and weights
        
    """
    
    excel_file = pd.ExcelFile("raan_case_study interns.xlsx")

    # Extract excel sheets into dfs
    edges_df = excel_file.parse('edges')
    nodes_df = excel_file.parse('nodes')
    nodes_df.drop('Unnamed: 3',axis = 1, inplace = True)
    
    color_mapping = Create_color_mapping_df(nodes_df)
    nodes_df['group'] = nodes_df['node_color'].map(lambda x: color_mapping[x])
    
    edges_df['Edge_pair'] = list(zip(edges_df.source_id, edges_df.target_id))
    
    return(edges_df,nodes_df)

def Visualize_2D_Network(G,widths,labels):
    
    """
    Visualize network in 2-D
    
    Args:
        G: networkX garph object
        widths : dictionary with edges as key (tuple form) and weights as value
        labels :  dictionary with node_id as key and node_label as value
        
    """
    # Find edge list
    edge_list = {e: G.edges[e] for e in G.edges}
    
    # Add weights to edges
    weights = {e: G.edges[e]['weights'] for e in G.edges}
    
    # Color nodes
    colors = [node[1]['color'] for node in G.nodes(data=True)]

    # Visualize network
    pos = nx.spring_layout(G, k = 10, iterations = 50)

    fig = plt.figure(figsize=(20,20)) 
    
    nx.draw_networkx_nodes(G, pos,node_color = colors, node_size = 500)
    nx.draw_networkx_labels(G, pos,labels = labels)
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, arrows=True,
                            width=[x / 2 for x in list(widths.values())],
                            edge_color='gray')
    
    edge_labels=dict([((u,v,),d['weights'])
             for u,v,d in G.edges(data=True)])
    
    # Add weights as edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,label_pos=0.3) 
  
    
    # Save network as image (.png format)
    fig.savefig("Network_2D_Visualization.png",dpi = 300)


def Create_Graph_Info(G,nodes_df):
    
    """
    Compute colors and labels, which correspond to each node
    
    Args:
        G: networkX garph object
        nodes_df : dataframe with source_id, target_id and weights
       
    Returns:
        colors : dictionary with color as key and incremental integer as value
        labels : list of node_name items
        
    """
    
    labels = []
    colors = []
    for n in G.nodes():
        colors.append(nodes_df.loc[nodes_df['node_id'] == n, 'node_color'].iloc[0])
        labels.append(nodes_df.loc[nodes_df['node_id'] == n, 'node_label'].iloc[0])
        
    return(colors,labels)
        
def Create_Text_Edges_Layout(G,edges_df,pos):
    
    """
    Create text and edges for input into go.Scatter3d
    
    Args:
        G: networkX garph object
        edges_df : dataframe with node_id, node_color and node_label
        pos : dictionary with node_id as key and three element array as value
       
    Returns:
       etext : list of node weights
       xtext : list of weight positions for each edge in the x-dimension
       ytext : list of weight positions for each edge in the y-dimension
       ztext : list of weight positions for each edge in the z-dimension
       
       edge_x : list of source_id, target_id, None positions for each edge in the x-dimension
       edge_y : list of source_id, target_id, None positions for each edge in the y-dimension
       edge_z : list of source_id, target_id, None positions for each edge in the z-dimension
        
    """
    
    xtext=[]
    ytext=[]
    ztext = []
    etext = []
    check_for_directed_edges = []
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        
        offset = 0
        etext.append(edges_df.loc[edges_df['Edge_pair'] == edge, 'weights'].iloc[0])
        
        if tuple(reversed(edge)) in check_for_directed_edges:
            offset = 0.107
        else:
            offset = 0
    
        x0, x1, x2 =[pos[edge[0]][0],pos[edge[1]][0], None]
        y0, y1,y2 = [pos[edge[0]][1],pos[edge[1]][1], None]
        z0,z1,z2 = [pos[edge[0]][2],pos[edge[1]][2], None]
        
        xtext.append((x0+x1)/(2.5 + offset))
        ytext.append((y0+y1)/(2.5 + offset))
        ztext.append((z0+z1)/(2.5 + offset))
        
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(x2)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(y2)
        edge_z.append(z0)
        edge_z.append(z1)
        edge_z.append(z2)
        
        check_for_directed_edges.append(edge)
        
        
    return(etext,xtext,ytext,ztext,edge_x,edge_y,edge_z)


def Devise_Node_Trace(pos,colors,labels):
    
    """
    Devise Trace for Nodes
    
    Args:
       pos : dictionary with node_id as key and three element array as value
       colors : colors : dictionary with color as key and incremental integer as value
       labels : list of node_name items
       
    Returns:
      Nodes_Trace : Trace Object
        
    """
    
    Xn = []
    Yn = []
    Zn = []
    for key,val in pos.items():
        # x-coordinates of nodes
        Xn.append(pos[key][0]) 
        # y-coordinates of nodes
        Yn.append(pos[key][1])
        # z-cordivates of nodes
        Zn.append(pos[key][2]) 
    
    Nodes_Trace=go.Scatter3d(x=Xn,
                             y=Yn,
                             z=Zn,
                             mode='markers',
                             name='net',
                             marker=dict(symbol='circle',
                             size=7,
                             color=colors,
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )
    return(Nodes_Trace)
    
    
def Devise_Edges_Trace(edge_x,edge_y,edge_z):
    
    
    """
    Devise Trace for Edges
    
    Args:
       edge_x : list of source_id, target_id, None positions for each edge in the x-dimension
       edge_y : list of source_id, target_id, None positions for each edge in the y-dimension
       edge_z : list of source_id, target_id, None positions for each edge in the z-dimension
       
    Returns:
      Edges_trace : Trace Object
        
    """
    
    Edges_trace = go.Scatter3d(x=edge_x, 
                              y=edge_y,
                              z=edge_z,
                              mode='lines',
                              line=dict(color='rgb(125,125,125)', width=2),
                              hoverinfo='none'
    )
    
    return(Edges_trace)
    

def Devise_Weights_Trace(xtext,ytext,ztext,etext):
    
    """
    Devise Trace for Weights of Edges
    
    Args:
       etext : list of node weights
       xtext : list of weight positions for each edge in the x-dimension
       ytext : list of weight positions for each edge in the y-dimension
       ztext : list of weight positions for each edge in the z-dimension
       
    Returns:
      Weights_trace : Trace Object
        
    """
    
    Weights_trace = go.Scatter3d(x=xtext,
                                 y= ytext,
                                 z=ztext,
                                 mode='text',
                                 marker_size=0.5,
                                 text= etext,
                                 textposition='top right',
                                 hovertemplate='weight: %{text}'
    
    )
    
    return(Weights_trace)


def Create_Network_Layout():
    
    """
   Define layout for the network
    
    Returns:
      layout : layout Object
        
    """
    
    width=800
    height=800

    axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )
    layout = go.Layout(
            title="Interactive 3-D Network Visualization - Case Study",
            width=1000,
            height=1000,
            showlegend=False,
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
            ),
            margin=dict(
                t=100
            ),
            hovermode='closest'
            )
    
    return(layout)