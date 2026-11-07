Step 11 of 50: validation loss 0.9475, accuracy 0.7636.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   794     0     4     1     2     1   167     1     0    21
               1     2   804    20     4    37     1    49    12   132     3
               2     4     0   701    48    75     0    23    62    18    59
               3     0     0     2   763    14   115    60     6    50    20
               4     4     1     0     0   866     0    11     1    21    79
               5     7     2     0    19     3   679    88     1   104    12
               6    10     0     0     0   108     7   779     0     9    54
               7     1     0     5     8     1     1    17   754     7   296
               8     8     3    36     6    11    12   123    60   684    66
               9     2     0     0     6    22     2    31    15    71   812

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9468 | 0.2540
2 | 1.2629 | 0.5742
3 | 1.0920 | 0.6503
4 | 1.0095 | 0.7297
5 | 0.9636 | 0.7647
6 | 0.9087 | 0.8054
7 | 0.8223 | 0.7877
8 | 0.5529 | 0.8265
9 | 0.5545 | 0.8242
10 | 1.0930 | 0.7353
11 | 0.9475 | 0.7636

39 steps left. Reply with the complete build_weights() for step 12 in one Python code block.
