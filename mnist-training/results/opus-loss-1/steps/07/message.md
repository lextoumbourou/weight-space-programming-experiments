Step 6 of 50: validation loss 1.0103, accuracy 0.6918.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   858    12    84     0     3     6    25     1     2     0
               1     0  1003    38     0     9     3     1    10     0     0
               2    18    12   595   197    65    18    17     8    60     0
               3     4     7    20   829     2   124    10    22     5     7
               4    11    93    45     6   615     4    54     3    17   135
               5    35    19     7    27    10   691    87    26     8     5
               6    93    72     5     3    73   117   596     0     8     0
               7    38     6   163    17    20    73     1   719     2    51
               8    15    81   189    83    10    17    59    68   426    61
               9    76    54    64    21    33    16    11    60    40   586

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3242 | 0.5148
2 | 1.1827 | 0.6054
3 | 1.0792 | 0.6656
4 | 1.0021 | 0.6869
5 | 1.3029 | 0.6276
6 | 1.0103 | 0.6918

At most 44 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 7 in one Python code block.
