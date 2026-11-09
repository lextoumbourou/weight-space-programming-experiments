Step 1 of 15: validation loss 0.9176, accuracy 0.7428.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   837     0     2     0     0     2    36     0   111     3
               1     0   851     7    13     0     4     1     4   182     2
               2    20     1   550   253     2     1     5     3   145    10
               3     0     0     3   973     1    28     1     2    20     2
               4    11    14     2     1   637     0    38     1   129   150
               5     1     0     0   260     1   493    52     0   107     1
               6    66     3     3     0     2     1   845     0    35    12
               7    46     0    11    81    21    60     1   594    49   227
               8     5     4     1    29     2     2    15     4   928    19
               9    27     4     0    33    13    15    48     5    96   720

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428

14 steps left. Reply with the complete build_weights() for step 2 in one Python code block.
