Step 9 of 50: training loss 0.9434, accuracy 0.7246.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   903    16    62     0     1     5     3     0     0     1
               1     0   956    77     7     2     7     6     8     0     1
               2    15     3   661   115   136     9     7     3    41     0
               3     4     5    11   835     2   115     9    28    19     2
               4     4    63    13     3   754     4    10    51     6    75
               5    11     6    16    51     2   656    92    29    51     1
               6    55    20    12     0   104    12   764     0     0     0
               7    26     3    26    59     3     6     0   908     4    55
               8    15   178    82    20    12    38   118   239   253    54
               9    25    33     8    16    24    21    14   253    11   556

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
9 | 0.9434 | 0.7246

At most 41 steps left. Reply with the complete build_weights() for step 10 in one Python code block.

