Step 8 of 15: validation loss 1.2644, accuracy 0.5950.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   779    12    11     0     0     0    61     6    94    28
               1     0  1008    45     4     0     4     2     1     0     0
               2    19    42   539    69    14    13    24     7   195    68
               3     2    43    10   597     1   190    96    26    60     5
               4     3    99     9     0   622    15     0    31    82   122
               5    11   115     6   104     1   410    94    60    78    36
               6    31   109     8    13    85    56   466     0    98   101
               7    12    80    10    25     7    21     2   793     6   134
               8     0   181   174    89     0    37     6   131   355    36
               9     5   124     0     4   111    87     1   212    36   381

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

7 steps left. Reply with the complete build_weights() for step 9 in one Python code block.
