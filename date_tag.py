import pynini
from pynini.lib import pynutil

def build_date_tagger():

    digit = pynini.closure(pynini.union(*"0123456789"), 1)

    graph = (
        pynutil.insert('date { ') +
        pynutil.insert('day: "') + digit + pynutil.insert('" ') +
        pynutil.delete('/') +
        pynutil.insert('month: "') + digit + pynutil.insert('" ') +
        pynutil.delete('/') +
        pynutil.insert('year: "') + digit + pynutil.insert('" ') +
        pynutil.insert('}')
    )

    return graph.optimize()