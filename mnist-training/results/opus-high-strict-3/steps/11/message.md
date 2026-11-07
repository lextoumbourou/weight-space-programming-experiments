Step 10 of 15: validation loss 0.9119, accuracy 0.7315.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   883    13    27     0     3     1    34     0    16    14
               1     0   979    50     1     0     3     1    21     9     0
               2    27    22   631    73    47     5     2    26   125    32
               3     5     6    17   628     0   265     4     4    95     6
               4     5    77     4     7   754    19     4     7    42    64
               5     9    10     0    68     4   499   102     9   165    49
               6    52    68     3     0    15    14   773     0    15    27
               7    19    14    24    18     5    55     1   849     2   103
               8    24    81    76   107     1    10    15    33   607    55
               9    26    45    14    21    10    53     4    66    10   712

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.8050 | 0.4403
2 | 1.0673 | 0.6866
3 | 1.3639 | 0.6626
4 | 2.2082 | 0.6541
5 | 1.0513 | 0.7082
6 | 1.0357 | 0.7054
7 | 1.6683 | 0.6427
8 | 0.9795 | 0.7212
9 | 0.9277 | 0.7288
10 | 0.9119 | 0.7315

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
