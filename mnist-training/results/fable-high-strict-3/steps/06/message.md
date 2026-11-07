Step 5 of 15: validation loss 1.4504, accuracy 0.5204.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   713     1     7    13     0    15    24     0   196    22
               1     0   852   126    78     2     2     0     2     2     0
               2    30    16   408    88    62    13     0    11   223   139
               3     6     0    18   398     1   380     1    16   196    14
               4     3     9    16    11   556    19     0     3   140   226
               5     1    20     3   232    21   386     0    13   210    29
               6     9    26     4    94    16   280   214     0   298    26
               7     4    12    28    21   106    42     0   789     5    83
               8     0    16   237   151    10    85     0    38   442    30
               9     4     8    17    46   264    29     0    82    65   446

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.9434 | 0.3796
2 | 1.6381 | 0.4687
3 | 1.4273 | 0.5260
4 | 1.6030 | 0.4847
5 | 1.4504 | 0.5204

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
