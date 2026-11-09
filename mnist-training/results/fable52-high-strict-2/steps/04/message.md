Step 3 of 15: validation loss 0.8910, accuracy 0.7126.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   724    11    63     1     0     2   187     0     1     2
               1     0   978    55     4     6     0     3     8    10     0
               2    24    22   602   223     4     0    16    17    75     7
               3     2     2    30   876     0    30    17     4    68     1
               4     8    70    16    48   617     3   178     3    18    22
               5     5     5     4    66     0   541   191     2   100     1
               6    26    57     1     0     3     3   854     0    22     1
               7    16    14    11   176     9    20    30   624     6   184
               8     9    47    20    16     1     3    94     7   806     6
               9    24    29    14   115    11    36   186    25    17   504

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9981 | 0.6911
2 | 1.2553 | 0.6304
3 | 0.8910 | 0.7126

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
