import pynini
from pynini.lib import pynutil


def _value_graphs(cardinal_fst, modes):
    """
    Retourne une liste de graphes FST pour une valeur numérique
    selon les modes activés dans config.
      "cardinal"   → FST cardinal (verbalisé en Darija)
      "number_raw" → accepte les chiffres tels quels (identité)
    """
    graphs = []
    if "cardinal" in modes:
        graphs.append(cardinal_fst)
    if "number_raw" in modes:
        digit = pynini.closure(pynini.union(*"0123456789"), 1)
        graphs.append(digit)
    if not graphs:
        graphs.append(cardinal_fst)   # fallback
    return graphs


def build_date_verbalizer(cardinal_fst, config):
    """
    Construit le FST de verbalization de date à partir de config["date"].

    Entrée  (depuis date_tag.py) :
        date { day: "12" month: "05" year: "2026" }

    Sorties (exemples avec config par défaut) :
        طناش ماي ألفين و ستة و عشرين
        طناش شهر خمسة ألفين و ستة و عشرين
        نهار طناش ماي ألفين و ستة و عشرين
        ف طناش شهر خمسة ألفين و ستة و عشرين
        ...
    """
    cfg       = config["date"]
    connector = cfg.get("month_connector", "شهر")

    # ------------------------------------------------------------------
    # Préfixes
    # ------------------------------------------------------------------
    prefix_graph = pynini.union(
        *[pynutil.insert(p) for p in cfg["prefixes"]]
    )

    # ------------------------------------------------------------------
    # Jour
    # ------------------------------------------------------------------
    day_gs = _value_graphs(cardinal_fst, cfg.get("day_modes", ["cardinal"]))
    day    = pynini.union(*day_gs)

    # ------------------------------------------------------------------
    # Mois
    # ------------------------------------------------------------------
    month_graphs = []

    if "cardinal" in cfg["month_modes"]:
        sep = pynutil.insert(f" {connector} ") if connector else pynutil.insert(" ")
        month_graphs.append(sep + cardinal_fst)

    if "number_raw" in cfg["month_modes"]:
        digit = pynini.closure(pynini.union(*"0123456789"), 1)
        sep   = pynutil.insert(f" {connector} ") if connector else pynutil.insert(" ")
        month_graphs.append(sep + digit)

    if "name" in cfg["month_modes"]:
        month_names = pynini.string_map(list(cfg["months"].items()))
        month_graphs.append(pynutil.insert(" ") + month_names)
    if "name_fr" in cfg["month_modes"]:
        month_names_fr = pynini.string_map(list(cfg["months_fr"].items()))
        month_graphs.append(pynutil.insert(" ") + month_names_fr)
    

    month = pynini.union(*month_graphs)

    # ------------------------------------------------------------------
    # Année
    # ------------------------------------------------------------------
    year_gs = _value_graphs(cardinal_fst, cfg.get("year_modes", ["cardinal"]))
    year    = pynutil.insert(" ") + pynini.union(*year_gs)

    # ------------------------------------------------------------------
    # Assemblage
    # ------------------------------------------------------------------
    graph = (
        pynutil.delete('date { day: "') +
        prefix_graph +
        day +
        pynutil.delete('" month: "') +
        month +
        pynutil.delete('" year: "') +
        year +
        pynutil.delete('" }')
    )

    return graph.optimize()