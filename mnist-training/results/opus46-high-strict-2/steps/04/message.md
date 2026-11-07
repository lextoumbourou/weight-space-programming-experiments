Step 3 of 15: validation loss 1.8248, accuracy 0.3637.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   500     1    88    52     0   146     6    27   158    13
               1     0   603    35     3     0     6     0   413     4     0
               2     0     4   556   279     4    32    38    17    60     0
               3     0    35    64   620    39    55     5    94    56    62
               4     1    23    14     6   264     0     5    22   648     0
               5     1     4    60    60    20   348    82    81   181    78
               6     3    14    59    26     2    24   380     9   450     0
               7     4    31     3   415    26    24     0   222   127   238
               8     0    31   236    93    21   102    10   388   121     7
               9     6    30     1    37    83    14     1   121   645    23

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.4126 | 0.1130
2 | 1.9302 | 0.3116
3 | 1.8248 | 0.3637

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
