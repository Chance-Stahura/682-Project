from datasets import load_dataset

currier = load_dataset(
    "Ched-ai/voynich-transliterations",
    "cd",
    split="train"
)

# for local testing: see how currier transliteration is structured
# prints first three lines
#for row in currier.select(range(3)):
    #print(row["line_id"], row["text_raw"])

currier.to_json(
    "data/raw_data/currier.jsonl",
    force_ascii=False
)