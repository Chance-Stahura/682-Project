from pathlib import Path
import random
import re

random.seed(42)

OUT = Path("tests")
OUT.mkdir(exist_ok=True)

TARGET_WORDS = 1500


# ------------------------------------------------------------
# 1. LOREM IPSUM
# ------------------------------------------------------------

LOREM = """
Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur Excepteur sint occaecat cupidatat non proident sunt
in culpa qui officia deserunt mollit anim id est laborum
"""

lorem_words = LOREM.lower().split()

lorem_output = [
    lorem_words[i % len(lorem_words)]
    for i in range(TARGET_WORDS)
]

(OUT / "lorem_ipsum.tes").write_text(
    " ".join(lorem_output),
    encoding="utf-8"
)


# ------------------------------------------------------------
# 2. RUGG-STYLE HOAX TEXT
# ------------------------------------------------------------

PREFIXES = [
    "", "", "", "q", "ch", "sh", "qo", "ol",
    "d", "s", "y", "k", "t", "p", "f"
]

MIDDLES = [
    "o", "a", "e", "ee", "ai", "ol", "or",
    "ar", "al", "edy", "ed", "eo", "iin",
    "ii", "i", "che", "she"
]

SUFFIXES = [
    "", "", "y", "dy", "in", "iin", "ain",
    "aiin", "ol", "or", "ar", "al", "ey",
    "edy", "am"
]


def make_rugg_word():
    word = (
        random.choice(PREFIXES)
        + random.choice(MIDDLES)
        + random.choice(SUFFIXES)
    )

    if random.random() < 0.18:
        word += random.choice(MIDDLES)

    return word


rugg_words = [
    make_rugg_word()
    for _ in range(TARGET_WORDS)
]

(OUT / "rugg_hoax.tes").write_text(
    " ".join(rugg_words),
    encoding="utf-8"
)


# ------------------------------------------------------------
# 3. TRANSPOSED LATIN
# ------------------------------------------------------------

LATIN = """
Gallia est omnis divisa in partes tres quarum unam incolunt Belgae aliam
Aquitani tertiam qui ipsorum lingua Celtae nostra Galli appellantur Hi omnes
lingua institutis legibus inter se differunt Gallos ab Aquitanis Garumna
flumen a Belgis Matrona et Sequana dividit Horum omnium fortissimi sunt
Belgae propterea quod a cultu atque humanitate provinciae longissime absunt
minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos
animos pertinent important proximique sunt Germanis qui trans Rhenum
incolunt quibuscum continenter bellum gerunt Qua de causa Helvetii quoque
reliquos Gallos virtute praecedunt quod fere cotidianis proeliis cum Germanis
contendunt cum aut suis finibus eos prohibent aut ipsi in eorum finibus
bellum gerunt
"""


def clean_words(text):
    return re.findall(r"[A-Za-z]+", text.lower())


latin_words = clean_words(LATIN)

latin_words = [
    latin_words[i % len(latin_words)]
    for i in range(TARGET_WORDS)
]


def transpose_word(word):
    chars = list(word)

    if len(chars) <= 1:
        return word

    original = chars[:]

    for _ in range(10):
        random.shuffle(chars)
        if chars != original:
            break

    return "".join(chars)


transposed = [
    transpose_word(word)
    for word in latin_words
]

(OUT / "transposed_latin.tes").write_text(
    " ".join(transposed),
    encoding="utf-8"
)


# ------------------------------------------------------------
# REPORT
# ------------------------------------------------------------

print("Created:")

for filename in [
    "lorem_ipsum.tes",
    "rugg_hoax.tes",
    "transposed_latin.tes",
]:
    path = OUT / filename
    words = path.read_text(encoding="utf-8").split()
    avg_len = sum(map(len, words)) / len(words)

    print(
        f"  {path}: "
        f"{len(words)} words, "
        f"average length {avg_len:.2f}"
    )