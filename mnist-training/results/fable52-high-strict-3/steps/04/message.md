Step 3 of 15: validation loss 0.8671, accuracy 0.7260.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   652    31    25     0     0     5     0     0   260    18
               1     0  1028    13     3     0     0     0     8    10     2
               2     2    17   771    18     1     4     2    32   117    26
               3     0     4    93   657     0    64     4    19   181     8
               4     0   202     4     0   629     0     2     1    28   117
               5     1    27     5    14     2   626    36     2   194     8
               6     3    83    16     0    16     2   690     0    83    74
               7     8    47    25     9    12    12     0   637    13   327
               8     1   139    19     2     1     1     8    12   770    56
               9     7    85     2     1     4     5     4    12    41   800

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428
2 | 0.8203 | 0.7656
3 | 0.8671 | 0.7260

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
