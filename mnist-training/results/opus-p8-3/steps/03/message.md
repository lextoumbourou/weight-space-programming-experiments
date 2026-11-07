Step 2 of 50: validation loss 1.4873, accuracy 0.5904.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   815     9    90     0     0    10    64     3     0     0
               1     0   872    11     1     0     0     3   177     0     0
               2    21    29   429   348     0    21    84    15    42     1
               3    10    28    14   732     1    85    70    34    14    42
               4    11   108    14     1   359    18   276    33     0   163
               5    23    61    11    82     0   436   257    18     1    26
               6    48    96     3     0     0    48   769     2     1     0
               7     6    28   211    26    43    42     2   664     0    68
               8    24    82   130   150     0    19   179   129   239    57
               9    69    81    61    16     6    14    35    88     2   589

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.8708 | 0.4273
2 | 1.4873 | 0.5904

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
