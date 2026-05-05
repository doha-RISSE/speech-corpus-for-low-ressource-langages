import pynini
from pynini.lib import pynutil

def build_date_verbalizer(cardinal_fst, config):

    prefix_graph = pynini.union(
        *[pynutil.insert(p) for p in config["prefixes"]]
    )

    day = cardinal_fst
    year = cardinal_fst

    month_graphs = []

    if "cardinal" in config["month_modes"]:
        month_graphs.append(
            pynutil.insert(" شهر ") + cardinal_fst
        )

    if "name" in config["month_modes"]:
        month_names = pynini.string_map(
            list(config["months"].items())
        )
        month_graphs.append(
            pynutil.insert(" ") + month_names
        )

    month = pynini.union(*month_graphs)

    graph = (
        pynutil.delete('date { day: "') +
        prefix_graph +
        day +
        pynutil.delete('" month: "') +
        month +
        pynutil.delete('" year: "') +
        pynutil.insert(" ") +
        year +
        pynutil.delete('" }')
    )

    return graph.optimize()