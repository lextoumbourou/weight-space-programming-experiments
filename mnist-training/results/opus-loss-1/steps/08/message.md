Step 7 of 50: validation loss 1.2342, accuracy 0.6404.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   767    17   183     0    16     2     0     6     0     0
               1     0  1033     9     0    10     0     0    12     0     0
               2    12    11   661    64   194    10     2    27     9     0
               3     7    10    61   672    30   137     4   105     0     4
               4     3   121    28     0   796     0     2     7     0    26
               5    38    12    21    18    75   623    22   101     0     5
               6    99    91    19     0   413    48   293     4     0     0
               7     9     0    79     7    21    15     0   947     0    12
               8    24    76   249    99    40    20    44   206   162    89
               9    70    42   100     8    73    16     0   201     1   450

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3242 | 0.5148
2 | 1.1827 | 0.6054
3 | 1.0792 | 0.6656
4 | 1.0021 | 0.6869
5 | 1.3029 | 0.6276
6 | 1.0103 | 0.6918
7 | 1.2342 | 0.6404

At most 43 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 8 in one Python code block.
