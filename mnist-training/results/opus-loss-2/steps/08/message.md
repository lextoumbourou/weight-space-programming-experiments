Step 7 of 50: validation loss 0.8256, accuracy 0.7435.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   875     9    64     0     3     9    17     2    11     1
               1     0  1004    10     0     8     5     1    26    10     0
               2     4    15   628    73   102     4    11     5   148     0
               3     0     3    37   798     3   152     2    20    11     4
               4     7    41     2     1   719     0     1     4    35   173
               5     5     6     3    43    11   591   205     5    46     0
               6    46    31     1     0    73    34   759     0    20     3
               7    12    15   128    24    36    78     1   720     9    67
               8     2    67    54    11     6    14    69    22   667    97
               9    39    32    40    21    59    10    18    25    43   674

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2203 | 0.6525
2 | 1.0061 | 0.6721
3 | 1.9548 | 0.5810
4 | 0.9710 | 0.6862
5 | 0.9076 | 0.7298
6 | 0.8788 | 0.7393
7 | 0.8256 | 0.7435

At most 43 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 8 in one Python code block.
