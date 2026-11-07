Step 2 of 50: validation loss 1.8335, accuracy 0.5049.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   578     2    24     0     0     8   193     1   185     0
               1     2   873   141     0     9     2     3    34     0     0
               2     9     6   434    17    22     9    21     2   469     1
               3     2     5    47   229     1    89    10     9   628    10
               4     1    31    17     0   469     0    25     9   290   141
               5     7    11    15     5     2   230   183     4   455     3
               6    20    20     4     0    63     0   760     0   100     0
               7     8     8    93     8     7    42     7   360   142   415
               8     6    29   106     1     4     1    38    12   789    23
               9    20    24    15     0    10     5    52    17   491   327

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4065 | 0.6314
2 | 1.8335 | 0.5049

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
