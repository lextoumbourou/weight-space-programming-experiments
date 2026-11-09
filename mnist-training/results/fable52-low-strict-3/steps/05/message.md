Step 4 of 15: validation loss 1.0775, accuracy 0.7421.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   670     2     2     1     0     1   134     0   141    40
               1     1   932    57    11    13     0     0     3    35    12
               2     5     1   417   420    16     4     4     1    72    50
               3     0     0     1   980     5    35     0     1     6     2
               4     3    10     5     0   866     0     7     5    16    71
               5     3     1     1   167    17   619    26     0    76     5
               6    14     6     7     3    71     9   741     0    84    32
               7    10     2    10    79    53     5     0   595    21   315
               8     6    15     5    11    10     9    17    14   857    65
               9    11    10     0    11    40    10    43    59    33   744

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5340 | 0.7380
2 | 1.1300 | 0.7364
3 | 1.1663 | 0.6848
4 | 1.0775 | 0.7421

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
