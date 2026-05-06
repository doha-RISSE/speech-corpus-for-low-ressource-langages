import pynini
from .base import GraphFst
from functools import lru_cache


def nombre_vers_darija(n):
    if not isinstance(n, int):
        raise ValueError("L'entrée doit être un entier.")

    if n == 0:
        return "صفر"

    unites         = ["", "واحد", "جوج", "تلاتة", "ربعة", "خمسة", "ستة", "سبعة", "تمنية", "تسعود"]
    dizaines_10_19 = ["عشرة", "حداش", "طناش", "تلطاش", "ربعطاش", "خمستاش", "سطاش", "سبعطاش", "تمنطاش", "تسعطاش"]
    dizaines       = ["", "عشرة", "عشرين", "تلاتين", "ربعين", "خمسين", "ستين", "سبعين", "تمنين", "تسعين"]
    centaines      = ["", "مية", "ميتين", "تلت مية", "ربع مية", "خمس مية", "ست مية", "سبع مية", "تمن مية", "تسع مية"]
    milliers_fuses = {
        3: "تلتالاف", 4: "ربعالاف", 5: "خمسالاف", 6: "ستالاف",
        7: "سبعالاف", 8: "تمنالاف", 9: "تسعالاف", 10: "عشرالاف"
    }

    def traiter_dizaines(num):
        if num < 10:
            return unites[num]
        elif num <= 19:
            return dizaines_10_19[num - 10]
        else:
            u, d = num % 10, num // 10
            nom_u = "تنين" if u == 2 else unites[u]
            return (dizaines[d] if u == 0 else nom_u + " و " + dizaines[d])

    def traiter_centaines(num):
        if num < 100:
            return traiter_dizaines(num)
        c, r = num // 100, num % 100
        return centaines[c] if r == 0 else centaines[c] + " و " + traiter_dizaines(r)

    if n < 1000:
        return traiter_centaines(n).strip()

    millier, reste = n // 1000, n % 1000

    if millier == 1:
        s = "الف"
    elif millier == 2:
        s = "الفين"
    elif 3 <= millier <= 10:
        s = milliers_fuses[millier]
    else:
        s = traiter_centaines(millier) + " الف"

    return (s if reste == 0 else s + " و " + traiter_centaines(reste)).strip()


@lru_cache(maxsize=None)
def verbalize_number(token: str) -> str:
    """Verbalise un token numérique à la demande, avec cache."""
    try:
        return nombre_vers_darija(int(token))
    except (ValueError, TypeError):
        return token


class CardinalFst(GraphFst):
    def __init__(self, config=None):
        super().__init__("cardinal")
        self._config = config
        self.fst = None  # pas précalculé

    def build_fst_for_date(self):
        if self.fst is None:
            # Lit depuis config["date"]["fst_max_number"], défaut 10_000
            max_number = 10_000
            if self._config and "date" in self._config:
                max_number = self._config["date"].get("fst_max_number", max_number)
            pairs = []
            for i in range(max_number):
                pairs.append((str(i), nombre_vers_darija(i)))
                if i < 10:
                    pairs.append((f"0{i}", nombre_vers_darija(i)))
            self.fst = pynini.string_map(pairs).optimize()
        return self.fst