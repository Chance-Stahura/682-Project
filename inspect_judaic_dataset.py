from datasets import load_dataset
from pathlib import Path
from collections import defaultdict
import random
import re

random.seed(42)

TRAIN_DIR = Path("judaic_languages")
TEST_DIR = Path("judaic_tests")

TRAIN_DIR.mkdir(exist_ok=True)
TEST_DIR.mkdir(exist_ok=True)

TRAIN_RATIO = 0.7

MAX_TRAIN_WORDS = 500_000
MAX_TEST_WORDS = 150_000

# Load local Parquet files
ds = load_dataset(
    "parquet",
    data_files="judaic-texts-corpus/**/*.parquet",
    split="train"
)


def clean_words(text):
    # Keep Hebrew-script letters only
    return re.findall(r"[\u05D0-\u05EA]+", text)


def classify(category):
    if not category:
        return None

    # Biblical Hebrew
    if category in [
        "תנך/תורה",
        "תנך/נביאים",
        "תנך/כתובים",
    ]:
        return "biblical_hebrew"

    # Rabbinic Hebrew / Mishnah
    if (
        category == "משנה"
        or category.startswith("משנה/סדר ")
    ):
        return "rabbinic_hebrew"

    # Babylonian Talmud
    if (
        category == "תלמוד/בבלי"
        or category.startswith("תלמוד/בבלי/")
        or category.startswith("תלמוד בבלי/סדר ")
    ):
        return "babylonian_talmud"

    # Jerusalem Talmud
    if (
        category == "תלמוד/ירושלמי"
        or category.startswith("תלמוד/ירושלמי/")
        or category.startswith("תלמוד ירושלמי/סדר ")
    ):
        return "jerusalem_talmud"

    # Targum Aramaic
    if any(x in category for x in [
        "תרגום אונקלוס",
        "תרגום יונתן",
        "תרגום ירושלמי",
        "תרגום ניאופיטי",
    ]):
        return "targum_aramaic"

    # Zoharic Aramaic
    if (
        category == "קבלה/זהר"
        or category.startswith("קבלה/זהר/")
    ):
        # Exclude translated Zohar
        if "מתורגם" not in category:
            return "zohar_aramaic"

    # Later Hebrew
    if (
        category.startswith("הלכה/אחרונים")
        or category.startswith("שות/אחרונים")
    ):
        return "later_hebrew"

    return None


# group -> document_id -> words
documents = defaultdict(lambda: defaultdict(list))

for i, row in enumerate(ds):
    metadata = row.get("metadata") or {}

    category = metadata.get("category")
    group = classify(category)

    if group is None:
        continue

    words = clean_words(row.get("text") or "")

    if not words:
        continue

    # One dataset row corresponds to one source text file.
    document_id = (
        metadata.get("source_path")
        or metadata.get("book_name")
        or metadata.get("title")
        or f"row_{i}"
    )

    documents[group][document_id].extend(words)


print("\nBALANCED DOCUMENT-LEVEL TRAIN/TEST SPLIT\n")

for group, docs in sorted(documents.items()):

    doc_items = list(docs.items())
    random.shuffle(doc_items)

    if len(doc_items) < 2:
        print(f"WARNING: {group} only has {len(doc_items)} document(s)")
        continue

    # Split whole documents, not individual words
    split_index = int(len(doc_items) * TRAIN_RATIO)
    split_index = max(1, min(split_index, len(doc_items) - 1))

    train_docs = doc_items[:split_index]
    test_docs = doc_items[split_index:]

    train_words = []
    test_words = []

    # Build balanced training corpus
    for _, words in train_docs:
        if len(train_words) >= MAX_TRAIN_WORDS:
            break

        needed = MAX_TRAIN_WORDS - len(train_words)
        train_words.extend(words[:needed])

    # Build balanced test corpus
    for _, words in test_docs:
        if len(test_words) >= MAX_TEST_WORDS:
            break

        needed = MAX_TEST_WORDS - len(test_words)
        test_words.extend(words[:needed])

    train_path = TRAIN_DIR / f"{group}.tra"
    test_path = TEST_DIR / f"{group}.tes"

    train_path.write_text(
        " ".join(train_words),
        encoding="utf-8"
    )

    test_path.write_text(
        " ".join(test_words),
        encoding="utf-8"
    )

    print(group)
    print(f"  total documents:       {len(doc_items)}")
    print(f"  train docs available:  {len(train_docs)}")
    print(f"  test docs available:   {len(test_docs)}")
    print(f"  train words written:   {len(train_words)}")
    print(f"  test words written:    {len(test_words)}")
    print()