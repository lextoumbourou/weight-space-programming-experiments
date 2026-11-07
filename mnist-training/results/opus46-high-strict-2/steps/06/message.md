Step 5 of 15: validation loss 1.6828, accuracy 0.4146.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   703     2    12    19     1   112    11    28    80    23
               1     0   837     7     3     0     3     0   213     1     0
               2    16    35   375   298     3    46   142    17    58     0
               3     0    76    18   347    59    47     6    30    61   386
               4     6    40     1     2   337     0    96     9   491     1
               5    31    32     9    29    26   295   150    58   136   149
               6    43    14    10     4     1     1   750     1   143     0
               7    15    68     1   104    29    27     0   130    48   668
               8     5   132    42    49    28   129    53   236   291    44
               9    54    35     0    10   120    10     6    37   608    81

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.4126 | 0.1130
2 | 1.9302 | 0.3116
3 | 1.8248 | 0.3637
4 | 1.7213 | 0.4072
5 | 1.6828 | 0.4146

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
