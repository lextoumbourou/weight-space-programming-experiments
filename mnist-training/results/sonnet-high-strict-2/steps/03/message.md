Step 2 of 15: validation loss 2.2641, accuracy 0.1767.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   490   316    29    33    16     0    26     0    78     3
               1     0  1059     0     0     0     0     0     0     5     0
               2     3   636     3   118    17     0     0     2   210     1
               3     1   933     1    17     0     0     0     1    58    19
               4     0   489     0     2    40     0     8     0   444     0
               5     3   730     0     1     2    25     6     2   122    24
               6     1   541     0     2     0     0    68     0   355     0
               7     1   902     0     0    10     0     0    17    65    95
               8     1   967     1     0     0     0     4     1    34     1
               9     5   754     0     0    15     2     0     2   169    14

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 9.5504 | 0.1653
2 | 2.2641 | 0.1767

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
