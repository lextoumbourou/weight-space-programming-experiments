Step 5 of 50: validation loss 0.9639, accuracy 0.6853.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   810    19    65     0    21     2    60     3     3     8
               1     0  1015    44     0     5     0     0     0     0     0
               2     8    40   589    33   155     0     5    55    35    70
               3    11     7    35   597    14   287    25    14    30    10
               4     1    50     1     1   903     1     0    14     1    11
               5     0    18     4   128    64   550    96    50     2     3
               6    18    81     1     0   304     8   544     0     2     9
               7     4    20     5     0    29    23     0   929     0    80
               8    12    63   115    92    23    26    71   202   350    55
               9     6    42     8     7   131    13     1   185     2   566

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.3858 | 0.5462
2 | 1.2956 | 0.5868
3 | 1.1333 | 0.6259
4 | 0.9561 | 0.6843
5 | 0.9639 | 0.6853

At most 45 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 6 in one Python code block.
