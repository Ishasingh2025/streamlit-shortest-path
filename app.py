import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import io

# --- Page setup ---
st.set_page_config(page_title="🚗 Advanced Road Trip Optimizer", layout="wide")

# --- Sidebar Settings ---
with st.sidebar:
    st.title("⚙️ Settings")
    metric = st.radio("📏 What do edge weights represent?", ['Miles (Distance)', 'Cost ($)', 'Time (minutes)'])
    layout_option = st.selectbox("🗺️ Choose Graph Layout", ["Spring", "Kamada-Kawai", "Circular", "Shell"])
    node_size = st.slider("🔘 Node Size", 500, 2500, 1500, 100)
    node_color = st.color_picker("🎨 Node Color", "#87CEEB")  # skyblue default

# --- Edge List ---
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

# --- Build Graph ---
G = nx.Graph()
G.add_weighted_edges_from(edges)

# --- Node Selection ---
all_nodes = sorted(G.nodes())
col1, col2 = st.columns(2)
with col1:
    start_node = st.selectbox("🚦 Select Starting Node", all_nodes, index=0)
with col2:
    end_node = st.selectbox("🏁 Select Destination Node", all_nodes, index=len(all_nodes)-1)

# --- Layout ---
if layout_option == "Spring":
    pos = nx.spring_layout(G, seed=42)
elif layout_option == "Kamada-Kawai":
    pos = nx.kamada_kawai_layout(G)
elif layout_option == "Circular":
    pos = nx.circular_layout(G)
else:
    pos = nx.shell_layout(G)

# --- Calculate Shortest Path ---
try:
    path = nx.dijkstra_path(G, start_node, end_node, weight='weight')
    length = nx.dijkstra_path_length(G, start_node, end_node, weight='weight')

    # --- Display Results ---
    st.subheader("🧭 Optimal Route Found")
    st.success(" → ".join(f"🏙️ {node}" for node in path))
    st.metric(f"Total {metric}", f"{length}")

    # --- Plot Graph ---
    st.subheader("🗺️ Network Visualization")
    fig, ax = plt.subplots(figsize=(8, 6))
    edge_labels = nx.get_edge_attributes(G, 'weight')

    nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=node_size, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=list(zip(path, path[1:])), edge_color='red', width=2.5, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, ax=ax)
    st.pyplot(fig)

    # --- Step-by-step Table ---
    st.subheader("📋 Route Breakdown")
    route_data = []
    for i in range(len(path) - 1):
        src = path[i]
        dest = path[i + 1]
        weight = G[src][dest]['weight']
        route_data.append({'From': src, 'To': dest, f'{metric}': weight})
    df = pd.DataFrame(route_data)
    st.dataframe(df, use_container_width=True)

    # --- Export Button ---
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button("📁 Download Path as CSV", data=csv_buffer.getvalue(),
                       file_name=f'shortest_path_{start_node}_to_{end_node}.csv',
                       mime='text/csv')

except nx.NetworkXNoPath:
    st.error(f"No path exists between **{start_node}** and **{end_node}**. Please select a connected pair.")
