Step 6 of 15: validation loss 1.0466, accuracy 0.6887.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   784    49    36     1     0     0   115     0     1     5
               1     0  1010    32     2     1     7     3     6     0     3
               2   109    34   448   116     4     4    46    72    91    66
               3    14     0    11   747     0   136    52    41    11    18
               4    13   136    11     0   401     2    18     6    82   314
               5    17     7     5    32     0   624   147    27    46    10
               6    26    60     1     0     1     4   868     0     1     6
               7    26     6     5    20     3     5     6   739     1   279
               8    17   117    61    12     1    11    48   148   460   134
               9    32    15     6     8     0     4     9    80     1   806

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5227 | 0.5126
2 | 1.2842 | 0.6440
3 | 0.9794 | 0.7006
4 | 1.8724 | 0.4922
5 | 1.0033 | 0.6914
6 | 1.0466 | 0.6887

9 steps left. Reply with the complete build_weights() for step 7 in one Python code block.
