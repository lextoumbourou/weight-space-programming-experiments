Step 3 of 50: training loss 1.2078, accuracy 0.6210.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   741     0    14    10     0    12   195     0    15     4
               1     0   813    35     8     0     0     1    54   119    34
               2    33     0   219   510     2     0    18     2   186    20
               3     1     0     0   871     0   116    11     1    28     2
               4    20     4     0    88   158    10    65     3   116   519
               5     3     0     0   185     0   522    96     1   105     3
               6    40     1     0     3     0     4   883     0    33     3
               7    22     1     3   131     0    53    30   597    31   222
               8    11     6     1    39     0    14    60     3   857    18
               9    24     1     0   228     0    20    92    22    25   549

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2181 | 0.6165
2 | 1.3785 | 0.5515
3 | 1.2078 | 0.6210

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.

