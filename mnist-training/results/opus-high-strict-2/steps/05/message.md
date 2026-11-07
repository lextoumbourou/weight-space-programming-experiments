Step 4 of 15: validation loss 1.0664, accuracy 0.6522.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   880    13    40     0     0     8    44     5     0     1
               1     0   933     7     0     0     1     0   120     0     3
               2    26    81   657    49    53     6    12    36    70     0
               3     3    11    26   554     1   257    37    60    76     5
               4    15   101    13     3   704     0    20    54    12    61
               5    26    18     0    27    16   503   242    13    46    24
               6   138    68    10     1    61    49   585     0    54     1
               7    69    23    30    26    34    34     1   846     0    27
               8    11   126   133     8     4     5    54   133   421   114
               9   144    46    26    19   103    14    22   130    18   439

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723
2 | 1.3882 | 0.6128
3 | 1.1668 | 0.6014
4 | 1.0664 | 0.6522

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
