from .base import GraphFst
from .money_parser import parse_money


class MoneyFst(GraphFst):
    """
    Verbalise une expression monétaire en Darija.
    Comportement entièrement contrôlé par config["money"].

    Modes (verbalization_order) :
      "amount_first"   → تمن مية و خمسين درهم
      "currency_first" → درهم تمن مية و خمسين

    Décimales (decimal_separator_word) :
      "فاصلة" → تمن مية فاصلة خمسين درهم
      "و"     → تمن مية و خمسين درهم
    """

    def __init__(self, cardinal_fst, config):
        super().__init__("money")
        self._cardinal_fst = cardinal_fst
        self._cfg          = config["money"]

    def verbalize(self, text: str) -> list:
        """
        Entrée  : "8500 درهم" | "MAD 8500" | "8500.50 €" | "€ 250" ...
        Sortie  : liste de toutes les verbalisations possibles
        """
        from utils import generate_all

        currencies = self._cfg["currencies"]
        amount_str, currency_verbal = parse_money(text, currencies)

        if amount_str is None:
            return [text]

        # Partie entière / décimale
        if "." in amount_str:
            int_part, dec_part = amount_str.split(".", 1)
        else:
            int_part, dec_part = amount_str, None

        int_verbals = generate_all(int_part, self._cardinal_fst) or [int_part]

        sep      = self._cfg.get("decimal_separator_word", "فاصلة")
        orders   = self._cfg.get("verbalization_order", ["amount_first"])

        results = []

        for int_v in int_verbals:

            # Bloc montant (avec ou sans décimale)
            if dec_part and int(dec_part) != 0:
                dec_verbals    = generate_all(str(int(dec_part)), self._cardinal_fst) or [dec_part]
                amount_verbals = [f"{int_v} {sep} {dec_v}" for dec_v in dec_verbals]
            else:
                amount_verbals = [int_v]

            # Application des ordres depuis config
            for amount_v in amount_verbals:
                for order in orders:
                    if order == "amount_first":
                        results.append(f"{amount_v} {currency_verbal}")
                    elif order == "currency_first":
                        results.append(f"{currency_verbal} {amount_v}")

        return list(set(results)) if results else [text]