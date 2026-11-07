Step 4 of 50: validation loss 1.0095, accuracy 0.7297.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   831     0     3     1     2     0   134     0     0    20
               1     1   522   176    30     5     9   102    26   130    63
               2     5     0   637   201    19     2    25    25    39    37
               3     3     0    19   752     1   166    52     7    16    14
               4     1     1     0     3   641     1    36     1    16   283
               5     4     0     1    32     3   707    70    11    76    11
               6     0     0     0     1    24    19   880     0    13    30
               7     2     0    41    10     8     2    24   724     1   278
               8     9     0    22    31     2    13    66    13   723   130
               9     3     0     1    10     0     5    22    15    25   880

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9468 | 0.2540
2 | 1.2629 | 0.5742
3 | 1.0920 | 0.6503
4 | 1.0095 | 0.7297

46 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
