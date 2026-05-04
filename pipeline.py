from detector import detect_entities
from router import process_entity
from grammars.cardinal import CardinalFst
from config import CONFIG
from utils import generate_all


def fst_to_string(text, fst):
    results = generate_all(text, fst)
    return results[0] if results else text


def normalize(text):

    cardinal = CardinalFst().fst
    entities = detect_entities(text)

    outputs = []
    last = 0

    for e in entities:

        prefix = text[last:e["start"]]

        fst_result = process_entity(e, cardinal, CONFIG)
        candidates = generate_all(e["value"], fst_result)

        new_outputs = []

        for c in candidates:
            new_outputs.append(prefix + c)

        outputs = new_outputs if not outputs else [
            old + " " + new for old in outputs for new in new_outputs
        ]

        last = e["end"]

    return outputs

    cardinal = CardinalFst().fst
    entities = detect_entities(text)
    print("ENTITIES:", entities)
    results = [""]  # start with empty sentence

    last = 0

    for e in entities:
        print("ENTITY DETECTED:", e)

        prefix = text[last:e["start"]]

        fst_result = process_entity(e, cardinal, CONFIG)
        candidates = generate_all(e["value"], fst_result)

        new_results = []

        for r in results:
            for c in candidates:
                new_results.append(r + prefix + c)

        results = new_results

        last = e["end"]

    # add remaining text
    results = [r + text[last:] for r in results]

    return results
if __name__ == "__main__":

    text = " عندي موعد 12/05/2026"
    #text = " شريت هاد البيسي ب 8500  "
    print(normalize(text))