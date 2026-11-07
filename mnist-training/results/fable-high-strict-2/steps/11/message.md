Step 10 of 15: validation loss 1.5251, accuracy 0.5627.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   747     5     0     0     0     0    86     0    94    59
               1     0   941    76     2     9    10     6     1    18     1
               2    37     6   241    19    23    22    64     1   358   219
               3     5     4     3   243     3   378   174     4   196    20
               4     2    12     0     0   714    21     0     0    85   149
               5    12     7     5    11     4   495   154     2   161    64
               6    25    18     0     0   114    53   541     0    72   144
               7    10    11    12     3    17    32     2   447    30   526
               8     0    39    41    21     5    75    19     6   711    92
               9     6    17     0     1   169   131     1    21    68   547

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.1586 | 0.4753
2 | 1.4530 | 0.4972
3 | 1.2907 | 0.5670
4 | 1.3876 | 0.4982
5 | 1.2362 | 0.5778
6 | 1.2805 | 0.5933
7 | 1.3757 | 0.5399
8 | 1.2644 | 0.5950
9 | 1.2366 | 0.5959
10 | 1.5251 | 0.5627

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
