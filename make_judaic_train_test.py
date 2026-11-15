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

ds = load_dataset(
    "parquet",
    data_files="judaic-texts-corpus/**/*.parquet",
    split="train"
)


def clean_words(text):
    return re.findall(r"[\u05D0-\u05EA]+", text)


def classify(category):
    if not category:
        return None

    if category in [
        "תנך/תורה",
        "תנך/נביאים",
        "תנך/כתובים",
    ]:
        return "biblical_hebrew"

    if category.startswith("משנה/סדר "):
        return "rabbinic_hebrew"

    if category.startswith("תלמוד בבלי/סדר "):
        return "babylonian_talmud"

    if category.startswith("תלמוד ירושלמי/סדר "):
        return "jerusalem_talmud"

    if (
        "תרגום אונקלוס" in category
        or "תרגום יונתן" in category
        or "תרגום ירושלמי" in category
        or "תרגום ניאופיטי" in category
    ):
        return "targum_aramaic"

    if category == "קבלה/זהר":
        return "zohar_aramaic"

    if (
        category.startswith("הלכה/אחרונים")
        or category.startswith("שות/אחרונים")
    ):
        return "later_hebrew"

    return None


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

    document_id = (
        metadata.get("source_path")
        or metadata.get("book_name")
        or metadata.get("title")
        or f"row_{i}"
    )

    documents[group][document_id].extend(words)


print("\nBALANCED DOCUMENT-LEVEL TRAIN/TEST SPLIT\n")

for group, docs in documents.items():

    doc_items = list(docs.items())
    random.shuffle(doc_items)

    if len(doc_items) < 2:
        print(f"WARNING: {group} only has {len(doc_items)} document(s)")
        continue

    split_index = int(len(doc_items) * TRAIN_RATIO)
    split_index = max(1, min(split_index, len(doc_items) - 1))

    train_docs = doc_items[:split_index]
    test_docs = doc_items[split_index:]

    train_words = []
    test_words = []

    for _, words in train_docs:
        if len(train_words) >= MAX_TRAIN_WORDS:
            break

        needed = MAX_TRAIN_WORDS - len(train_words)
        train_words.extend(words[:needed])

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
    print(f"  train docs available: {len(train_docs)}")
    print(f"  test docs available:  {len(test_docs)}")
    print(f"  train words written:  {len(train_words)}")
    print(f"  test words written:   {len(test_words)}")
    print()