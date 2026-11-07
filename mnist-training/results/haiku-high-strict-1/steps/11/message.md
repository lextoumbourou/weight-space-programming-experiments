Step 10 of 15: validation loss 1.9822, accuracy 0.3380.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   468     0     0     0     1     0    65    85   327    45
               1     0   834     0     0     1     0     0   102   112    15
               2     0     1   285     0    33     0     2   181   422    66
               3     0     4    30     2    23     0     6   584    20   361
               4     0    12     0     0    61     0     0     2   619   289
               5     0     1    18     0    20     1    54   240   194   387
               6     0    18     1     0    57     0    10     0   851    30
               7     0     2     0     1     0     0     0   806    34   247
               8     0    33     6     3    18     1     2   481   218   247
               9     1    11     0     0     4     0     1    83   166   695

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.6085 | 0.1223
2 | 1.9985 | 0.4359
3 | 2.0168 | 0.3084
4 | 2.2109 | 0.3604
5 | 2.2342 | 0.2196
6 | 2.2229 | 0.4016
7 | 2.1604 | 0.2039
8 | 2.1559 | 0.2034
9 | 8.1275 | 0.1379
10 | 1.9822 | 0.3380

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
