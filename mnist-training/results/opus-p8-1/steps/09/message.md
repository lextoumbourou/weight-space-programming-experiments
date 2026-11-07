Step 8 of 50: validation loss 4.7657, accuracy 0.5293.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   702    31   250     1     0     3     1     3     0     0
               1     0   996    12     0     0     0     0    56     0     0
               2    23   145   674    70     1     5     7    65     0     0
               3    13   102    55   590     0    78    10   180     0     2
               4     6   528    98     8   282     0    14    33     0    14
               5    12   224    25    77     1   384   145    46     0     1
               6    79   310    58     2     8     0   509     1     0     0
               7     5    99    58     5     2    26     0   888     0     7
               8    22   298   345    32     3     2    86   124    81    16
               9    80   265   142    11     9    24    11   232     0   187

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.7511 | 0.3148
2 | 1.2930 | 0.6248
3 | 1.5677 | 0.5552
4 | 1.3191 | 0.5505
5 | 1.2707 | 0.6192
6 | 1.8067 | 0.6464
7 | 1.3242 | 0.6409
8 | 4.7657 | 0.5293

At most 42 steps left. Reply with the complete build_weights() for step 9 in one Python code block.
