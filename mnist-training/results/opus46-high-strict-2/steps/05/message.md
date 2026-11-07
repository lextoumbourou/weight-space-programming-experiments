Step 4 of 15: validation loss 1.7213, accuracy 0.4072.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   698     2    38    14     1    78    31    29     3    97
               1     0   795    11     1     0     2     0   252     0     3
               2    10    35   496   245    10    39   116    21     6    12
               3     0    98    38   211    64    34    12    44     0   529
               4     7   112    14     2   460     0   168    31   178    11
               5    12    52    36    12    38   260   216    58    13   218
               6    36    32    46    17     4     2   782     1    42     5
               7    13    75     2    47    31    11     1   128     3   779
               8     4   176   132    38    55   116    66   309    13   100
               9    32   128     1    14   217    18    24    99   199   229

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.4126 | 0.1130
2 | 1.9302 | 0.3116
3 | 1.8248 | 0.3637
4 | 1.7213 | 0.4072

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
