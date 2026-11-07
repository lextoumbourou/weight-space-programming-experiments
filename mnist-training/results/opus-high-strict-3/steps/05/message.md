Step 4 of 15: validation loss 2.2082, accuracy 0.6541.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   799    30    13     0     0     0   127    10     0    12
               1     0   985    72     1     0     3     0     3     0     0
               2    39   109   610    39    27     0     6    40    83    37
               3    13    45    50   562     0   219    44    59    32     6
               4     5   211     9     2   633    12    25    19     8    59
               5    14   103     0    52     4   393   232    40    17    60
               6    41    91     5     0     3     0   809     0     3    15
               7     5    38    22     4     2    17     1   941     0    60
               8    18   385   132    21     2     6    43   128   240    34
               9    30   117    10     5     7    22     7   192     2   569

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.8050 | 0.4403
2 | 1.0673 | 0.6866
3 | 1.3639 | 0.6626
4 | 2.2082 | 0.6541

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
