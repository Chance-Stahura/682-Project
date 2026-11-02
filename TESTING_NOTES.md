
Language ID Testing Notes

Training languages:
Arabic, German, Greek, English, Esperanto, French, Hebrew, Italian, Latin, Spanish, Turkish.

Tests:
- Hebrew real text
- Lorem Ipsum
- Rugg-style nonsense
- Transposed Latin

How to test:

Pattern method:
perl -I. langid_probdist.pl \
-c 'tests/*.tes' \
-p 'languages/*.tra' \
-d pattern

Unigram method:
perl -I. langid_probdist.pl \
-c 'tests/*.tes' \
-p 'languages/*.tra' \
-d unigram

Pattern results:
- Hebrew real -> Hebrew #1
- Lorem Ipsum -> Arabic #1, Hebrew #2
- Rugg-style nonsense -> Hebrew #1
- Transposed Latin -> Esperanto #1, Latin #3

Unigram results:
- Hebrew real -> Esperanto #1, Hebrew #2
- Lorem Ipsum -> Latin #1
- Rugg-style nonsense -> Italian #1
- Transposed Latin -> Latin #1