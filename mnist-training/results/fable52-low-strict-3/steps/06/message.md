Step 5 of 15: validation loss 1.0404, accuracy 0.7677.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   769     3     8     1     0     4   161     0    38     7
               1     4   919    91     9    12     2     0     8     7    12
               2    56     1   605   243    19    10     5     3    31    17
               3     2     0     3   908     4   107     0     2     3     1
               4    17     9     6     0   907     1    16     7     4    16
               5     9     1     3   103     6   747    38     0     7     1
               6    64     5     8     0    57    20   805     0     3     5
               7   117     0    13    68    55    19     8   699     6   105
               8    17    20    18    12    15    68    50    32   722    55
               9    44     8     0     9    51    61    75    98    19   596

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5340 | 0.7380
2 | 1.1300 | 0.7364
3 | 1.1663 | 0.6848
4 | 1.0775 | 0.7421
5 | 1.0404 | 0.7677

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
