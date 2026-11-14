Step 2 of 50: training loss 1.1281, accuracy 0.6957.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   675    13   162     3     0    59    78     1     0     0
               1     0   980    54     1     5     0     0    19     5     0
               2    13    30   496   373     3     5     4    21    29    16
               3     0     0    16   881     0   112     2    14     4     1
               4     7    90    52    47   472     4    43    35     3   230
               5     4     5    11   100     0   740    29    14    11     1
               6    41   122    20     2     2    93   682     0     1     4
               7     4     3    41    45    21    25     0   854     0    97
               8     7    81    30   102     2    39    74    45   564    65
               9    22    31    22   105    14    41    15    98     0   613

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6415 | 0.6010
2 | 1.1281 | 0.6957

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.

