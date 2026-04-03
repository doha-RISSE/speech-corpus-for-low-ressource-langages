import pynini
from pynini.lib import pynutil
from .base import GraphFst

class MoneyFst(GraphFst):
    def __init__(self, cardinal_fst, config):
        super().__init__("money")

        number = pynini.closure(pynini.union(*"0123456789"), 1)

        # mapping symbole -> nom
        currency_graph = pynini.string_map(list(config["currencies"].items()))

        # un espace explicitement consommé
        space = pynini.accep(" ")
        # un ou plusieurs espaces consécutifs
        spaces = pynini.closure(space, 1)

        # chemins qui reconnaissent :
        # 1) nombre + espaces + devise
        # 2) nombre + devise (collé)
        # 3) devise + espaces + nombre
        # 4) devise + nombre (collé)
        money_pattern = (
            number + spaces + currency_graph |
            number + currency_graph |
            currency_graph + spaces + number |
            currency_graph + number
        )

        self.fst = (
            pynutil.insert("money { ") +
            pynutil.insert("amount: \"") + number + pynutil.insert("\" ") +
            pynutil.insert("currency: \"") + currency_graph + pynutil.insert("\"") +
            pynutil.insert(" }")
        ).optimize()