from .base import GraphFst
from .money_parser import parse_money


class MoneyFst(GraphFst):
    """
    Verbalise une expression monétaire en Darija.
    Stratégie : on sort du FST pur pour les montants décimaux
    (pynini ne gère pas le float nativement).
    On utilise money_parser pour extraire montant + devise,
    puis cardinal_fst pour verbaliser la partie entière.
    """

    def __init__(self, cardinal_fst, config):
        super().__init__("money")
        # On stocke ce dont verbalize() a besoin
        self._cardinal_fst = cardinal_fst
        self._config = config
        # Pas de self.fst fixe : la verbalization est dynamique (à cause des décimales)

    def verbalize(self, text):
        """
        Entrée  : "8500 درهم" | "MAD 8500" | "8500.50 €" ...
        Sortie  : liste de verbalisations possibles
        Ex      : ["تمن مية و خمسين درهم"]
                  ["تمن مية و خمسين فاصلة خمسة درهم"]   (si décimales)
        """
        import pynini
        from utils import generate_all

        amount_str, currency_verbal = parse_money(text)

        if amount_str is None:
            return [text]   # rien reconnu → on laisse tel quel

        # --- Partie entière ---
        if "." in amount_str:
            integer_part, decimal_part = amount_str.split(".")
        else:
            integer_part, decimal_part = amount_str, None

        # Verbaliser la partie entière via cardinal FST
        int_candidates = generate_all(integer_part, self._cardinal_fst)
        if not int_candidates:
            int_candidates = [integer_part]   # fallback

        results = []

        for int_verbal in int_candidates:
            if decimal_part and int(decimal_part) != 0:
                # Ex: 8500.50 → "تمن مية و خمسين فاصلة خمسين درهم"
                dec_candidates = generate_all(
                    str(int(decimal_part)),   # "50" pas "050"
                    self._cardinal_fst
                )
                if not dec_candidates:
                    dec_candidates = [decimal_part]
                for dec_verbal in dec_candidates:
                    results.append(
                        f"{int_verbal} فاصلة {dec_verbal} {currency_verbal}"
                    )
            else:
                # Ex: 8500 → "تمن مية و خمسين درهم"
                results.append(f"{int_verbal} {currency_verbal}")

        return list(set(results)) if results else [text]