Step 3 of 50: training loss 2.4275, accuracy 0.5608.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   740    57    61     0    60     4    66     0     2     1
               1     0  1054     3     0     0     3     3     1     0     0
               2     5   110   599    27   129    18    48    21    33     0
               3     3    87    46   458     6   266    23   104    29     8
               4     3   329     3     1   520     9     5     0     0   113
               5     4   153     3     8     2   555   187     1     2     0
               6    20   196     5     0   100    18   624     1     2     1
               7    11   104   196    17     8    27     0   636     0    91
               8     5   559    43     1    16    43   123    28   105    86
               9    30   267    45     0   163    72     4    63     0   317

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2152 | 0.6072
2 | 1.2620 | 0.6013
3 | 2.4275 | 0.5608

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.

