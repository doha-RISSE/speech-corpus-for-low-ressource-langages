import re

CURRENCY = r"(MAD|€|\$|درهم|أورو|دولار)"

def parse_money(text):

    text = re.sub(r"\s+", " ", text.strip())

    # 8500 درهم
    m = re.search(rf"(\d+(?:\.\d+)?)\s*{CURRENCY}", text)
    if m:
        return m.group(1), re.search(CURRENCY, text).group()

    # درهم 8500
    m = re.search(rf"{CURRENCY}\s*(\d+(?:\.\d+)?)", text)
    if m:
        return m.group(1), re.search(CURRENCY, text).group()

    # fallback → nombre seul
    m = re.search(r"(\d+(?:\.\d+)?)", text)
    if m:
        return m.group(1), "درهم"

    return None, None