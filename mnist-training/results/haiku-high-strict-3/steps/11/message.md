Step 10 of 15: validation loss 3.0078, accuracy 0.3644.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   795     2    31    31    11    10    83     0    19     9
               1     0   751   133     5     2     4     0   168     1     0
               2     9     0   402   180    28    85     2     3   267    14
               3    14    20   201   525    73    87     2     7    96     5
               4     6    24     0     6   527   242     0     4   164    10
               5    51    42   120   147   106   296    15     9   117    12
               6   120    90    68    67   353    78    49     0   111    31
               7    24     9     4   220    46   111     0   145     8   523
               8     0    53   378    84    17   327     0    51    97     2
               9    20    50     1    30   354   290     1     9   149    57

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 17.3035 | 0.3631
2 | 3.9784 | 0.3627
3 | 4.9236 | 0.1423
4 | 2.1846 | 0.2680
5 | 3.6147 | 0.1499
6 | 3.7019 | 0.3624
7 | 7.7517 | 0.1041
8 | 3.3955 | 0.1361
9 | 3.2968 | 0.3653
10 | 3.0078 | 0.3644

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
