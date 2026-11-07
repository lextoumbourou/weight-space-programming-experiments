Step 4 of 15: validation loss 1.9442, accuracy 0.3359.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   484    67     0    14     2     0   408     6     5     5
               1     0   835     0     0     0     1     0   228     0     0
               2    19   352   282   116     6     4    16   163    26     6
               3     0   547     8   322     4    79    19    16    15    20
               4     4   392     0     0   260     1   143    53    33    97
               5    13   507     1    19    26   188    74    16    50    21
               6    18   351     8     0    15     6   530     0    39     0
               7     2   403     0    19    43     9    14    59     1   540
               8     3   717    11     6     9    14     6   110   124     9
               9    14   563     0     3    58    10    25    10     3   275

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 9.5504 | 0.1653
2 | 2.2641 | 0.1767
3 | 2.5593 | 0.3107
4 | 1.9442 | 0.3359

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
