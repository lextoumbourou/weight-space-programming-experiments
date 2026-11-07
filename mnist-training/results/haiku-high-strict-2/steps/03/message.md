Step 2 of 15: validation loss 3.5391, accuracy 0.1546.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     0     0   966     0    13    12     0     0     0     0
               1     0     0  1062     0     0     2     0     0     0     0
               2     0     0   958     0    32     0     0     0     0     0
               3     0     0   992    10     2    26     0     0     0     0
               4     0     0   506     0   476     1     0     0     0     0
               5     0     0   794     3    16   102     0     0     0     0
               6     0     0   942     0    20     5     0     0     0     0
               7     0     0   900    86    94    10     0     0     0     0
               8     0     0  1000     0     2     7     0     0     0     0
               9     0     0   790    18   146     7     0     0     0     0

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.6151 | 0.1010
2 | 3.5391 | 0.1546

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
