Step 3 of 50: validation loss 1.5677, accuracy 0.5552.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   901    36    31     9     0     1     2    10     1     0
               1     0  1025    30     0     0     2     0     7     0     0
               2    65   200   476   117     9     4    16    59    41     3
               3    58   158     3   455     7    86    16   117    84    46
               4    16   329     2     7   476     0     5     1     7   140
               5   103   325     1    25     5   177   138    10    72    59
               6    97   216     0     6     6    52   586     1     3     0
               7    28   126    13     0     4    57     0   752     1   109
               8    17   553    24    11     4     2    13   178   140    67
               9    87   228     4     1    26     5     1    43     2   564

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.7511 | 0.3148
2 | 1.2930 | 0.6248
3 | 1.5677 | 0.5552

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
