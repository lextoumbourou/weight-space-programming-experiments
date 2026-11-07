Step 2 of 15: validation loss 1.3882, accuracy 0.6128.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   787     8    55    10    14    89    25     3     0     0
               1     0   833    39     0    55     0     2   135     0     0
               2     5     7   516   241   203     7     6     5     0     0
               3     0     2     9   850     7   151     1     8     0     2
               4     3     7    12    16   891     0     4     7     0    43
               5     9     4     0    90   101   634    62     7     0     8
               6    35    14     1    32   291    88   503     1     1     1
               7    34     2   156   132   135    33     0   587     0    11
               8     9    35   244   256    46    35    96    25   133   130
               9    50     4    42    85   326    16     8    36     0   394

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723
2 | 1.3882 | 0.6128

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
