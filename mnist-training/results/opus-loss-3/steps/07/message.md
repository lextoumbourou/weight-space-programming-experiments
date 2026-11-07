Step 6 of 50: validation loss 1.0021, accuracy 0.6652.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   755     1    21     0     1     4    23     0   178     8
               1     0   950    67     2    10     6     3     6    19     1
               2     9     5   334    84    42     3     6     2   475    30
               3     2     1     3   406     1    74     2     1   534     6
               4     1    15     0     0   699     0    17     8    72   171
               5     1     9     0    58     8   506    92    18   214     9
               6    33     7     1     0    56     7   736     0   121     6
               7     4     7    22    22     7     6     0   626    24   372
               8    13    26    21    36     3    13    16    18   840    23
               9    11    13    11     8    10     7     7    37    57   800

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.3858 | 0.5462
2 | 1.2956 | 0.5868
3 | 1.1333 | 0.6259
4 | 0.9561 | 0.6843
5 | 0.9639 | 0.6853
6 | 1.0021 | 0.6652

At most 44 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 7 in one Python code block.
