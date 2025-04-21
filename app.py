import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Configure Streamlit page
st.set_page_config(page_title="🚗 Road Trip Optimizer", layout="wide")

# Sidebar content
with st.sidebar:
    st.title("📍 Road Trip Optimizer")
    st.markdown("This app calculates the **shortest path** between towns based on distance, cost, or time using **Dijkstra's Algorithm**.")
    st.markdown("Built with ❤️ using Streamlit + NetworkX")
    st.markdown("GitHub: [Add your link here](https://github.com/YOUR_USERNAME/streamlit-shortest-path)")
    st.markdown("---")
    layout_option = st.selectbox("🗺️ Choose Graph Layout", ["Spring", "Kamada-Kawai", "Circular", "Shell"])

# Radio button to select metric type
metric = st.radio("🔢 What do the numbers represent?", ['Miles (Distance)', 'Cost ($)', 'Time (minutes)'])

# Define the edge list from the problem
edges = [
    ('Origin', 'A', 40),
    ('Origin', 'B', 60),
    ('Origin', 'C', 50),
    ('A', 'B', 10),
    ('A', 'D', 70),
    ('B', 'C', 20),
    ('B', 'D', 55),
    ('B', 'E', 40),
    ('C', 'D', 50),
    ('D', 'E', 10),
    ('E', 'Destination', 60),
    ('D', 'Destination', 80)
]

# Create undirected graph (since roads are bidirectional)
G = nx.Graph()
G.add_weighted_edges_from(edges)

# Select layout
if layout_option == "Spring":
    pos = nx.spring_layout(G, seed=42)
elif layout_option == "Kamada-Kawai":
    pos = nx.kamada_kawai_layout(G)
elif layout_option == "Circular":
    pos = nx.circular_layout(G)
else:
    pos = nx.shell_layout(G)

# Compute shortest path
path = nx.dijkstra_path(G, 'Origin', 'Destination', weight='weight')
length = nx.dijkstra_path_length(G, 'Origin', 'Destination', weight='weight')

# Show route
st.subheader("🛣️ Shortest Route")
st.success(" → ".join(f"🏙️ {node}" for node in path))
st.metric(f"Total {metric}", f"{length}")

# Plotting the graph
st.subheader("🗺️ Route Map")
fig, ax = plt.subplots(figsize=(8, 6))
edge_labels = nx.get_edge_attributes(G, 'weight')

# Draw all edges and nodes
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1500, ax=ax)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', ax=ax)

# Highlight the path
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2.5, ax=ax)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, ax=ax)
st.pyplot(fig)

# Step-by-step breakdown
st.subheader("📋 Step-by-Step Travel Details")
route_data = []
for i in range(len(path) - 1):
    src = path[i]
    dest = path[i + 1]
    weight = G[src][dest]['weight']
    route_data.append({'From': src, 'To': dest, f'{metric}': weight})

df = pd.DataFrame(route_data)
st.dataframe(df, use_container_width=True)

# Footer
st.markdown("----")
st.caption("Need help deploying this or customizing it further? Just ask!")
