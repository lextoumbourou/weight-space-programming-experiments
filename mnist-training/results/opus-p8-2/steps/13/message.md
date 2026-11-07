Step 12 of 50: validation loss 0.9999, accuracy 0.6808.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   733    11    77     7     6    66    44     4    42     1
               1     0   880    62     3    12     0     0   105     1     1
               2     2     4   567   237   106     6     2     8    50     8
               3     0     2    17   913     5    30     1    26    28     8
               4     1    26    49     5   807     2    19     7    43    24
               5     2     4     2    52    37   741    55     3    17     2
               6    37    33    12    16   176    12   631     3    46     1
               7     8     9   134    86   102    47     8   590    17    89
               8     4    66   106    21    18    28   144    76   460    86
               9    24    32    25    22   135    62    54    30    91   486

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4065 | 0.6314
2 | 1.8335 | 0.5049
3 | 1.3679 | 0.6182
4 | 1.7558 | 0.5974
5 | 1.3255 | 0.5417
6 | 1.1397 | 0.6529
7 | 1.3018 | 0.5786
8 | 1.0999 | 0.6685
9 | 1.0772 | 0.6831
10 | 1.0621 | 0.6789
11 | 0.9904 | 0.6924
12 | 0.9999 | 0.6808

At most 38 steps left. Reply with the complete build_weights() for step 13 in one Python code block.
