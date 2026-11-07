Step 5 of 50: validation loss 0.9076, accuracy 0.7298.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   883    11    26     0     1     8    25     0    35     2
               1     0  1017     3     0     8     5     1    13    17     0
               2     7    16   530    71   114     4    17     2   229     0
               3     0     3    16   818     2   155     6    10    17     3
               4     7    47     1     1   674     0     3     0    47   203
               5     5     7     0    28     6   603   228     3    35     0
               6    39    29     0     0    42    33   803     0    18     3
               7    10    24   204    32    36    50     1   572    17   144
               8     2    73    18     5     5    12    95     8   689   102
               9    37    38    24    14    47     7    26     9    50   709

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2203 | 0.6525
2 | 1.0061 | 0.6721
3 | 1.9548 | 0.5810
4 | 0.9710 | 0.6862
5 | 0.9076 | 0.7298

At most 45 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 6 in one Python code block.
