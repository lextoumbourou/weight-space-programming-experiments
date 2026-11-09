Step 8 of 15: validation loss 0.7594, accuracy 0.7718.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   769     0    68     5     0     9    36     0   103     1
               1     0   872    79     7    41     6     2    47     5     5
               2    33     2   724   140     2     2     2    18    65     2
               3     3     0     6   922     0    52     0     1    45     1
               4    10     7    31     9   599    11    44     5    93   174
               5     5     1     2   128     2   684    35    11    47     0
               6    73     3     9     0    19     6   848     0     9     0
               7    18     0    31    60     6    70     1   769    32   103
               8     1     6    52    21     2     3    19    10   869    26
               9    28     0    12   138     2    44    23    25    27   662

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428
2 | 0.8203 | 0.7656
3 | 0.8671 | 0.7260
4 | 1.3566 | 0.5882
5 | 0.8736 | 0.7192
6 | 0.9409 | 0.7196
7 | 0.8792 | 0.7403
8 | 0.7594 | 0.7718

7 steps left. Reply with the complete build_weights() for step 9 in one Python code block.
