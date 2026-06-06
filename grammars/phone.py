from .base import GraphFst
from .cardinal import verbalize_number


class PhoneFst(GraphFst):
    """
    Verbalise un numéro de téléphone marocain (10 chiffres).
    Lecture : 2 premiers chiffres isolés, puis groupes de 2.
    Ex: 0612345678 → صفر ستة طناش ربعة وتلاتين ستة وخمسين تمنية وسبعين
    """

    def __init__(self, config):
        super().__init__("phone")
        self._cfg = config.get("phone", {})

    def verbalize(self, text: str) -> list:
        # Nettoyer : garder uniquement les chiffres
        digits = "".join(c for c in text if c.isdigit())

        if len(digits) != 10:
            return [text]

        parts = []

        # Les 2 premiers chiffres lus individuellement (chiffre par chiffre)
        parts.append(verbalize_number(digits[0]))   # "0" → صفر
        parts.append(verbalize_number(digits[1]))   # "6" → ستة

        # Les 8 chiffres restants : groupes de 2
        for i in range(2, 10, 2):
            group = digits[i:i+2]
            # Lire comme entier (ex: "06" → 6 → ستة, "12" → 12 → طناش)
            parts.append(verbalize_number(str(int(group))))

        return [" ".join(parts)]