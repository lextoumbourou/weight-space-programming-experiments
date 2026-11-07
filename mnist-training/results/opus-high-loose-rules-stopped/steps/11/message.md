Step 10 of 50: validation loss 1.0930, accuracy 0.7353.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   755     0     4     1     2     1   205     1     0    22
               1     3   685    13     3    44     1    87     6   195    27
               2     4     0   661    45    76     0    31    66    22    85
               3     0     0     2   730    12   102    78     6    76    24
               4     4     1     0     0   838     0    12     1    21   106
               5     5     1     0    18     3   618   111     1   140    18
               6     5     0     0     0    81     5   804     0     9    63
               7     1     0     4     6     0     0    20   730     9   320
               8     6     1    19     1    11     7   131    45   712    76
               9     2     0     0     5    17     2    33     9    73   820

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9468 | 0.2540
2 | 1.2629 | 0.5742
3 | 1.0920 | 0.6503
4 | 1.0095 | 0.7297
5 | 0.9636 | 0.7647
6 | 0.9087 | 0.8054
7 | 0.8223 | 0.7877
8 | 0.5529 | 0.8265
9 | 0.5545 | 0.8242
10 | 1.0930 | 0.7353

40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
