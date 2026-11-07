Step 3 of 50: validation loss 1.5014, accuracy 0.6332.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   886     9    65     0     0     0    28     3     0     0
               1     0   879    18     2     0     1     4   160     0     0
               2    39    18   576    91    21    20    94    10   120     1
               3    17    13    22   656     3   142    65    30    36    46
               4    11    72     7     1   497     0   165    18     3   209
               5    45    22     2   123     4   445   201    32     6    35
               6   102    44     2     3     1    10   798     3     3     1
               7    17    13   226    18    33    82     2   593     2   104
               8    30    44   107    84     2     7   148   137   317   133
               9    63    50    23     6    21     3    21    74    15   685

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.8708 | 0.4273
2 | 1.4873 | 0.5904
3 | 1.5014 | 0.6332

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
