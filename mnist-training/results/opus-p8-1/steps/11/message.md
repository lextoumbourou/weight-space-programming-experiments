Step 10 of 50: validation loss 1.7526, accuracy 0.5254.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   797     4   136     0     0     0     0     0    54     0
               1     1   836   187     0     0     0     4    21    15     0
               2    28     4   467    40     0     8    14     0   428     1
               3     7     0    22   523     0    47     2     3   421     5
               4     9    20    36     3   266     0    14     0   561    74
               5    10     2    17    46     0   272   154     1   412     1
               6    62    16    14     0     0     0   654     0   221     0
               7    10     5   177    20     1   145     0   354   115   263
               8     7    20   151     1     0     0     6     3   810    11
               9    51    16    55     1     1     8     2     6   546   275

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.7511 | 0.3148
2 | 1.2930 | 0.6248
3 | 1.5677 | 0.5552
4 | 1.3191 | 0.5505
5 | 1.2707 | 0.6192
6 | 1.8067 | 0.6464
7 | 1.3242 | 0.6409
8 | 4.7657 | 0.5293
9 | 1.2504 | 0.6462
10 | 1.7526 | 0.5254

At most 40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
