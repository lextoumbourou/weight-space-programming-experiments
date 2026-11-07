Step 8 of 50: validation loss 1.0112, accuracy 0.6946.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   854    11    84     0     3     6    27     2     4     0
               1     0   992    37     0     9     3     1    22     0     0
               2    17    11   583   175    72    18    14     9    91     0
               3     3     6    19   826     5   118    13    24     8     8
               4     9    84    37     4   619     4    53     5    29   139
               5    34    17     7    28    14   655   108    35    11     6
               6    82    64     4     2    82   108   607     0    18     0
               7    35     5   150    15    22    66     1   738     2    56
               8    11    77   165    59    11    10    58    74   486    58
               9    68    51    55    17    35    13    10    64    62   586

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
8 | 1.0112 | 0.6946

At most 42 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 9 in one Python code block.
