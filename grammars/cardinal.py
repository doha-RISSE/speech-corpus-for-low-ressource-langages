import pynini
from .base import GraphFst

def nombre_vers_darija(n):
    """
    Convertit un entier en sa verbalisation en Darija marocaine (script arabe).
    Gère les nombres de 0 à 999 999.
    """
    if not isinstance(n, int):
        raise ValueError("L'entrée doit être un entier.")

    if n == 0:
        return "صفر"

    # Dictionnaires de base pour la Darija
    unites = ["", "واحد", "جوج", "تلاتة", "ربعة", "خمسة", "ستة", "سبعة", "تمنية", "تسعود"]
    dizaines_10_19 = ["عشرة", "حداش", "طناش", "تلطاش", "ربعطاش", "خمستاش", "سطاش", "سبعطاش", "تمنطاش", "تسعطاش"]
    dizaines = ["", "عشرة", "عشرين", "تلاتين", "ربعين", "خمسين", "ستين", "سبعين", "تمنين", "تسعين"]

    # En Darija, les centaines sont souvent fusionnées ou écrites séparément.
    # Ex: تلت مية (300). On les code en dur pour plus de fluidité.
    centaines = ["", "مية", "ميتين", "تلت مية", "ربع مية", "خمس مية", "ست مية", "سبع مية", "تمن مية", "تسع مية"]

    def traiter_dizaines(num):
        if num < 10:
            return unites[num]
        elif 10 <= num <= 19:
            return dizaines_10_19[num - 10]
        else:
            unite = num % 10
            dizaine = num // 10
            if unite == 0:
                return dizaines[dizaine]
            else:
                # Règle : Unité + " و " + Dizaine (ex: 21 -> واحد و عشرين)
                return unites[unite] + " و " + dizaines[dizaine]

    def traiter_centaines(num):
        if num < 100:
            return traiter_dizaines(num)
        else:
            centaine = num // 100
            reste = num % 100
            if reste == 0:
                return centaines[centaine]
            else:
                return centaines[centaine] + " و " + traiter_dizaines(reste)

    # Logique principale pour assembler le tout
    if n < 1000:
        return traiter_centaines(n).strip()

    # Traitement des milliers
    millier = n // 1000
    reste = n % 1000

    str_millier = ""
    if millier == 1:
        str_millier = "الف"
    elif millier == 2:
        str_millier = "الفين"
    elif 3 <= millier <= 10:
        # Pour 3000 à 10000, on utilise le pluriel "آلاف" (ex: تلت آلاف)
        str_millier = traiter_dizaines(millier) + " آلاف"
    else:
        # Au-delà de 10000, on utilise le singulier "الف" (ex: خمسين الف)
        str_millier = traiter_centaines(millier) + " الف"

    if reste == 0:
        return str_millier.strip()
    else:
        return (str_millier + " و " + traiter_centaines(reste)).strip()



class CardinalFst(GraphFst):
    def __init__(self, max_number=10000):
        super().__init__("cardinal")

        pairs = []
        for i in range(max_number):
            pairs.append((str(i), nombre_vers_darija(i)))
            if i < 10:
                pairs.append((f"0{i}", nombre_vers_darija(i)))

        self.fst = pynini.string_map(pairs).optimize()