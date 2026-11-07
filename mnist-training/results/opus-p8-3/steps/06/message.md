Step 5 of 50: validation loss 1.1075, accuracy 0.6597.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   869     9    83     0     1     3    16     3     7     0
               1     0   878    18     2     1     2     3   160     0     0
               2    18    18   558    86    47    24    38     9   192     0
               3    10    13    19   626     6   187    18    30    92    29
               4     8    57    11     1   688     0    61    17    19   121
               5    35    23     2   111    11   562    96    31    17    27
               6    99    54     2     6    10    39   702     6    48     1
               7    13    13   231    17    53   101     1   592     3    66
               8    10    47    83    61     7    20    69   142   487    83
               9    43    49    23     8    57    11     7    77    51   635

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.8708 | 0.4273
2 | 1.4873 | 0.5904
3 | 1.5014 | 0.6332
4 | 1.5245 | 0.5778
5 | 1.1075 | 0.6597

At most 45 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
