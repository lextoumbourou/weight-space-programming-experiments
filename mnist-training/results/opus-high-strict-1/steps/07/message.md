Step 6 of 15: validation loss 1.3076, accuracy 0.6173.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   773     7   156     0     0    24     2     0    29     0
               1     0   924    64     4    17    37    10     7     1     0
               2    22     7   563   254    26    59    27     3    28     1
               3     3     0     7   716     0   184     4     1   114     1
               4     2    25    21     8   550    10    37     2   215   113
               5     4     0     3    40     0   726   108     3    31     0
               6    52     3    10     8    16   234   611     0    32     1
               7     6     7   115   102    15    12     3   625    16   189
               8     8    12    72    71     3   105   225    10   442    61
               9    17     7    50    32     3    80    16    11   502   243

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.3782 | 0.4924
2 | 2.6052 | 0.5593
3 | 1.2434 | 0.5977
4 | 1.2769 | 0.5620
5 | 1.3371 | 0.6101
6 | 1.3076 | 0.6173

9 steps left. Reply with the complete build_weights() for step 7 in one Python code block.
