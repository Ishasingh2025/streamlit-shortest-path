import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Page config
st.set_page_config(page_title="🚗 Road Trip Planner", layout="wide")

# Sidebar info
with st.sidebar:
    st.title("🚗 Road Trip Optimizer")
    st.markdown("This app calculates the **shortest path** between towns based on distance, cost, or time using **Dijkstra's Algorithm**.")
    st.markdown("Built with ❤️ using Streamlit + NetworkX")
    st.markdown("[View Source on GitHub](https://github.com/YOUR_USERNAME/streamlit-shortest-path)")
    st.markdown("---")
    layout_option = st.selectbox("🔀 Choose Graph Layout", ["Spring", "Kamada-Kawai", "Circular", "Shell"])

# Metric selection
metric = st.radio("🔢 What do the numbers represent?", ['Miles (Distance)', 'Cost ($)', 'Time (minutes)'])

# Define the graph edges
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

# Build the directed graph
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

# Layout options
if layout_option == "Spring":
    pos = nx.spring_layout(G, seed=42)
elif layout_option == "Kamada-Kawai":
    pos = nx.kamada_kawai_layout(G)
elif layout_option == "Circular":
    pos = nx.circular_layout(G)
else:
    pos = nx.shell_layout(G)

# Calculate shortest path
path = nx.dijkstra_path(G, 'Origin', 'Destination', weight='weight')
length = nx.dijkstra_path_length(G, 'Origin', 'Destination', weight='weight')

# Show shortest path and route
st.subheader("🛣️ Shortest Route")
st.success(" → ".join(f"🏙️ {node}" for node in path))
st.metric(f"Total {metric}", f"{length}")

# Plot the graph with path highlighted
st.subheader("🗺️ Visual Map of Route")
fig, ax = plt.subplots(figsize=(8, 6))
edge_labels = nx.get_edge_attributes(G, 'weight')

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1500, ax=ax)

# Draw all edges in gray
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', arrows=True, ax=ax)

# Highlight the shortest path in red
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2.5, arrows=True, ax=ax)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, ax=ax)

st.pyplot(fig)

# Show step-by-step path info
st.subheader("📋 Step-by-Step Travel Details")
route_data = []
for i in range(len(path) - 1):
    src = path[i]
    dest = path[i + 1]
    weight = G[src][dest]['weight']
    route_data.append({'From': src, 'To': dest, f'{metric}': weight})
df = pd.DataFrame(route_data)
st.dataframe(df, use_container_width=True)

# Optional feedback
st.markdown("----")
st.caption("Made with Streamlit 🚀 | Need help deploying? Just ask.")
