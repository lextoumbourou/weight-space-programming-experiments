Step 4 of 15: validation loss 10.2460, accuracy 0.0684.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     6    61   281   129     0     9    98   307   100     0
               1   139     7     5     5     0   883    18     3     4     0
               2    19   149   461   159     0     5    41   119    37     0
               3     8    72   501   159     1    10    55   193    31     0
               4    15    52    16     2     0   284   468   140     5     1
               5    10   112   359   137     0    13    47   193    44     0
               6    21   183   541   124     1     4    19    56    18     0
               7   500    45    15     0     0   475    42    13     0     0
               8    52   229   217    17     0    92   247   149     6     0
               9   153    93    26     1     0   332   291    59     6     0

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9981 | 0.6911
2 | 1.2553 | 0.6304
3 | 0.8910 | 0.7126
4 | 10.2460 | 0.0684

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
