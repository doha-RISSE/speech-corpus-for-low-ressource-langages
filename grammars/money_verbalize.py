import pynini
from pynini.lib import pynutil
from .base import GraphFst

class MoneyVerbalizeFst(GraphFst):
    def __init__(self, cardinal_fst, config):
        super().__init__("money_verbalize")

        amount = cardinal_fst

        currency_graph = pynini.string_map(
            list(config["currencies"].items())
        )

        self.fst = (
            pynutil.delete("money { amount: \"") +
            amount +
            pynutil.delete("\" currency: \"") +
            currency_graph +
            pynutil.delete("\" }")
        ).optimize()