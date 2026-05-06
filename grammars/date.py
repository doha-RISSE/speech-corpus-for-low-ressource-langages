import pynini
from pynini.lib import pynutil
from .base import GraphFst

class DateFst(GraphFst):
    def __init__(self, cardinal_fst, config):
        super().__init__("date")

        # prefixes
        prefix_graph = pynini.union(
            *[pynutil.insert(p) for p in config["prefixes"]]
        )

        # day
        day = cardinal_fst

        # month options
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
        if "name_fr" in config["month_modes"]:
            month_names_fr = pynini.string_map(
                list(config["months_fr"].items())
            )
            month_graphs.append(
                pynutil.insert(" ") + month_names_fr
            )

        month = pynini.union(*month_graphs)

        # year
        year = pynutil.insert(" ") + cardinal_fst

        self.fst = (
            prefix_graph +
            day +
            pynutil.delete("/") +
            month +
            pynutil.delete("/") +
            year
        ).optimize()