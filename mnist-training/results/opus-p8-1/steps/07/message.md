Step 6 of 50: validation loss 1.8067, accuracy 0.6464.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   744     8   205     0     0    10     2     1    20     1
               1     0   885   133     0     1     4     3    37     0     1
               2    12    11   677    82     4    15    22     5   162     0
               3     2     2    35   750     0   150     6    12    69     4
               4     2    48   121    13   574     0    20     4   134    67
               5     3     8    33    84     0   493   226     2    62     4
               6    32    36    26     6     8     4   759     0    96     0
               7     3     9   161    28     8   160     0   581     4   136
               8     4    48   318     7     2     4    21    17   556    32
               9    29    31   139     8    34    44    12    26   193   445

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.7511 | 0.3148
2 | 1.2930 | 0.6248
3 | 1.5677 | 0.5552
4 | 1.3191 | 0.5505
5 | 1.2707 | 0.6192
6 | 1.8067 | 0.6464

At most 44 steps left. Reply with the complete build_weights() for step 7 in one Python code block.
