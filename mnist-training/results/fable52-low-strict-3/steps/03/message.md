Step 2 of 15: validation loss 1.1300, accuracy 0.7364.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   587     2     4     0     1    16   358     0    22     1
               1     0   926    71     4    11    13     0     4    33     2
               2     3     0   665   136    28    55     4     2    91     6
               3     0     0     3   625     2   396     0     1     3     0
               4     0     6     4     0   935     1    18     6    12     1
               5     2     1     1    43     6   812    22     0    28     0
               6    23     4     7     0    89     5   804     0    34     1
               7     2     2    15    38    50   161    24   760     9    29
               8     3    17     7     3    12    38    26    18   882     3
               9     6    11     0     3    93   229   117    79    55   368

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5340 | 0.7380
2 | 1.1300 | 0.7364

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
