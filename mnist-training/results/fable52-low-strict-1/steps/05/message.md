Step 4 of 15: validation loss 1.8724, accuracy 0.4922.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   515    39     0     0     0     0    14     0   419     4
               1     0  1024    24     0     1     4     2     2     3     4
               2    18    80   194    23     2     0     9    11   600    53
               3     0     3     3   287     0     3     1     2   718    13
               4     3   171     0     0   368     0     1     1   275   164
               5     0    31     1     5     0    19    16     2   837     4
               6     1   109     0     0     1     1   615     0   240     0
               7     5    38     5     5     4     0     0   473   101   459
               8     0   239     3     0     2     0     2     6   700    57
               9     8    54     0     1     1     0     1     6   163   727

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5227 | 0.5126
2 | 1.2842 | 0.6440
3 | 0.9794 | 0.7006
4 | 1.8724 | 0.4922

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
