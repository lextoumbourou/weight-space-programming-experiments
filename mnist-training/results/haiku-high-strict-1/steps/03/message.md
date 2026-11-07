Step 2 of 15: validation loss 1.9985, accuracy 0.4359.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0    47     2   216    88     1   624     0    13     0     0
               1     0   878   122    55     6     3     0     0     0     0
               2     0     0   783    83    36    83     0     5     0     0
               3     0     5   227   602    22   153     0    21     0     0
               4     1    26    19    61   707   169     0     0     0     0
               5     0     2   141    94    14   659     0     5     0     0
               6     1    20   474   189    80   202     1     0     0     0
               7     4     7     8   310    16    60     1   682     0     2
               8     0    51   148   288    17   497     0     8     0     0
               9     0    30     3   362   127   421     0    18     0     0

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.6085 | 0.1223
2 | 1.9985 | 0.4359

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
