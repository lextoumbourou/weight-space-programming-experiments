Step 3 of 50: validation loss 1.0792, accuracy 0.6656.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   858    12    72     0     0     3    42     1     3     0
               1     1  1019    37     0     1     5     1     0     0     0
               2    22    21   617   155     7    23    39     5   101     0
               3     5    11    22   805     0   122    33    17     6     9
               4    12   151    26     1   284     3   128     0    43   335
               5    40    33     6    19     1   623   168     5     8    12
               6    73    81     2     0     1    96   699     0    14     1
               7    36    17   217    20    10    73     2   613     2   100
               8    13   102   168    38     1    12    81    29   483    82
               9    65    78    57     9     2     8    17    21    49   655

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3242 | 0.5148
2 | 1.1827 | 0.6054
3 | 1.0792 | 0.6656

At most 47 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 4 in one Python code block.
