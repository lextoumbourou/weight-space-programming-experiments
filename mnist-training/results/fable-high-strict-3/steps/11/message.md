Step 10 of 15: validation loss 1.4515, accuracy 0.5423.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   736    13    13    13    18    13    82     5    91     7
               1     0   941    81    28     9     1     0     2     2     0
               2    38    45   313    69   196    38    15    14   127   135
               3     6    12    32   481    37   341     9    34    74     4
               4     2    23     3     0   900     3     1     9    15    27
               5     2    63     2   135   155   361    30    56   105     6
               6     4   136     0     4   183    57   546     0    28     9
               7     6    30    10     4   208     3     0   780     0    49
               8     0   161   205   114    59   116     1   119   219    15
               9     6    35     2    21   563    27     1   139    21   146

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
9 | 1.4461 | 0.5700
10 | 1.4515 | 0.5423

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
