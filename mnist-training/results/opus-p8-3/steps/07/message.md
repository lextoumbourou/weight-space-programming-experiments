Step 6 of 50: validation loss 1.1029, accuracy 0.6659.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   884    11    54     1     2     0    24     1    14     0
               1     0  1000    20     7     3     0     2    32     0     0
               2    27    19   439   174    60     3    45    11   212     0
               3    11    14     8   722    19    38    27    22   132    37
               4     8    69     2     6   689     0    65     2    21   121
               5    45    23     1   187    25   378   161    21    38    36
               6   103    52     0     8    15    10   729     0    49     1
               7    38    26    32    55    89    22     3   648    11   166
               8    18    80     4   137    10     1    85    69   512    93
               9    48    62     1    21    68     0     7    39    57   658

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.8708 | 0.4273
2 | 1.4873 | 0.5904
3 | 1.5014 | 0.6332
4 | 1.5245 | 0.5778
5 | 1.1075 | 0.6597
6 | 1.1029 | 0.6659

At most 44 steps left. Reply with the complete build_weights() for step 7 in one Python code block.
