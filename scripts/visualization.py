# %%
# This script create an example calculation context and visualizes it

from dataclasses import dataclass
import matplotlib.pyplot as plt
import networkx as nx
from calculation_tree.model import DataSource, Operation, Node, Variable
from calculation_tree.services import CalculationContext

# %%
# Create graph

G = nx.Graph()

# %%
# Create a function to populate the graph with each node


def repr_node(n) -> str:
    match n:
        case DataSource():
            repr_ds = f"{n.name}"
            if n.description:
                repr_ds += f"\n{n.description}"
            if n.year:
                repr_ds += f"\n({n.year})"
            return repr_ds
        case Variable():
            return f"{n.name}\n=\n{n.value:.4g}"
        case Operation():
            return n.name
        case _:
            raise ValueError(f"Unknown node type: {type(n)}")


def populate_graph(node: Node):
    node_type = "FinalResult" if node.is_leaf else type(node).__name__
    G.add_node(node.id, type=node_type, repr=repr_node(node))
    if node.child:
        G.add_edge(node.id, node.child.id)


# %%
# Create a command to compute a transaction


@dataclass
class Command:
    pass


@dataclass
class ComputeTransaction(Command):
    normid: str
    year: int
    region: str
    value: float
    currency: str


compute_transaction = ComputeTransaction("02030000000000", 2023, "SE", 1000, "EUR")


# %%
# Create a new calculation context and populate the graph

with CalculationContext() as ctx:
    user_data = DataSource("User input", "Transaction", compute_transaction.year)
    transaction = ctx.variables.create(
        "Transaction", compute_transaction.value, parents=[user_data]
    )
    ef = ctx.emission_factors.get_by_normid(compute_transaction.normid)
    cf = ctx.conversion_factors.get_by_normid(compute_transaction.normid)
    assert ef and cf
    if cf.year != compute_transaction.year:
        ppi_from = ctx.price_indices.get_by_normid(
            compute_transaction.normid,
            compute_transaction.region,
            compute_transaction.year,
        )
        ppi_to = ctx.price_indices.get_by_normid(
            compute_transaction.normid,
            compute_transaction.region,
            cf.year,
        )
        assert ppi_from and ppi_to
        inflation_factor = ppi_to / ppi_from
        transaction *= inflation_factor
    activity_amount = transaction / cf
    emissions = activity_amount * ef
    ctx.traverse(populate_graph)  # type: ignore


# %%
# Visualize the graph

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[k for k, v in G.nodes.data("type") if v == "FinalResult"],
    node_size=1300,
    node_color="gold",
    node_shape="*",
)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[k for k, v in G.nodes.data("type") if v == "Variable"],
    node_size=1200,
    node_color="lightblue",
    node_shape="o",
)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[k for k, v in G.nodes.data("type") if v == "EmissionFactor"],
    node_size=1200,
    node_color="palegreen",
    node_shape="o",
)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[k for k, v in G.nodes.data("type") if v == "PriceIndex"],
    node_size=1200,
    node_color="khaki",
    node_shape="o",
)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[k for k, v in G.nodes.data("type") if v == "ConversionFactor"],
    node_size=1200,
    node_color="thistle",
    node_shape="o",
)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[k for k, v in G.nodes.data("type") if v == "Operation"],
    node_size=600,
    node_color="peachpuff",
    node_shape="s",
)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[k for k, v in G.nodes.data("type") if v == "DataSource"],
    node_size=1000,
    node_color="lightcoral",
    node_shape="h",
)
nx.draw_networkx_edges(
    G, pos, arrows=True, arrowstyle="<|-", arrowsize=10, min_source_margin=18
)
nx.draw_networkx_labels(
    G,
    pos,
    labels=dict(G.nodes.data("repr")),
    font_size=8,
    font_family="sans-serif",
)
plt.axis("off")
plt.show()

# %%
