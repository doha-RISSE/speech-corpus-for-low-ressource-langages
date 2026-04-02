import pynini

def generate_all(text, fst):
    lattice = pynini.accep(text) @ fst

    if lattice.start() == pynini.NO_STATE_ID:
        return []

    lattice = pynini.project(lattice, "output").rmepsilon()

    paths = lattice.paths(input_token_type="utf8", output_token_type="utf8")

    results = []

    while not paths.done():
        results.append(paths.ostring())
        paths.next()

    return list(set(results))