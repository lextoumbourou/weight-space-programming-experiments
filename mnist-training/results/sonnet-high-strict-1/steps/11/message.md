Step 10 of 15: validation loss 1.5757, accuracy 0.4177.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   800    64   101     2    18     0     0     0     5     1
               1     0  1054     0     0     0     3     0     0     7     0
               2     7   302   442    16   130     3     2     2    85     1
               3     3   360    17   504     1   122     0     3    20     0
               4     7   535     1     0   138    26     5     0   233    38
               5    11   324     0    61     4   435    39     0    41     0
               6   105   309     0     1    52    98   191     0   205     6
               7     3   474   111    78     0    32     0   290     7    95
               8     7   771    54    21     1    20     4     7   121     3
               9    41   576    22     4     4    57     1     3    51   202

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 28.9933 | 0.1083
2 | 1.7764 | 0.4517
3 | 2.0240 | 0.3052
4 | 1.6377 | 0.5136
5 | 1.4611 | 0.5491
6 | 1.4698 | 0.5288
7 | 1.3827 | 0.5680
8 | 1.3262 | 0.5729
9 | 1.3440 | 0.5742
10 | 1.5757 | 0.4177

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
