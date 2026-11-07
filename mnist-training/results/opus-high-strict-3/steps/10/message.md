Step 9 of 15: validation loss 0.9277, accuracy 0.7288.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   882    13    22     0     3     0    35     0    22    14
               1     0   989    39     1     1     0     1    22    11     0
               2    30    23   594    78    45     3     2    28   154    33
               3     9     6    14   647     0   215     5     4   124     6
               4     6    81     2     6   740    17     5     8    47    71
               5     8    10     0    77     4   446   116     8   195    51
               6    52    70     3     0    14     8   775     0    16    29
               7    19    16    20    19     6    47     1   852     4   106
               8    23    82    58   102     1     6    14    31   639    53
               9    24    46    11    21     9    39     4    66    17   724

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.8050 | 0.4403
2 | 1.0673 | 0.6866
3 | 1.3639 | 0.6626
4 | 2.2082 | 0.6541
5 | 1.0513 | 0.7082
6 | 1.0357 | 0.7054
7 | 1.6683 | 0.6427
8 | 0.9795 | 0.7212
9 | 0.9277 | 0.7288

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.
