import pynini
from pynini.lib import pynutil
from .base import GraphFst

class MoneyVerbalizeFst(GraphFst):
    def __init__(self, cardinal_fst, config):
        super().__init__("money_verbalize")

        # lecture du nombre avec cardinal_fst
        amount = cardinal_fst

        currency_names = []
        for sym, name in config["currencies"].items():
            # on prévoit plusieurs versions possibles
            currency_names.append((name, name))

        currency_graph = pynini.string_map(currency_names)

        # supprimer les tags et produire la phrase
        self.fst = (
            pynutil.delete("money { amount: \"") +
            amount +
            pynutil.insert(" ") +  # ← on insère un espace ici
            pynutil.delete("\" currency: \"") +
            currency_graph +
            pynutil.delete("\" }")
        ).optimize()