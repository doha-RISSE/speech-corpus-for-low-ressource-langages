from .base import GraphFst
from .cardinal import verbalize_number
import re


class PercentFst(GraphFst):
    """
    Verbalise un pourcentage.
    Ex: 25% → خمسة وعشرين فالمية
    Ex: 8.5% → تمنية فاصلة خمسة فالمية
    """

    def __init__(self, config):
        super().__init__("percent")
        self._cfg = config.get("percent", {})
        self._suffix = self._cfg.get("suffix_word", "فالمية")
        # Pour la partie décimale, réutiliser le séparateur de money si dispo
        self._decimal_sep = config.get("money", {}).get("decimal_separator_word", "فاصلة")

    def verbalize(self, text: str) -> list:
        # Extraire le nombre (sans le %)
        m = re.search(r"(\d+)(?:[.,](\d+))?", text)
        if not m:
            return [text]

        int_part = m.group(1)
        dec_part = m.group(2)

        int_verbal = verbalize_number(str(int(int_part)))

        if dec_part and int(dec_part) != 0:
            dec_verbal = verbalize_number(str(int(dec_part)))
            amount = f"{int_verbal} {self._decimal_sep} {dec_verbal}"
        else:
            amount = int_verbal

        return [f"{amount} {self._suffix}"]