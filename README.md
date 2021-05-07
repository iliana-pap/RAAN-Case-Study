# RAAN-Case-Study

## Interactive network 2-D and 3-D visualizations with NetworkX, Plotly, Dash and Heroku

This project includes the 2D and 3D Visualizations of a network archichecture, utilizing networkX and plotly libraries as well as the creation of a web application via Dash and its deployment via Heroku.

[NetworkX](https://networkx.org/) constitutes a Python package, which aims to the devision, handling and evaluation of complex networks with respect to their structure, dynamics and functionality. 

[Plotly](https://plotly.com/) library consists of an interactive, open-source plotting library, which offers chart types for diverse statistical, financial, geographic, scientific, and 3-dimensional use-cases.

[Dash](https://dash.plotly.com/introduction#:~:text=Dash%20is%20a%20productive%20Python,works%20with%20data%20in%20Python.) framework, implemented on top of Flask, Plotly.js, and React.js, enables the development of highly customable analytic web applications using various programming languages (Python, R, and Julia), without the need for JavaScript and DevOps.

[Heroku](https://www.heroku.com/what), being a container-based cloud Platform, permit developers to deploy, manage, and scale modern apps.

The project pipeline can be summarized below:


Assumptions about visualizations:

- 2D : The weights of the edges are present both as a number in the middle of the edge and as the width of the edge. Larger width corresponds to larger edge weight. Due to networkX implementation, in interacted nodes, their shared edge contains arrowheads in both ends.

![image](Network_2D_Visualization.png)

- 3D : Plotly and Dash do not enable the drawing of directed graphs, with the exception of introducing arrows in the form of annotations. However, the aforementioned restricts the interactivity of the network edges during live rotations. To overcome this issue, directed edges between two nodes have their weights very close to each other. In this case, for avoiding the overlapping, a small offset to the position of the weight has been introduced during the examination of the reversed edge.
- 3D : The display of the edge weights is performed by defining an additional trace for weights. Weights_trace is a scatter trace, of mode='text', with x, y, z lists being the middle point coordinates of the edges. 

The interactive 3-D visualization of the network can be found [here](https://network3dvisual.herokuapp.com/).




## References

https://plotly.com/python/v3/igraph-networkx-comparison/

https://networkx.org/documentation/stable/tutorial.html

https://dashboard.heroku.com/apps
