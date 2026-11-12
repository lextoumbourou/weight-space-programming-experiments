Step 2 of 50: training loss 1.1902, accuracy 0.6278.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   790     7   165     1     0     7    12     3     6     0
               1     0   786     6     2     1     4     3   260     2     0
               2     5     6   495   127     1    12    18     3   323     0
               3     2     1    19   731     0   134     1    10   131     1
               4     4    35     5     1   716     0    58    22    94    48
               5    11     2     5    92     0   432    83     5   284     1
               6    78    26     3    10    75    44   645     1    85     0
               7     8     4    83    67     2    11     0   562    48   305
               8    22    42    71    40     5    17    19    82   693    18
               9    85    24    54     8    44    23     9    68   218   428

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2326 | 0.5909
2 | 1.1902 | 0.6278

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.

