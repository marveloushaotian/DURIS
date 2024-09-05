# Import required libraries
import igraph as ig
import matplotlib.pyplot as plt
import numpy as np

# 1. Create a sample graph
n_vertices = 10
n_edges = 15
g = ig.Graph.Erdos_Renyi(n=n_vertices, m=n_edges)

# 2. Add some attributes to vertices and edges
g.vs["name"] = [f"Node {i}" for i in range(n_vertices)]
g.vs["size"] = np.random.randint(10, 50, n_vertices)
g.es["weight"] = np.random.uniform(1, 5, n_edges)

# 3. Set up the plot
fig, ax = plt.subplots(figsize=(10, 8))
plt.title("Sample Network Graph")

# 4. Define layout and visual style
layout = g.layout_fruchterman_reingold()
visual_style = {
    "vertex_size": g.vs["size"],
    "vertex_label": g.vs["name"],
    "edge_width": [w/2 for w in g.es["weight"]],
    "layout": layout,
    "bbox": (300, 300),
    "margin": 20
}

# 5. Plot the graph
ig.plot(g, target=ax, **visual_style)

# 6. Show the plot
plt.show()

# Sample usage:
# Just run this script to generate and display the network graph
# python network_graph_example.py

# Note: This script creates a random graph each time it's run.
# For reproducibility, you may want to set a random seed.
