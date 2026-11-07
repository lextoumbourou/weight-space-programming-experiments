Step 3 of 15: validation loss 1.3639, accuracy 0.6626.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   695     2    11     0     0     0   223     0    39    21
               1     0   836   214     1     0     2     5     3     2     1
               2    14    11   486    59     5     0    14    12   319    70
               3     3     1    15   612     0   111    37     3   231    17
               4     5    25     5     1   568     5    64     9   120   181
               5     5     6     4    94     2   295   318    11    87    93
               6    19    16     3     0     1     0   891     0     5    32
               7     5     3    42    15     1    13     3   739     5   264
               8     2    45    99    24     0     0    55    22   695    67
               9    11    14    11    10     1     5     9    51    40   809

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.8050 | 0.4403
2 | 1.0673 | 0.6866
3 | 1.3639 | 0.6626

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
