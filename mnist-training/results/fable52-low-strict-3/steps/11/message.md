Step 10 of 15: validation loss 1.0006, accuracy 0.7812.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   754     6    17     0     0     8   129     0    71     6
               1     0   933    90     1    10     0     0    22     7     1
               2    16     2   681   179    38    12     2     3    43    14
               3     0     0     7   887    16   103     3     3     9     2
               4     7     6     5     0   943     0     8     4     6     4
               5     3     1     8    73    16   747    42     0    23     2
               6    34     9    18     0    91    17   769     0    25     4
               7    63     0    11    69    93    10    10   597    13   224
               8     5    15    28     7    15    20    37    23   817    42
               9    19     8     0    11    90    30    64    31    24   684

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5340 | 0.7380
2 | 1.1300 | 0.7364
3 | 1.1663 | 0.6848
4 | 1.0775 | 0.7421
5 | 1.0404 | 0.7677
6 | 1.0624 | 0.7534
7 | 1.0190 | 0.7860
8 | 1.0284 | 0.7683
9 | 1.0103 | 0.7890
10 | 1.0006 | 0.7812

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
