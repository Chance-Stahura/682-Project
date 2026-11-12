# Judaic Language Identification Experiment

This experiment tests `langid_probdist.pl` on seven Hebrew/Aramaic textual varieties from the `NHLOCAL/judaic-texts-corpus` dataset:

- Biblical Hebrew
- Rabbinic Hebrew
- Babylonian Talmud
- Jerusalem Talmud
- Targum Aramaic
- Zohar Aramaic
- Later Hebrew

## Dataset

The dataset is **not included in this repository** and should be downloaded locally because it is listed in `.gitignore`.

Download it from:

`NHLOCAL/judaic-texts-corpus`

The scripts expect the dataset to exist locally as:

```text
judaic-texts-corpus/
```

with Parquet files inside it.

## Train/Test Setup

Training and testing are split by **source document**, not by individual words, to avoid train/test leakage.

Each class is balanced to:

```text
500,000 training words
150,000 testing words
```

Generate the files with:

```bash
python make_judaic_train_test.py
```

This creates:

```text
judaic_languages/*.tra
judaic_tests/*.tes
```

## Pattern Test

```bash
perl -I. langid_probdist.pl \
-c 'judaic_tests/*.tes' \
-p 'judaic_languages/*.tra' \
-d pattern
```

Result:

```text
4 / 7 correct
57.1% accuracy
```

Incorrect classifications:

```text
Babylonian Talmud -> Rabbinic Hebrew
Targum Aramaic    -> Rabbinic Hebrew
Zohar Aramaic     -> Rabbinic Hebrew
```

## Unigram Test

```bash
perl -I. langid_probdist.pl \
-c 'judaic_tests/*.tes' \
-p 'judaic_languages/*.tra' \
-d unigram
```

Result:

```text
6 / 7 correct
85.7% accuracy
```

Only incorrect classification:

```text
Zohar Aramaic -> Babylonian Talmud
```

## Summary

```text
Pattern:  57.1%
Unigram:  85.7%
```

For these closely related Hebrew and Aramaic varieties, unigram distributions performed substantially better than decomposition-pattern distributions.

Note: the `ACCURACY: 0.0000` printed by the Perl script should be ignored for these custom filenames. The accuracies above were calculated from the rank-1 predictions.