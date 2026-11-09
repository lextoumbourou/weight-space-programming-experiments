Step 1 of 15: validation loss 0.9981, accuracy 0.6911.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   778     4    25     0     0     5   170     0     0     9
               1     0   870    72     2    21     0     1    79     9    10
               2    33     1   420   341    13     0     9    19    77    77
               3     5     0     3   895     1    81     5     6    32     2
               4    24     9    24    33   545     5    78     9    29   227
               5     4     1     2   150     3   641    59     6    46     3
               6   115    24     1     0    31    28   739     0    18    11
               7    25     2    12    32    20    90    19   692     2   196
               8    32    19    16    34     4    13    38    31   790    32
               9    53     2     6   115     9   100    74    55     6   541

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9981 | 0.6911

14 steps left. Reply with the complete build_weights() for step 2 in one Python code block.
