from .base import GraphFst
from .cardinal import nombre_vers_darija


HEURES_MAP = {
    1: "الوحدة",  2: "الجوج",    3: "التلاتة", 4: "الربعة",
    5: "الخمسة",  6: "الستة",    7: "السبعة",  8: "التمنية",
    9: "التسعود", 10: "العشرة",  11: "الحداش", 12: "الطناش"
}

MINUTES_IDIOM = {
    0:  "بيلا",
    5:  "وقسم",
    10: "وقسمين",
    15: "وربع",
    20: "وتلت",
    25: "وخمسة وعشرين",
    30: "ونص",
    35: "قل خمسة وعشرين",
    40: "قل تلت",
    45: "لارب",
    50: "قل قسمين",
    55: "قل قسم",
}


class TimeFst(GraphFst):
    """
    Verbalise une heure au format HH:MM en Darija.
    Génère jusqu'à deux candidats selon les modes activés dans config["time"]["modes"] :
      "idiomatic" → الجوج وربع  /  التلاتة قل تلت
      "literal"   → الجوج و خمستاش
    """

    def __init__(self, config):
        super().__init__("time")
        self._modes = config.get("time", {}).get("modes", ["idiomatic", "literal"])

    def verbalize(self, text: str) -> list:
        import re
        m = re.search(r"([0-2]?[0-9])[:hH]([0-5][0-9])", text)
        if not m:
            return [text]

        heure  = int(m.group(1))
        minute = int(m.group(2))

        results = []

        if "idiomatic" in self._modes:
            results.append(self._idiomatic(heure, minute))

        if "literal" in self._modes:
            results.append(self._literal(heure, minute))

        return list(dict.fromkeys(results))  # déduplique en gardant l'ordre

    # ------------------------------------------------------------------

    def _heure_12(self, heure):
        h = heure % 12
        return h if h != 0 else 12

# Remplacer la méthode _literal par celle-ci :

    def _minutes_non_idiomatiques(self, minute: int) -> str:
        if minute == 1:
            return "ودقيقة"
        elif 2 <= minute <= 10:
            return "و " + nombre_vers_darija(minute) + " دقايق"
        else:
            return "و " + nombre_vers_darija(minute) + " دقيقة"
    def _idiomatic(self, heure, minute) -> str:
        h12 = self._heure_12(heure)

        if minute in MINUTES_IDIOM and minute > 30:
            h12 = h12 + 1
            if h12 > 12:
                h12 = 1

        texte_heure = HEURES_MAP[h12]

        if minute in MINUTES_IDIOM:
            texte_minute = MINUTES_IDIOM[minute]
        else:
            texte_minute = self._minutes_non_idiomatiques(minute)  # ← fallback mis à jour

        return f"{texte_heure} {texte_minute}".strip()
    def _literal(self, heure, minute) -> str:
        h12         = self._heure_12(heure)
        texte_heure = HEURES_MAP[h12]

        if minute == 0:
            texte_minute = "بيلا"
        else:
            texte_minute = self._minutes_non_idiomatiques(minute)  # ← remplace l'ancien "و " + cardinal

        return f"{texte_heure} {texte_minute}".strip()