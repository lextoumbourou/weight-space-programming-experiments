Step 4 of 15: validation loss 2.1846, accuracy 0.2680.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   481    69    12     0     0     0     2     1   426     0
               1     0  1024    14     0     0     0     0    25     1     0
               2    15   170   287     0    16     1     0    16   483     2
               3     3   247    67    39    18     0     1   109   519    27
               4     0   421     0     0   243     0     1     3   315     0
               5     2   309    37     9     2     0     4    32   510    10
               6     2   407     9     0     0     0   156     0   393     0
               7     1   390     3     7    19     1     0   263   210   196
               8     0   667     5     1     3     0     0   165   165     3
               9     4   450     0     1    98     0     0     9   377    22

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 17.3035 | 0.3631
2 | 3.9784 | 0.3627
3 | 4.9236 | 0.1423
4 | 2.1846 | 0.2680

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
