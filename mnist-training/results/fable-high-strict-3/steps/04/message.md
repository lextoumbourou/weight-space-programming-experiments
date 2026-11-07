Step 3 of 15: validation loss 1.4273, accuracy 0.5260.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   669     0    23    26     2    47   217     0     6     1
               1     0   801    93   164     2     2     0     2     0     0
               2    30    11   510   155   131   102     4    13    28     6
               3     3     0    19   468     3   502     4    11    14     6
               4     4     6    50    20   823    37     3     4    10    26
               5     0    13     4   331    46   469    23     8    12     9
               6     5    11     5   147    26   439   325     0     9     0
               7     4     8    29    26   145    56     1   802     1    18
               8     0     6   325   275    17   184     2    48   127    25
               9     7     3    24    70   439    55     3    91     3   266

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.9434 | 0.3796
2 | 1.6381 | 0.4687
3 | 1.4273 | 0.5260

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
