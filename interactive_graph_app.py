
import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

def build_candidate_graph(room_list, edge_list_str):
    G = nx.Graph()
    G.add_nodes_from(room_list)
    for line in edge_list_str.strip().split("\n"):
        try:
            u, v, w = line.split(",")
            G.add_edge(u.strip(), v.strip(), weight=float(w.strip()))
        except:
            continue
    return G

def display_graph_pyvis(G):
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")
    net.from_nx(G)

    # Add weights as titles
    for u, v, data in G.edges(data=True):
        net.get_edge(u, v)['title'] = f"Weight: {data.get('weight', 1.0)}"

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.show(tmp_file.name)
    return tmp_file.name

# Streamlit UI
st.set_page_config(page_title="Interactive Candidate Graph", layout="centered")
st.title("🧩 Interactive Candidate Graph Viewer")

room_input = st.text_input("Enter room names (comma-separated):", "Living, Kitchen, Bedroom1, Bath1")
candidate_edges_input = st.text_area("Candidate relationships (format: RoomA, RoomB, weight):", 
                                     "Living, Kitchen, 1.0\nBedroom1, Bath1, 0.8")

if st.button("Generate Candidate Graph"):
    rooms = [r.strip() for r in room_input.split(",")]
    G_candidate = build_candidate_graph(rooms, candidate_edges_input)

    st.markdown("### 📌 Drag nodes below to rearrange layout:")
    graph_html = display_graph_pyvis(G_candidate)
    with open(graph_html, 'r', encoding='utf-8') as f:
        components.html(f.read(), height=550, scrolling=True)
