Step 11 of 50: validation loss 0.9904, accuracy 0.6924.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   762    10   100     2     2    48    45     4    18     0
               1     0   853    77     3    11     0     0   119     1     0
               2     5     3   564   274    83     5     4    10    38     4
               3     0     2    18   928     4    37     1    21    11     8
               4     1    22    58     6   799     1    19     7    41    29
               5     4     3     3    51    22   764    57     4     7     0
               6    43    29    12    15   145    13   692     2    16     0
               7    12     8   128    89    71    54     6   634     7    81
               8     5    52   154    38    12    33   127    80   426    82
               9    38    31    43    23   103    65    40    36    80   502

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

At most 39 steps left. Reply with the complete build_weights() for step 12 in one Python code block.
