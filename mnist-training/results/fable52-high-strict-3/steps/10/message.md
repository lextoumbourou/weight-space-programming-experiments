Step 9 of 15: validation loss 0.7161, accuracy 0.7895.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   783     0    67     0     0    12    40     0    87     2
               1     0   879    75     5    40     6     2    46     6     5
               2    42     2   755    66     2     3     4    27    84     5
               3     3     0    11   810     0   119     1     2    81     3
               4    11     8    45     4   652    15    46     8    58   136
               5     5     1     5    14     2   797    29    12    50     0
               6    79     4     9     0    22     6   840     0     7     0
               7    21     0    32    33     3    80     1   786    22   112
               8     1     7    55     3     2     9    20    11   864    37
               9    33     0    18    37     2    72    20    29    21   729

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428
2 | 0.8203 | 0.7656
3 | 0.8671 | 0.7260
4 | 1.3566 | 0.5882
5 | 0.8736 | 0.7192
6 | 0.9409 | 0.7196
7 | 0.8792 | 0.7403
8 | 0.7594 | 0.7718
9 | 0.7161 | 0.7895

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.
