import json
import re
import os
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from networkx.algorithms import community
from src.helpers.path_helpers import *

def visualize_hashtag_cooccurrence(
    posts_tags,
    output_filename,
    output_path="data\\visualizations\\networks",
    output_image=None,
    min_weight: int = 2,
    top_n: int = 25,
    label_degree_thresh: int = 1,
    k: float = 5.0,
    iterations: int = 100,
):
    output_path = join_paths(output_path, output_filename)

    # 2. Co-Occurrence zählen
    co_occurrence = {}
    for tags in posts_tags:
        for t1, t2 in combinations(tags, 2):
            pair = tuple(sorted([t1, t2]))
            co_occurrence[pair] = co_occurrence.get(pair, 0) + 1

    # 3. Graph aufbauen & filtern
    G = nx.Graph()
    # Knoten und Kanten nur mit weight >= min_weight
    for (t1, t2), w in co_occurrence.items():
        if w >= min_weight:
            G.add_edge(t1, t2, weight=w)
    # Nur die top_n Knoten nach Grad behalten
    if top_n and G.number_of_nodes() > top_n:
        deg_sorted = sorted(G.degree, key=lambda x: x[1], reverse=True)
        top_nodes = {n for n, d in deg_sorted[:top_n]}
        G = G.subgraph(top_nodes).copy()

    # 4. Community Detection für Farben
    communities = community.greedy_modularity_communities(G, weight="weight")
    # Map Node -> Community-Index
    node_color_map = {}
    for idx, comm in enumerate(communities):
        for node in comm:
            node_color_map[node] = idx

    # 5. Layout berechnen
    pos = nx.spring_layout(G, k=k, seed=42, iterations=iterations)

    # 6. Zeichnen
    plt.figure(figsize=(12, 10))
    # Nodes
    node_sizes = [200 + 1000 * G.degree(n) for n in G.nodes()]
    node_colors = [node_color_map[n] for n in G.nodes()]
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=plt.cm.tab20,
        alpha=0.9
    )
    # Edges
    edge_widths = [G[u][v]["weight"] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.4)

    # Labels nur für Knoten mit Grad >= label_degree_thresh
    labels = {
        n: n for n in G.nodes()
        if G.degree(n) >= label_degree_thresh
    }
    nx.draw_networkx_labels(G, pos, labels, font_size=9)

    plt.title("Hashtag Co-occurrence Network")
    plt.axis("off")

    # 7. Speichern oder anzeigen
    if output_image:
        # Wenn output_image ein Ordner ist, Dateinamen anhängen
        if os.path.isdir(output_image):
            output_image = os.path.join(output_image, "hashtag_network_top_25_higher_distance.png")
        plt.tight_layout()
        plt.savefig(output_image, dpi=300)
        print(f"✔ Netzwerk-Bild gespeichert: {output_image}")
    else:
        plt.show()

    print("\n=== Hashtag Co-occurrence Visualization Settings ===")
    print(f"Number of posts processed: {len(posts_tags)}")
    print(f"Min co-occurrence weight: {min_weight}")
    print(f"Top N nodes kept: {top_n}")
    print(f"Label degree threshold: {label_degree_thresh}")
    print(f"Spring layout k: {k}")
    print(f"Layout iterations: {iterations}")
    print(f"Output image: {output_image if output_image else 'Displayed on screen'}")
    print("====================================================\n")