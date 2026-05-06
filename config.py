# =============================================================================
#  config.py  —  SOURCE UNIQUE DE VÉRITÉ
#
#  Chaque clé de premier niveau = une classe sémantique.
#  Pour ajouter une nouvelle classe :
#    1. Ajouter son bloc ici
#    2. Créer grammars/<classe>.py avec une classe <Classe>Fst
#    3. C'est tout — router et detector la détectent automatiquement.
# =============================================================================

CONFIG = {

    # -------------------------------------------------------------------------
    #  CARDINAL  —  nombres isolés  (ex: "عندي 3 ديال الولاد")
    # -------------------------------------------------------------------------
    "cardinal": {
        "max_number": 1_000_000,
    },

    # -------------------------------------------------------------------------
    #  DATE  —  format attendu en entrée : JJ/MM/AAAA
    #
    #  Modes disponibles :
    #    "cardinal"   → verbalisation Darija  (طناش / خمسة / ألفين و ستة و عشرين)
    #    "number_raw" → chiffres bruts        (12 / 5 / 2026)
    #    "name"       → nom du mois           (ماي)  ← month_modes seulement
    #
    #  Activer plusieurs modes → toutes les variantes sont générées.
    # -------------------------------------------------------------------------
    "date": {
        "fst_max_number": 10_000,  # ← FST limité, les dates n'ont pas besoin de plus

        # Particules optionnelles avant la date verbalisée
        # "" = sans préfixe  |  "ف " ≈ "في"  |  "نهار " ≈ "يوم"
        "prefixes": ["", "ف ", "نهار "],

        "day_modes":   ["cardinal"],          # ex: ["cardinal", "number_raw"]
        "month_modes": ["cardinal", "name","name_fr"],  # ex: ["cardinal", "name", "number_raw"]
        "year_modes":  ["cardinal"],          # ex: ["cardinal", "number_raw"]

        # Mot entre le jour et le mois (modes cardinal/number_raw)
        # "طناش شهر خمسة"  — mettre "" pour supprimer
        "month_connector": "شهر",

        # Noms des mois (utilisés si "name" est dans month_modes)
        "months": {
            "01": "يناير",  "02": "فبراير", "03": "مارس",
            "04": "أبريل",  "05": "ماي",    "06": "يونيو",
            "07": "يوليوز", "08": "غشت",    "09": "شتنبر",
            "10": "أكتوبر", "11": "نونبر",  "12": "دجنبر",
        },
        "months_fr": {
            "01": "جونفيي",  "02": "فيفريي",  "03": "مارس",
            "04": "أفريل",   "05": "مي",      "06": "جوان",
            "07": "جويي",    "08": "أوت",     "09": "سبتمبر",
            "10": "أكتوبر",  "11": "نوفمبر",  "12": "ديسمبر",
        },
    },

    # -------------------------------------------------------------------------
    #  MONEY  —  "8500 درهم" | "MAD 8500" | "€ 250" | "8500.50 MAD"
    #
    #  verbalization_order :
    #    "amount_first"   → تمن مية و خمسين درهم
    #    "currency_first" → درهم تمن مية و خمسين
    #  (les deux valeurs → deux candidats générés)
    #
    #  decimal_separator_word :
    #    "فاصلة" → تمن مية فاصلة خمسين درهم
    #    "و"     → تمن مية و خمسين درهم
    # -------------------------------------------------------------------------
    "money": {

        "verbalization_order":    ["amount_first"],
        "decimal_separator_word": "فاصلة",

        # Ajouter une devise ici → reconnue partout (detector + parser + verbalizer)
        "currencies": {
            "MAD":   "درهم",
            "DH":    "درهم",
            "د.م":   "درهم",
            "درهم":  "درهم",
            "€":     "أورو",
            "EUR":   "أورو",
            "أورو":  "أورو",
            "$":     "دولار",
            "USD":   "دولار",
            "دولار": "دولار",
        },
    },

    # -------------------------------------------------------------------------
    #  CLASSES FUTURES — décommenter quand la grammaire sera prête
    # -------------------------------------------------------------------------

    # "time": {
    #     "prefixes": ["", "من الصباح ", "من الليل "],
    #     "formats":  ["24h", "12h"],
    # },

    # "ordinal": {
    #     "gender": ["masculine", "feminine"],   # الأول / الأولى
    # },

    # "phone": {
    #     "country_prefix": "212",
    #     "group_size": 2,      # 06 12 34 56 78
    # },
}