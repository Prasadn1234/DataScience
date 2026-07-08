# ============================================================================
# WEEK 6.3: VISUALIZATION METHODS
# ============================================================================
#
# Assumes `ContractKnowledgeGraph` (week6_knowledge_graph.py) is already
# in scope.

def visualize_matplotlib(self):
    """
    Create matplotlib visualization of the knowledge graph.
    """

    plt.figure(figsize=(16, 12))

    # Get colors from node attributes
    colors = [self.graph.nodes[n].get('color', '#95a5a6') for n in self.graph.nodes()]

    # Calculate layout
    pos = nx.spring_layout(self.graph, k=2, iterations=50, seed=42)

    # Draw nodes, labels, and edges
    nx.draw_networkx_nodes(self.graph, pos, node_color=colors, node_size=1200, alpha=0.9)
    nx.draw_networkx_labels(self.graph, pos, font_size=8)
    nx.draw_networkx_edges(
        self.graph, pos, arrows=True, arrowsize=12, alpha=0.4,
        connectionstyle='arc3,rad=0.05',
    )

    # Legend: one entry per distinct node type, using its actual assigned color,
    # so node type is never identifiable by color alone
    type_colors = {}
    for _node, data in self.graph.nodes(data=True):
        node_type = data.get('type', 'OTHER')
        if node_type not in type_colors:
            type_colors[node_type] = data.get('color', '#95a5a6')
    legend_handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=12, label=node_type)
        for node_type, color in sorted(type_colors.items())
    ]
    plt.legend(handles=legend_handles, loc='upper left', title='Node Type')

    plt.title("Contract Knowledge Graph", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('contract_knowledge_graph.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("Visualization saved to contract_knowledge_graph.png")

def visualize_interactive(self, filename: str = "contract_kg.html"):
    """
    Create interactive PyVis visualization.
    """

    # Create PyVis network
    net = Network(height="600px", width="100%", directed=True, notebook=True)

    # Add nodes from graph
    for node, data in self.graph.nodes(data=True):
        net.add_node(
            node,
            label=node,
            color=data.get('color', '#95a5a6'),
            title=data.get('type', 'OTHER'),
        )

    # Add edges from graph
    for source, target, data in self.graph.edges(data=True):
        net.add_edge(source, target, title=data.get('relation', ''))

    # Save graph
    net.save_graph(filename)
    print(f"Interactive graph saved to {filename}")
    return filename

# Add methods to class
ContractKnowledgeGraph.visualize_matplotlib = visualize_matplotlib
ContractKnowledgeGraph.visualize_interactive = visualize_interactive

print("Visualization methods added")
