import pynini
from pynini.lib import pynutil
from .base import GraphFst

class MoneyFst(GraphFst):
    def __init__(self, cardinal_fst, config):
        super().__init__("money")

        number = pynini.closure(pynini.union(*"0123456789"), 1)
        currency = pynini.string_map(list(config["currencies"].items()))
        space = pynini.closure(pynini.accep(" "), 1)

        pattern = (
            number + space + currency |
            number + currency |
            currency + space + number |
            currency + number
        )

        self.fst = pattern.optimize()