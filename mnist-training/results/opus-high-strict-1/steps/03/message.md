Step 2 of 15: validation loss 2.6052, accuracy 0.5593.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   644     4   208    31     0     6    63     3    32     0
               1     0   826   118     1     4     6     0   109     0     0
               2     6    22   501   204     5     5    16    18   190    23
               3     4     1    88   695     0    29     2     6   202     3
               4     1    75   109    20   424    13    47    87    33   174
               5    10     2    22    89     1   400   108     5   277     1
               6    54    41     7    39     2    56   654     2   110     2
               7     5    30   233    44    26     7     1   656    15    73
               8     5    39   167    47     3    15   162    25   523    23
               9    31    35   121    32    33    15    77   102   245   270

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.3782 | 0.4924
2 | 2.6052 | 0.5593

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
