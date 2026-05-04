import re

PATTERNS = {
    "money": r"\b\d+\s?(MAD|€|\$|درهم|أورو|دولار)\b|\b(MAD|€|\$|درهم|أورو|دولار)\s?\d+\b",
    "date": r"\b\d{1,2}/\d{1,2}/\d{4}\b"
}


def detect_entities(text):
    entities = []

    for label, pattern in PATTERNS.items():
        for m in re.finditer(pattern, text):
            entities.append({
                "type": label,
                "value": m.group(),
                "start": m.start(),
                "end": m.end()
            })

    return sorted(entities, key=lambda x: x["start"])