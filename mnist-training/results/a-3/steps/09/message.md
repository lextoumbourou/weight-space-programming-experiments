Step 8 of 50: training loss 0.8913, accuracy 0.7369.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   837    10    63     0     1     1     3     1    75     0
               1     1   987    45     6     3     6     6     9     0     1
               2    10     2   588    55   166     1    16     4   148     0
               3     4     6     6   745     3   141     9    17    93     6
               4     2    33     4     0   720     1     5    21    47   150
               5    10     5     8    43     2   643    50    16   135     3
               6    31    21     5     0    35     0   860     0    15     0
               7    20     2    35    44     5     4     0   796    14   170
               8     4   135    46     2     3    11    54   153   531    70
               9    17    25     6     8    52     7     4   143    37   662

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2152 | 0.6072
2 | 1.2620 | 0.6013
3 | 2.4275 | 0.5608
4 | 1.4795 | 0.6030
5 | 1.9930 | 0.3961
6 | 1.0068 | 0.6843
7 | 0.9306 | 0.7290
8 | 0.8913 | 0.7369

At most 42 steps left. Reply with the complete build_weights() for step 9 in one Python code block.

