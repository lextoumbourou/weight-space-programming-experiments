Step 2 of 15: validation loss 1.6381, accuracy 0.4687.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   285     0     3     4     0     0   689     0     6     4
               1     0   758   157   127     0     1     6     2     7     6
               2    10     6   425    42     1     0    93    13   309    91
               3     2     0    16   238     0     9   212    18   512    23
               4     1     2     5     8    36     0    50     1   305   575
               5     0     5     6   101     0    38   525     3   207    30
               6     4     5     3    36     0     0   877     0    30    12
               7     0     5    30    12     0     5    60   737    30   211
               8     0     1   152    95     0     1    96    22   571    71
               9     0     2     7    24     0     0    41    25   140   722

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.9434 | 0.3796
2 | 1.6381 | 0.4687

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
