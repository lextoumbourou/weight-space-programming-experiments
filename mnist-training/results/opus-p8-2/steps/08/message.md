Step 7 of 50: validation loss 1.3018, accuracy 0.5786.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   623    15   155     4     6   182     3     2     0     1
               1     0   902    81     1     9     2     0    69     0     0
               2     0    20   562   258    68    49     0    33     0     0
               3     0     7    19   814     1   144     0    45     0     0
               4     0    61    68     0   833    11     3     2     0     5
               5     1    13    22    59    13   797     6     4     0     0
               6     4    84    48    41   228   189   373     0     0     0
               7     4    10    97    39    76   131     0   719     0    14
               8     1   117   353   199    17   201    18    93     0    10
               9     6    63    82    16   230   321     3    77     0   163

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

At most 43 steps left. Reply with the complete build_weights() for step 8 in one Python code block.
