Step 8 of 15: validation loss 1.5149, accuracy 0.5403.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   636     3     3     6     0     4   253     0    54    32
               1     0   834   100   119     2     1     0     2     6     0
               2    32    21   362    49    45     3     9    17   145   307
               3     6     0    37   404     2   180    18    37   324    22
               4    12     4     2    16   597    16     2     1   178   155
               5     1    17     0   152    56   269    91    21   283    25
               6     7    42     1    42    40    67   581     0   104    83
               7     5     6    27    45    83    12     9   805    18    80
               8     3    28   226   145     7    38     3    30   493    36
               9     8     3     7   102   101    20     2    23   273   422

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.9434 | 0.3796
2 | 1.6381 | 0.4687
3 | 1.4273 | 0.5260
4 | 1.6030 | 0.4847
5 | 1.4504 | 0.5204
6 | 1.5097 | 0.4936
7 | 1.4970 | 0.5433
8 | 1.5149 | 0.5403

7 steps left. Reply with the complete build_weights() for step 9 in one Python code block.
