Step 10 of 50: training loss 0.9399, accuracy 0.7370.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   905    16    62     0     2     3     2     0     0     1
               1     0   957    77     8     2     7     4     8     0     1
               2    14     3   662   113   141     8     6     3    40     0
               3     4     5    11   839     2   114     7    28    18     2
               4     4    63    13     3   767     4     3    52     2    72
               5    11     6    17    64     2   709    47    37    22     0
               6    47    32    14     0    64     4   806     0     0     0
               7    26     3    26    62     3     6     0   909     3    52
               8     8   185    93    18    12    29    93   261   259    51
               9    25    34     8    17    23    24     9   258     6   557

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
10 | 0.9399 | 0.7370

At most 40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.

