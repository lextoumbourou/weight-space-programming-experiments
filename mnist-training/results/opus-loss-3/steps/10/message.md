Step 9 of 50: validation loss 1.0125, accuracy 0.7390.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   840     2    50     0     1     7    43     0    43     5
               1     0   925    97     5     9    10     5     7     6     0
               2    12     5   531   163    52     9     5     3   198    12
               3     6     1    18   692     1   113     1     1   192     5
               4     1    16     1     1   830     1    23    12    15    83
               5     2     6     1    79     8   677    74    22    44     2
               6    50     8     2     0    61     9   819     0    13     5
               7     5     4    39    43    12    11     0   748     4   224
               8    22    21   111   116     3    52    35    29   600    20
               9    17    13    32    17    21    26    10    82    15   728

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.3858 | 0.5462
2 | 1.2956 | 0.5868
3 | 1.1333 | 0.6259
4 | 0.9561 | 0.6843
5 | 0.9639 | 0.6853
6 | 1.0021 | 0.6652
7 | 0.9227 | 0.7348
8 | 0.9806 | 0.7142
9 | 1.0125 | 0.7390

At most 41 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 10 in one Python code block.
