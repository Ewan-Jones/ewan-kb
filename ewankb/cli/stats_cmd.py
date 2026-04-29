"""`ewankb stats` / `ewankb communities` / `ewankb surprising`."""

import json

from ._helpers import graph_file


def run_stats(args):
    from ewankb.tools.build_graph.__main__ import _print_stats

    gf = graph_file()
    with open(gf, encoding="utf-8") as f:
        graph = json.load(f)
    _print_stats(graph)


def run_communities(args):
    from ewankb.tools.build_graph.graph_builder import detect_communities
    from ewankb.tools.build_graph.__main__ import _print_communities

    gf = graph_file()
    with open(gf, encoding="utf-8") as f:
        graph = json.load(f)
    communities = detect_communities(graph)
    _print_communities(communities, graph)


def run_surprising(args):
    from ewankb.tools.build_graph.graph_builder import detect_communities, find_surprising_connections
    from ewankb.tools.build_graph.__main__ import _print_surprising

    gf = graph_file()
    with open(gf, encoding="utf-8") as f:
        graph = json.load(f)
    communities = detect_communities(graph)
    surprising = find_surprising_connections(graph, communities)
    _print_surprising(surprising)
