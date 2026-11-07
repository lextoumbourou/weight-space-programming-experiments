Step 4 of 50: validation loss 1.0021, accuracy 0.6869.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   853    12    69     0     2     3    38     1    13     0
               1     0  1010    36     0     8     3     1     6     0     0
               2    18    15   588   141    44    19    24     7   134     0
               3     4     8    18   809     2   120    25    21    14     9
               4    11   108    24     1   493     3    82     2    62   197
               5    39    24     3    20     9   637   150    15    10     8
               6    74    70     1     0    42    86   664     0    30     0
               7    35     7   183    16    16    70     2   671     3    87
               8     7    85   150    28     5    10    65    49   544    66
               9    62    60    46     8    18     9    11    41   106   600

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3242 | 0.5148
2 | 1.1827 | 0.6054
3 | 1.0792 | 0.6656
4 | 1.0021 | 0.6869

At most 46 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 5 in one Python code block.
