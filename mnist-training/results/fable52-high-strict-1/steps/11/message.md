Step 10 of 15: validation loss 0.7933, accuracy 0.7499.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   816     0     0     0     3     0   114     0    56     2
               1     1   986    10     3    22     1    23    17     0     1
               2   141     1   520    68    18     3    27    17   160    35
               3    19     0     2   832     0   103    10     3    51    10
               4     5     8     8     1   790     1    10    23     1   136
               5    41     0    11   100     8   617    79    12    35    12
               6    87     2    12     0    47     5   760     2    45     7
               7    30     3     8    12    39     8     2   804     2   182
               8    27     2    86   124     2    28    31    18   630    61
               9    50     5     1    28    36     9     1    79     8   744

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3919 | 0.2590
2 | 1.4921 | 0.4959
3 | 4.1205 | 0.2481
4 | 2.9187 | 0.3582
5 | 378.0263 | 0.1887
6 | 1.6447 | 0.5262
7 | 1.2630 | 0.5479
8 | 264.5562 | 0.0551
9 | 0.8597 | 0.7217
10 | 0.7933 | 0.7499

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
