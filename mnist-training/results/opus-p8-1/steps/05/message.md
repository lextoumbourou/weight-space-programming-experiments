Step 4 of 50: validation loss 1.3191, accuracy 0.5505.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   788    14    42     1     0    15     1     7   123     0
               1     0   894    33     0     1     7     1   127     1     0
               2    14    23   300    84     5    22     5    38   499     0
               3     3    18     3   341     1   111     0    60   477    16
               4     3    74     0     5   571     0     1     7   291    31
               5     7    12     2    52     1   352    46    10   414    19
               6    16    89     2     6     0    19   371     1   463     0
               7    15    15    32     1    21   138     0   785    40    43
               8     1    82    27     2     1     2     1   112   761    20
               9    27    58     5     0    70    11     1    62   385   342

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.7511 | 0.3148
2 | 1.2930 | 0.6248
3 | 1.5677 | 0.5552
4 | 1.3191 | 0.5505

At most 46 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
