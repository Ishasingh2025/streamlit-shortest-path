import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.title("📍Shortest Path Finder - Road Trip Problem")

# Define the graph with edges and weights
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

metric = st.radio("Choose what the numbers represent:", ['Miles (Distance)', 'Cost ($)', 'Time (minutes)'])

G = nx.DiGraph()
G.add_weighted_edges_from(edges)

# Display the graph
st.subheader("📌 Road Network Graph")
fig, ax = plt.subplots()
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, ax=ax)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
st.pyplot(fig)

# Shortest path
path = nx.dijkstra_path(G, 'Origin', 'Destination', weight='weight')
length = nx.dijkstra_path_length(G, 'Origin', 'Destination', weight='weight')

st.subheader("🛣️ Shortest Path")
st.write(f"**Path:** {' → '.join(path)}")
st.write(f"**Total {metric}:** {length}")
