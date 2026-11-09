Step 3 of 15: validation loss 1.1663, accuracy 0.6848.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   518     5     0     0     0    34   386     0    48     0
               1     0   930    96    13     0     5     2     5    13     0
               2     9     1   526    97     2    61     5     3   286     0
               3     0     0    15   711     5   272     2     5    20     0
               4     1    26     5     0   724     6    69    15   136     1
               5     0     3     5    72     1   729    20     0    85     0
               6     9    20     4     6    10    24   793     0   101     0
               7    10     2    14    43    55    90    28   788    29    31
               8     1    25    10     6     2    26    15    29   894     1
               9    12    24     0     7    64   117   181   131   190   235

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5340 | 0.7380
2 | 1.1300 | 0.7364
3 | 1.1663 | 0.6848

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
